"""
orchestrator.py
───────────────
Chef d'orchestre du pipeline pour UN exercice. (Le job/threading vit dans
server.py ; le mode batch boucle simplement sur run_exercise.)

Ordre des étapes :
  1. Analyse + notions + RAG fonctions (PARALLÈLE — indépendants)
  2. Génération par paires (séquentielle, contexte partagé)
  3. Post-traitements déterministes (config_standard, assemblage 4-backticks,
     dédoublonnage)
  4. Substitution des solutions validées (si présentes dans la source)
  5. Audit LLM (≤ 2 itérations, patches toutes-occurrences sécurisés)
  6. Post-traitements déterministes finaux : auto-lift GÉNÉRALISÉ des
     injections non nues, renommage underscores, auto-correctif $+chiffre,
     :id: vide, diff solutions, décimales (langue), invariants multi-seed,
     contrôles matplotlib
  7. Langue cible (déterministe ou LLM masqué)
  8. PORTE HARNAIS (HARNESS_GATE_SEEDS graines) + 1 boucle de réparation LLM
     max ; verdict exposé dans le résultat.
"""

from __future__ import annotations

import json
import logging
import time
from typing import Callable, Optional

from app.config import (
    HARNESS_GATE_SEEDS,
    HARNESS_REPAIR_MAX,
    MAX_ESCALADES,
    MULTI_SEED_NUM,
    PEDAGO_AUDIT_ENABLED,
    PEDAGO_ESCALATE_IN_AUTO,
    PEDAGO_REPAIR_MAX,
)
from app.knowledge.rules_digest import build_rules_digest
from app.llm.client import process_with_openrouter
from app.llm.cost import cost_delta, cost_snapshot
from app.rag.catalogue import catalogue_for
from app.pipeline import postprocess as pp
from app.pipeline.analyze import run_analysis_phase
from app.pipeline.audit import (
    format_pedagogical_issues,
    pedagogical_badness,
    run_audit,
    run_pedagogical_audit,
)
from app.pipeline.fewshots import fewshot_for, fewshot_for_declinaison
from app.pipeline.generate import (
    assemble_exercise,
    build_exercise_metadata,
    generate_pair_blocks,
    split_original_questions,
)
from app.pipeline.prompts import (
    PEDAGOGICAL_REPAIR_PROMPT,
    REPAIR_PROMPT,
    SYSTEM_PROMPT,
    TRANSLATE_CONSTRAINTS_PROMPT,
)
from app.pipeline.solutions import replace_gen_solutions_with_source
from app.pipeline.translate import ensure_language
from app.validation import harness
from app.validation.sandbox import (
    dynamic_check_matplotlib,
    extract_all_python_blocks,
    extract_main_python_block,
    multi_seed_validate,
    static_check_rational_numpy_mix,
    static_check_unused_random_vars,
)

logger = logging.getLogger(__name__)

TRUNK_RULES = ["2.1", "3.1", "3.2", "6.1", "6.3", "8.1"]


def _translate_constraints_to_assertions(code: str, constraints: list[str],
                                         model_idx: int,
                                         model: str | None = None) -> list[dict]:
    """Mini appel LLM : contrainte FR → expression booléenne Python."""
    if not constraints or not code.strip():
        return []
    try:
        raw = process_with_openrouter(
            prompt=TRANSLATE_CONSTRAINTS_PROMPT.format(
                code=code,
                constraints="\n".join(f"  • {c}" for c in constraints
                                      if isinstance(c, str) and c.strip()),
            ),
            model_idx=model_idx,
            model=model,
            temperature=0.0,
            max_tokens=2048,
            system_prompt=SYSTEM_PROMPT,
        )
    except (RuntimeError, ValueError, OSError) as e:
        logger.warning("Traduction des contraintes en échec : %s", e)
        return []
    try:
        data = json.loads(pp.strip_fences(raw))
    except json.JSONDecodeError:
        logger.warning("Traduction des contraintes : JSON invalide.")
        return []
    if not isinstance(data, list):
        return []
    return [
        {"description": str(d.get("description", "")), "assertion": d.get("assertion")}
        for d in data
        if isinstance(d, dict) and d.get("assertion")
    ]


def _apply_deterministic_nets(candidate: str, decl_type: Optional[str]) -> str:
    """Séquence des filets déterministes appliquée à toute sortie LLM (candidat
    de génération OU de réparation harnais/pédagogique). Idempotente."""
    candidate, _ = pp.fix_orphan_python_openers(candidate)
    candidate = pp.normalize_python_fences(candidate)
    candidate, _ = pp.drop_empty_python_blocks(candidate)
    candidate, _ = pp.fix_triple_braces(candidate)
    candidate, _ = pp.fix_superscript_double_brace(candidate)
    candidate, _ = pp.unwrap_latex_injections(candidate)
    candidate, _ = pp.auto_lift_injections(candidate)
    candidate, _ = pp.rename_underscore_injections(candidate)
    candidate, _ = pp.fix_dollar_digit(candidate)
    if decl_type:
        candidate, _ = pp.fix_mcq_answer_aliases(candidate)
        candidate, _ = pp.merge_decl_python_blocks(candidate)
    if decl_type == "qcm":
        candidate, _ = pp.fix_none_option_last(candidate)
    candidate, _ = pp.aerate_blocks(candidate)
    candidate, _ = pp.renumber_question_ids(candidate)
    return candidate


def run_exercise(
    content: str,
    filename: str = "exercise.md",
    level: str = "",
    model_idx: int = 1,
    lang: str = "fr",
    set_step: Optional[Callable[[str], None]] = None,
    decl_type: Optional[str] = None,
    shared_phase: Optional[tuple] = None,
    forced_models: Optional[dict] = None,
) -> dict:
    """
    Traite UN exercice. `decl_type=None` = pythonisation (flux historique) ;
    `decl_type ∈ {"qcm","qat"}` = mode déclinaisons (même pipeline, prompt et
    harnais étendus). `shared_phase` = résultat de run_analysis_phase à
    RÉUTILISER (déclinaisons QCM+QAT d'une même source : une seule analyse).

    Retourne le dict résultat (contrat UI) :
      exercise, pair_blocks, analysis, functions, notions, audit_patches,
      warnings, harness {ok, summary, seeds}, lang {source, target, action},
      cost {usd, eur, requests}, duration_s [, decl_type]
    """
    t0 = time.time()
    cost_before = cost_snapshot()
    _step = set_step or (lambda label: None)
    # Modèles par rôle (IDs OpenRouter en chaîne), résolus par la policy ;
    # None → comportement legacy (model_idx partout).
    fm = forced_models or {}
    m_gen = fm.get("generate")
    m_audit = fm.get("audit")
    m_meca = fm.get("mecanique")

    # ── 1. Analyse + notions + RAG (parallèle ; partagée en mode QCM+QAT) ────
    if shared_phase is not None:
        analysis, notions_ctx, lists_of_notions, functions_ctx = shared_phase
    else:
        _step("Analyse + notions + catalogue RAG (en parallèle)…")
        analysis, notions_ctx, lists_of_notions, functions_ctx = run_analysis_phase(
            content, model_idx)

    step1_targets = [r for r in (analysis.get("target_rules") or []) if isinstance(r, str)]
    target_rules = list(dict.fromkeys(TRUNK_RULES + step1_targets))
    targeted_rules_digest = build_rules_digest(target_rules) or "(aucune règle spécifique ciblée)"

    constraints = [c for c in (analysis.get("property_constraints") or [])
                   if isinstance(c, str) and c.strip()]
    property_constraints_text = ("\n".join(f"  • {c}" for c in constraints)
                                 if constraints
                                 else "  (aucun invariant explicite — tirages libres)")

    # ── 2. Génération par paires ─────────────────────────────────────────────
    metadata, enonce, question_segments = split_original_questions(content)
    exercise_header = build_exercise_metadata(metadata, lists_of_notions, analysis,
                                              level, decl_type=decl_type)

    # Contexte fonctions = catalogue CURÉ (domaine détecté) + hits RAG FAISS.
    # Le catalogue curé donne « quel helper pour quel besoin » + couvre les
    # domaines absents du corpus livré (matrices, proba, IBP).
    catalogue_ctx = catalogue_for(analysis)
    functions_combined = "\n\n".join(filter(None, [
        catalogue_ctx,
        ("CATALOGUE RAG (hits spécifiques sur le code réel) :\n" + functions_ctx)
        if functions_ctx else "",
    ])) or "Aucune fonction spécifique détectée."

    fewshot = (fewshot_for_declinaison(decl_type) if decl_type
               else fewshot_for(analysis))
    pair_blocks = generate_pair_blocks(
        content=content,
        exercise_header=exercise_header,
        enonce=enonce,
        question_segments=question_segments,
        analysis=analysis,
        functions_ctx=functions_combined,
        fewshot=fewshot,
        targeted_rules_digest=targeted_rules_digest,
        property_constraints_text=property_constraints_text,
        level=level,
        model_idx=model_idx,
        lang=lang,
        set_step=_step,
        decl_type=decl_type,
        model=m_gen,
    )

    # ── 3. Post-traitements déterministes ────────────────────────────────────
    _step("Post-traitements déterministes…")
    pair_blocks = [pp.inject_config_standard_in_pair_block(b) for b in pair_blocks]
    myst_exercise = assemble_exercise(exercise_header, pair_blocks)

    audit_patches: list[dict] = []
    audit_warnings: list[dict] = []

    myst_exercise, orphan_py = pp.fix_orphan_python_openers(myst_exercise)
    if orphan_py:
        audit_patches.append({
            "rule": "3.1", "location": "(orphan python opener)",
            "fix": f"{orphan_py} opener(s) orphelin(s) supprimé(s)",
            "message": f"{orphan_py} fence(s) {{python}} orpheline(s) supprimée(s) (opener doublé).",
            "iteration": 0,
        })
    myst_exercise, dup_q = pp.dedupe_question_blocks(myst_exercise)
    myst_exercise, dup_py = pp.dedupe_python_blocks(myst_exercise)
    myst_exercise, empty_py = pp.drop_empty_python_blocks(myst_exercise)
    if empty_py:
        audit_patches.append({
            "rule": "3.1", "location": "(empty python blocks)",
            "fix": f"{empty_py} bloc(s) vide(s) supprimé(s)",
            "message": f"{empty_py} bloc(s) {{python}} vide(s) (globals() seul) supprimé(s).",
            "iteration": 0,
        })
    if dup_q:
        audit_patches.append({
            "rule": "9.4", "location": "(duplicate question blocks)",
            "fix": f"{dup_q} bloc(s) dédupliqué(s)",
            "message": f"{dup_q} `:::::{{question}}` redondant(s) supprimé(s).",
            "iteration": 0,
        })
    if dup_py:
        audit_patches.append({
            "rule": "3.1", "location": "(duplicate python blocks)",
            "fix": f"{dup_py} bloc(s) dédupliqué(s)",
            "message": f"{dup_py} bloc(s) {{python}} redondant(s) supprimé(s).",
            "iteration": 0,
        })

    # ── 4. Solutions validées (règle 8.1) ────────────────────────────────────
    if analysis.get("has_validated_solution_in_input"):
        _step("Substitution déterministe des solutions validées…")
        myst_exercise, sol_patches = replace_gen_solutions_with_source(
            myst_exercise, content, analysis, model_idx, model=m_meca)
        audit_patches.extend(sol_patches)

    # ── 5. Audit LLM ─────────────────────────────────────────────────────────
    myst_exercise, llm_patches, llm_warnings = run_audit(
        myst_exercise, step1_targets, model_idx, set_step=_step, model=m_audit)
    audit_patches.extend(llm_patches)
    audit_warnings.extend(llm_warnings)

    # ── 6. Filets déterministes finaux ───────────────────────────────────────
    _step("Filets déterministes (injections, $, id, décimales)…")
    myst_exercise, brace_patches = pp.fix_triple_braces(myst_exercise)
    audit_patches.extend(brace_patches)

    myst_exercise, sup_fixed = pp.fix_superscript_double_brace(myst_exercise)
    if sup_fixed:
        audit_patches.append({
            "rule": "6.1", "location": "^{{\\latex / _{{\\latex",
            "fix": "^{ {\\latex / _{ {\\latex",
            "message": f"{sup_fixed} double-accolade de superscript/indice désambiguïsée(s) (espace inséré).",
            "iteration": 0,
        })

    myst_exercise, unwrapped = pp.unwrap_latex_injections(myst_exercise)
    if unwrapped:
        audit_patches.append({
            "rule": "6.1", "location": "{{ \\latex … }}",
            "fix": f"{unwrapped} enveloppe(s) {{{{ }}}} externe(s) retirée(s)",
            "message": f"{unwrapped} injection(s) enveloppant du LaTeX déballée(s) (l'injection interne est la vraie).",
            "iteration": 0,
        })

    myst_exercise, lift_patches = pp.auto_lift_injections(myst_exercise)
    audit_patches.extend(lift_patches)

    myst_exercise, rename_patches = pp.rename_underscore_injections(myst_exercise)
    audit_patches.extend(rename_patches)

    myst_exercise, dollar_patches = pp.fix_dollar_digit(myst_exercise)
    audit_patches.extend(dollar_patches)

    if decl_type:
        # Filet : alias d'option MCQ mal nommés / :isRightAnswer: manquant
        # (le repli MCQ en QAT est concerné aussi).
        myst_exercise, alias_fixed = pp.fix_mcq_answer_aliases(myst_exercise)
        if alias_fixed:
            audit_patches.append({
                "rule": "MCQ", "location": "(mcqOption / :isRightAnswer:)",
                "fix": f"{alias_fixed} bloc(s) d'option normalisé(s)",
                "message": "Blocs d'options MCQ normalisés (mcqOption→mcqAnswer, :isRightAnswer: false par défaut).",
                "iteration": 0,
            })
        # Déclinaisons : UN SEUL bloc {python} — fusion des blocs additionnels
        # sans re-tirage (re-tirage → laissé au harnais + réparation LLM).
        myst_exercise, merged = pp.merge_decl_python_blocks(myst_exercise)
        if merged:
            audit_patches.append({
                "rule": "3.1", "location": "(blocs python additionnels)",
                "fix": f"{merged} bloc(s) fusionné(s) dans le bloc principal",
                "message": "Déclinaison : blocs {python} additionnels fusionnés (un seul bloc, spec).",
                "iteration": 0,
            })

    if decl_type == "qcm":
        # Filet MCQ : l'option « None/Aucune » doit être le dernier mcqAnswer.
        myst_exercise, none_moved = pp.fix_none_option_last(myst_exercise)
        if none_moved:
            audit_patches.append({
                "rule": "MCQ", "location": "(option None)",
                "fix": f"{none_moved} option(s) « None » déplacée(s) en dernier",
                "message": "Option « Aucune de ces réponses / None » repositionnée en dernière position.",
                "iteration": 0,
            })

    # Les warnings 6.1 du LLM deviennent du bruit une fois l'auto-lift passé.
    if not pp.INJECTION_RE.search(myst_exercise) or not any(
        "(" in tok or "**" in tok for tok in pp.INJECTION_RE.findall(myst_exercise)
    ):
        audit_warnings = [w for w in audit_warnings
                          if not (isinstance(w, dict) and w.get("rule") == "6.1")]

    myst_exercise, id_patched = pp.force_empty_id(myst_exercise)
    if id_patched and not any(p.get("rule") == "2.1" for p in audit_patches):
        audit_patches.append({
            "rule": "2.1", "location": "(metadata header)", "fix": ":id:",
            "message": "ID vidé par post-process déterministe.", "iteration": 0,
        })

    audit_warnings.extend(pp.diff_solutions(content, myst_exercise))
    audit_warnings.extend(pp.check_hardcoded_decimals_in_solutions(myst_exercise))

    # Invariants multi-seed (règle 4.3).
    main_code = extract_main_python_block(myst_exercise)
    if constraints and main_code:
        _step("Validation multi-seed des invariants…")
        assertions = _translate_constraints_to_assertions(main_code, constraints, model_idx, model=m_meca)
        if assertions:
            seed_report = multi_seed_validate(
                main_code, assertions, num_seeds=MULTI_SEED_NUM, timeout_per_seed=3.0)
            if seed_report["num_exec_errors"] > 0:
                audit_warnings.append({
                    "rule": "4.3",
                    "message": (f"Bloc Python : {seed_report['num_exec_errors']}/{MULTI_SEED_NUM} "
                                f"exécutions ont échoué. Première erreur : "
                                f"{seed_report.get('first_exec_error') or '?'}."),
                })
            for a in assertions:
                summary = seed_report["summary_per_assertion"].get(a["assertion"], {})
                viol = summary.get("violations", 0) + summary.get("errors", 0)
                if viol:
                    audit_warnings.append({
                        "rule": "4.3",
                        "message": (f"Invariant « {a['description']} » violé sur "
                                    f"{viol}/{MULTI_SEED_NUM} seeds. "
                                    f"Assertion : `{a['assertion']}`."),
                    })

    # Contrôles matplotlib (règles 11.x).
    if main_code:
        all_python_code = "\n".join(extract_all_python_blocks(myst_exercise))
        audit_warnings.extend(static_check_rational_numpy_mix(all_python_code))
        if "matplotlib" in all_python_code or analysis.get("needs_matplotlib"):
            random_var_names = [v.get("nom") for v in (analysis.get("variables") or [])
                                if isinstance(v, dict) and isinstance(v.get("nom"), str)]
            unused = static_check_unused_random_vars(
                all_python_code, random_var_names, markdown_text=myst_exercise)
            if unused:
                audit_warnings.append({
                    "rule": "11.1",
                    "message": ("Variables aléatoires non utilisées dans le tracé : "
                                f"{', '.join(unused)}."),
                })
            _step("Validation matplotlib (labels in-bounds)…")
            try:
                audit_warnings.extend(dynamic_check_matplotlib(all_python_code, timeout=8.0))
            except Exception as e:
                audit_warnings.append({
                    "rule": "11.3",
                    "message": f"Audit matplotlib impossible : {type(e).__name__}: {e}.",
                })

    # ── 7. Langue cible ──────────────────────────────────────────────────────
    _step("Langue cible…")
    myst_exercise, lang_warnings, lang_info = ensure_language(myst_exercise, lang, model_idx, model=m_meca)
    audit_warnings.extend(lang_warnings)
    effective_lang = lang if lang_info["action"] != "aucune" else lang_info["source"]
    audit_warnings.extend(pp.check_decimals_for_lang(myst_exercise, effective_lang))

    # ── 8. Porte harnais + réparation ────────────────────────────────────────
    myst_exercise, _aer = pp.aerate_blocks(myst_exercise)   # lisibilité (exemples)
    myst_exercise, renum = pp.renumber_question_ids(myst_exercise)
    if renum:
        audit_patches.append({
            "rule": "2.x", "location": ":questionId:/:questionIndex:",
            "fix": "renumérotation 0..N-1",
            "message": f"{renum} questionId/questionIndex renuméroté(s) (contiguïté plateforme).",
            "iteration": 0,
        })
    _step(f"Porte harnais ({HARNESS_GATE_SEEDS} graines)…")
    report = harness.validate_text(myst_exercise, seeds=HARNESS_GATE_SEEDS)

    for attempt in range(HARNESS_REPAIR_MAX):
        if report["ok"]:
            break
        _step(f"Harnais ROUGE — réparation LLM {attempt + 1}/{HARNESS_REPAIR_MAX}…")
        try:
            repaired = process_with_openrouter(
                prompt=REPAIR_PROMPT.format(
                    failures=harness.format_report(report),
                    exercise=myst_exercise,
                ),
                model_idx=model_idx,
                model=m_gen,
                temperature=0.0,
                max_tokens=30000,
                system_prompt=SYSTEM_PROMPT,
            )
        except (RuntimeError, ValueError, OSError) as e:
            audit_warnings.append({"rule": "harnais",
                                   "message": f"Réparation LLM en échec : {e}."})
            break
        # Re-passe des filets déterministes sur le candidat réparé.
        candidate = _apply_deterministic_nets(pp.strip_fences(repaired), decl_type)
        candidate_report = harness.validate_text(candidate, seeds=HARNESS_GATE_SEEDS)

        def _badness(r: dict) -> int:
            return (len(r["static_errors"]) + r["n_exec_errors"]
                    + r["n_unresolved"] + r["n_forbidden"]
                    + r.get("n_mcq_collisions", 0))

        if candidate_report["ok"] or _badness(candidate_report) < _badness(report):
            myst_exercise, report = candidate, candidate_report
            audit_patches.append({
                "rule": "harnais", "location": "(exercice complet)",
                "fix": "réparation LLM post-harnais",
                "message": "Sortie réparée suite au verdict rouge du harnais.",
                "iteration": attempt + 1,
            })

    if not report["ok"]:
        audit_warnings.append({
            "rule": "harnais",
            "message": ("⚠️ SORTIE NON VERTE AU HARNAIS — à corriger avant soumission. "
                        + harness.format_report(report)[:600]),
        })

    # ── 9. Audit pédagogique (déclinaisons, sortie VERTE) ────────────────────
    # Au-delà du harnais MÉCANIQUE : un juge LLM évalue la finesse pédagogique et
    # le respect des consignes (distracteurs cohérents, indevinabilité…), puis
    # une réparation ciblée qui ne doit JAMAIS casser le harnais.
    pedagogical = None
    if decl_type and PEDAGO_AUDIT_ENABLED and report["ok"]:
        _step("Audit pédagogique (finesse + respect des consignes)…")
        # Juge sur son modèle dédié (PEDAGO_AUDIT_MODEL) — constant entre échelons,
        # fort + JSON fiable, indépendant du modèle de génération qui escalade.
        pedagogical = run_pedagogical_audit(myst_exercise, decl_type)
        for attempt in range(PEDAGO_REPAIR_MAX):
            if pedagogical.get("verdict") != "A_REVOIR" or not pedagogical.get("issues"):
                break
            _step(f"Réparation pédagogique {attempt + 1}/{PEDAGO_REPAIR_MAX}…")
            try:
                repaired = process_with_openrouter(
                    prompt=PEDAGOGICAL_REPAIR_PROMPT.format(
                        decl_label="QCM (MCQ)" if decl_type == "qcm" else "QAT (FGQ)",
                        issues=format_pedagogical_issues(pedagogical["issues"]),
                        exercise=myst_exercise,
                    ),
                    model=m_gen, temperature=0.0, max_tokens=30000,
                    system_prompt=SYSTEM_PROMPT,
                )
            except (RuntimeError, ValueError, OSError) as e:
                audit_warnings.append({"rule": "pédagogie",
                                       "message": f"Réparation pédagogique en échec : {e}."})
                break
            cand = _apply_deterministic_nets(pp.strip_fences(repaired), decl_type)
            cand_report = harness.validate_text(cand, seeds=HARNESS_GATE_SEEDS)
            if not cand_report["ok"]:
                audit_warnings.append({"rule": "pédagogie",
                    "message": "Réparation pédagogique rejetée (casserait le harnais) "
                               "— version précédente conservée."})
                break
            new_ped = run_pedagogical_audit(cand, decl_type)
            if pedagogical_badness(new_ped) < pedagogical_badness(pedagogical):
                myst_exercise, report, pedagogical = cand, cand_report, new_ped
                audit_patches.append({"rule": "pédagogie", "location": "(exercice complet)",
                    "fix": "réparation pédagogique LLM",
                    "message": "Distracteurs/consignes améliorés suite à l'audit pédagogique.",
                    "iteration": attempt + 1})
            else:
                break                     # n'améliore pas → on garde l'existant
        if pedagogical.get("verdict") == "A_REVOIR":
            audit_warnings.append({"rule": "pédagogie",
                "message": "⚠️ QUALITÉ PÉDAGOGIQUE à revoir : "
                           + format_pedagogical_issues(pedagogical.get("issues") or [])[:500]})

    # ── Résultat ─────────────────────────────────────────────────────────────
    return {
        "exercise": myst_exercise,
        "pair_blocks": pair_blocks,
        "analysis": analysis,
        "functions": functions_ctx,
        "notions": (notions_ctx + "\n" + lists_of_notions).strip(),
        "audit_patches": audit_patches,
        "warnings": audit_warnings,
        "harness": {
            "ok": report["ok"],
            "seeds": report["seeds"],
            "summary": harness.format_report(report),
        },
        "pedagogical": pedagogical,
        "lang": lang_info,
        "decl_type": decl_type,
        "model_used": m_gen,
        "cost": cost_delta(cost_before),
        "duration_s": round(time.time() - t0, 1),
    }


def run_with_policy(
    content: str,
    filename: str = "exercise.md",
    level: str = "",
    lang: str = "fr",
    policy: str = "auto",
    manual_models: Optional[dict] = None,
    decl_type: Optional[str] = None,
    shared_phase: Optional[tuple] = None,
    set_step: Optional[Callable[[str], None]] = None,
) -> dict:
    """
    Traite UN exercice sous POLITIQUE de sélection de modèle (§5) :
      auto  : pré-classifieur de difficulté → départ sur l'échelle `auto` ;
              génération → harnais → ≤HARNESS_REPAIR_MAX réparations (même
              modèle) → si toujours ROUGE, ESCALADE d'un échelon et retente
              (analyse/RAG PARTAGÉS entre tentatives) → si `best` échoue,
              marque l'exo pour revue humaine.
      best / cheap / manual : un seul échelon (le modèle du preset).
    Télémétrie dans result["policy_telemetry"].
    """
    from app.models import policy as mp

    _step = set_step or (lambda label: None)
    manual = manual_models or {}
    m_audit = mp.openrouter_id(mp.resolve("audit", policy, manual))
    m_meca = mp.openrouter_id(mp.resolve("mecanique", policy, manual))

    cost_before_all = cost_snapshot()   # coût HONNÊTE : analyse + tous échelons
    difficulty = mp.classify_difficulty(content)
    if policy == "auto":
        steps = mp.ladder("generate")
        start = mp.start_rung("generate", difficulty)
        rungs = steps[start:start + MAX_ESCALADES + 1] or steps[-1:]
    else:
        rungs = [mp.resolve("generate", policy, manual)]
    if not rungs:
        raise RuntimeError("Aucun modèle utilisable pour le rôle generate "
                           "(clés API absentes) — vérifier OPENROUTER_API_KEY.")

    shared = shared_phase
    if shared is None:
        _step("Analyse + notions + catalogue RAG (en parallèle)…")
        shared = run_analysis_phase(content, 0, model=m_meca)

    tried: list[dict] = []
    result: dict = {}
    key = rungs[0]
    for i, key in enumerate(rungs):
        _step(f"Échelon {i + 1}/{len(rungs)} — {key}…")
        result = run_exercise(
            content=content, filename=filename, level=level,
            lang=lang, set_step=_step, decl_type=decl_type,
            shared_phase=shared,
            forced_models={"generate": mp.openrouter_id(key),
                           "audit": m_audit, "mecanique": m_meca},
        )
        harness_ok = result["harness"]["ok"]
        ped = result.get("pedagogical") or {}
        ped_verdict = ped.get("verdict")            # OK / A_REVOIR / INCONNU / None
        tried.append({"rung": i, "model": key, "ok": harness_ok,
                      "pedago": ped_verdict})
        is_last = (i == len(rungs) - 1)
        # Acceptation d'un échelon : harnais VERT ET (qualité pédagogique OK, ou
        # on n'escalade pas sur la pédagogie, ou dernier échelon). Sinon on
        # gravit l'échelon suivant — c'est le « meilleur modèle selon l'exo ».
        pedago_ok = ped_verdict != "A_REVOIR"
        escalate_pedago = (policy == "auto" and PEDAGO_ESCALATE_IN_AUTO
                           and not pedago_ok and not is_last)
        if harness_ok and not escalate_pedago:
            break
        if not harness_ok:
            logger.info("Échelon %s ROUGE (harnais) sur %s — escalade.", key, filename)
        else:
            logger.info("Échelon %s VERT mais qualité pédagogique à revoir sur %s "
                        "— escalade de modèle.", key, filename)

    result["policy_telemetry"] = {
        "mode": policy,
        "difficulty": difficulty,
        "tried": tried,
        "winning_model": key,
        "pedago_verdict": (result.get("pedagogical") or {}).get("verdict"),
        "needs_review": (not result["harness"]["ok"]
                         or (result.get("pedagogical") or {}).get("verdict") == "A_REVOIR"),
    }
    # Coût honnête : inclut l'analyse partagée (si calculée ici) ET les
    # échelons perdants — pas seulement la tentative gagnante.
    result["cost"] = cost_delta(cost_before_all)
    return result


def run_declinaisons(
    content: str,
    filename: str = "exercise.md",
    level: str = "",
    model_idx: int = 1,
    lang: str = "fr",
    types: Optional[list] = None,
    set_step: Optional[Callable[[str], None]] = None,
    policy: str = "auto",
    manual_models: Optional[dict] = None,
) -> list[tuple[str, dict]]:
    """
    Mode `declinaisons` : produit une déclinaison par type coché (qcm/qat),
    sous politique de sélection de modèle. L'analyse + notions + RAG sont
    calculées UNE SEULE fois et partagées entre les types ET les échelons
    (aucun appel LLM redondant). Retourne [(decl_type, result), …].
    """
    from app.models import policy as mp

    _step = set_step or (lambda label: None)
    types = [t for t in (types or []) if t in ("qcm", "qat")] or ["qcm"]

    m_meca = mp.openrouter_id(mp.resolve("mecanique", policy, manual_models))
    _step("Analyse + notions + catalogue RAG (partagés QCM/QAT)…")
    cost_before_analysis = cost_snapshot()
    shared = run_analysis_phase(content, model_idx, model=m_meca)
    analysis_cost = cost_delta(cost_before_analysis)

    out: list[tuple[str, dict]] = []
    for decl_type in types:
        label = "QCM" if decl_type == "qcm" else "QAT"

        def step_with_type(msg: str, _label=label):
            _step(f"[{_label}] {msg}")

        result = run_with_policy(
            content=content,
            filename=filename,
            level=level,
            lang=lang,
            policy=policy,
            manual_models=manual_models,
            decl_type=decl_type,
            shared_phase=shared,
            set_step=step_with_type,
        )
        out.append((decl_type, result))
    # L'analyse partagée tombe HORS des fenêtres de coût de run_with_policy :
    # on l'impute au premier type pour que le total du job reste honnête.
    if out and analysis_cost["requests"]:
        c = out[0][1].get("cost") or {"usd": 0.0, "eur": 0.0, "requests": 0}
        out[0][1]["cost"] = {
            "usd": round(c["usd"] + analysis_cost["usd"], 6),
            "eur": round(c["eur"] + analysis_cost["eur"], 6),
            "requests": c["requests"] + analysis_cost["requests"],
        }
    return out
