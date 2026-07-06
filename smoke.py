"""
Smoke tests minimaux — AUCUN appel réseau (LLM mocké), exécution :

    .venv/bin/python tests/smoke.py

Couvre : import/create_app, /health, 1 run de pipeline complet (mock LLM)
avec porte harnais VERTE, et les filets déterministes clés.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

PASS = []


def check(name, cond):
    PASS.append((name, bool(cond)))
    print(("✓" if cond else "✗"), name)


# ── 1. Import + /health ──────────────────────────────────────────────────────
from app import create_app  # noqa: E402

flask_app = create_app()
client = flask_app.test_client()
health = client.get("/health").get_json()
check("create_app + /health", health and health["status"] == "ok")
models = client.get("/api/models").get_json()
check("/api/models expose le roster", len(models["models"]) >= 5)

# ── 2. Filets déterministes ──────────────────────────────────────────────────
from app.pipeline import postprocess as pp  # noqa: E402

t, _ = pp.fix_dollar_digit("Prix : $3$ et ${{nAff}}$.")
check("fix_dollar_digit", "${}3$" in t and "${}{{nAff}}$" in t)
check("detect_languages both", pp.detect_languages("{fr}`Calculer`{en}`Compute` $x$") == "both")
check("strip_language fr", pp.strip_language("{fr}`Bonjour `{en}`Hello `", "fr").strip() == "Bonjour")

# ── 3. Pipeline complet avec LLM mocké ───────────────────────────────────────
SMOKE_SOURCE = """`````{exercise}
:title: Somme de deux entiers
:level: Elementary

On additionne deux entiers.

:::::{question}
:questionType: STQ
:questionId: 0
:questionIndex: 0

::::{questionStatement}
Calculer $3 + 4$.
::::

::::{questionHint}
Poser l'addition.
::::

::::{detailedSolution}
On trouve $7$.
::::

::::{weightDistribution}
:logic: 25
:abstraction: 25
:reasoning: 25
:calculation: 25
::::
:::::
`````"""

MOCK_ANALYSIS = json.dumps({
    "exercise_type": "équation linéaire",
    "exercise_title": "Somme de deux entiers",
    "nb_questions": 1,
    "variables": [{"nom": "a", "type_python": "int", "description": "1er terme",
                   "contraintes": "2..9", "plage_python": "rd.randint(2, 9)",
                   "location": "énoncé", "valeur_exemple": "3"}],
    "needs_fraction": False, "needs_sympy": False, "needs_numpy": False,
    "needs_matplolib": False,   # typo v1 volontaire : doit être normalisée
    "target_rules": [], "property_constraints": [],
    "has_validated_solution_in_input": False,
})

MOCK_PAIR = """````{python}
import random as rd
a = rd.randint(2, 9)
b = rd.randint(2, 9)
sumAff = str(a + b)
globals()
````

On additionne deux entiers.

:::::{question}
:questionType: STQ
:questionId: 0
:questionIndex: 0

::::{questionStatement}
Calculer ${}{{a}} + {{b}}$.
::::

::::{questionHint}
Poser l'addition.
::::

::::{detailedSolution}
On trouve ${}{{a}} + {{b}} = {{sumAff}}$.
::::

::::{weightDistribution}
:logic: 25
:abstraction: 25
:reasoning: 25
:calculation: 25
::::
:::::"""


MOCK_MCQ_PAIR = """````{python}
import random as rd
a = rd.randint(2, 9)
b = rd.randint(2, 9)
sumAff = str(a + b)
d1Aff = str(a + b + 1)      # erreur type : +1
d2Aff = str(a + b - 1)      # erreur type : -1
d3Aff = str(a * b + 100)    # produit décalé — toujours > somme+1 (distinct)
globals()
````

On additionne deux entiers.

:::::{question}
:questionType: MCQ
:questionId: 0
:questionIndex: 0

::::{questionStatement}
Combien vaut ${}{{a}} + {{b}}$ ?
::::

::::{questionHint}
Poser l'addition.
::::

::::{mcqAnswer}
:isRightAnswer: true
${}{{sumAff}}$
::::

::::{mcqAnswer}
:isRightAnswer: false
${}{{d1Aff}}$
::::

::::{mcqAnswer}
:isRightAnswer: false
${}{{d2Aff}}$
::::

::::{mcqAnswer}
:isRightAnswer: false
${}{{d3Aff}}$
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Aucune de ces réponses n'est correcte`{en}`None of these answers are correct`
::::

::::{detailedSolution}
On trouve ${}{{a}} + {{b}} = {{sumAff}}$.
::::

::::{weightDistribution}
:logic: 25
:abstraction: 25
:reasoning: 25
:calculation: 25
::::
:::::"""

MOCK_FGQ_PAIR = """````{python}
import random as rd
a = rd.randint(2, 9)
b = rd.randint(2, 9)
sumAff = str(a + b)
globals()
````

On additionne deux entiers.

:::::{question}
:questionType: FGQ
:questionId: 0
:questionIndex: 0
:solution: [["ord","${{sumAff}}$"],["0"]]

::::{questionStatement}
Calculer ${}{{a}} + {{b}}$.

$s =$ {input}`||110`
::::

::::{questionHint}
Poser l'addition.
::::

::::{displayedSolution}
$s = {{sumAff}}$
::::

::::{detailedSolution}
On trouve ${}{{a}} + {{b}} = {{sumAff}}$.
::::

::::{weightDistribution}
:logic: 15
:abstraction: 20
:reasoning: 20
:calculation: 45
::::
:::::"""

ANALYSIS_CALLS = {"n": 0}


GEN_MODELS_SEEN = []          # IDs de modèle vus par les appels de génération


def mock_llm(prompt, model_idx=0, temperature=0.0, max_tokens=4096,
             image_b64=None, system_prompt="", reasoning=False, model=None):
    if "expert en analyse d'exercices" in prompt:
        ANALYSIS_CALLS["n"] += 1
        return MOCK_ANALYSIS
    if "auditeur PyxiScience" in prompt:
        return json.dumps({"verdict": "OK", "issues": []})
    if "RELECTEUR PÉDAGOGIQUE" in prompt:            # audit pédagogique
        PEDAGO_CALLS["n"] += 1
        return json.dumps({"verdict": "OK", "score": 95, "issues": []})
    if "Tu déclines un exercice" in prompt:
        GEN_MODELS_SEEN.append(model)
        return MOCK_MCQ_PAIR if "QCM (MCQ)" in prompt else MOCK_FGQ_PAIR
    if "RÈGLES D'ASSEMBLAGE PAR PAIRE" in prompt:
        GEN_MODELS_SEEN.append(model)
        return MOCK_PAIR
    return "{}"


PEDAGO_CALLS = {"n": 0}


import app.pipeline.analyze as analyze  # noqa: E402
import app.pipeline.audit as audit  # noqa: E402
import app.pipeline.generate as generate  # noqa: E402
import app.pipeline.orchestrator as orchestrator  # noqa: E402

analyze.process_with_openrouter = mock_llm
audit.process_with_openrouter = mock_llm
generate.process_with_openrouter = mock_llm
orchestrator.process_with_openrouter = mock_llm
analyze.enrich_exercise_with_notions = lambda *a, **k: ("(notions mockées)", "NOTION_TEST")
analyze.retrieve_functions_context = lambda **k: {"catalogue": "(catalogue mocké)"}

result = orchestrator.run_exercise(
    content=SMOKE_SOURCE, filename="smoke.md", level="", model_idx=0, lang="fr")

check("pipeline : exercice produit", bool(result["exercise"].strip()))
check("pipeline : fence 4 backticks", "````{python}" in result["exercise"])
check("pipeline : se termine par `````", result["exercise"].rstrip().endswith("`````"))
check("pipeline : globals() présent", "globals()" in result["exercise"])
check("pipeline : typo needs_matplolib normalisée",
      "needs_matplolib" not in result["analysis"] and result["analysis"]["needs_matplotlib"] is False)
check("pipeline : harnais VERT", result["harness"]["ok"])
check("pipeline : coût exposé", "usd" in result["cost"])
check("pipeline : langue exposée", result["lang"]["target"] == "fr")

# En-tête {exercise} complet et bien formé
ex = result["exercise"]
check("header : enveloppe `````{exercise} en tête", ex.lstrip().startswith("`````{exercise}"))
for field in (":id:", ":title:", ":modules:", ":recommendedExecutionTime:",
              ":level:", ":chap:", ":involvedConcepts:", ":originalSource:", ":visibility:"):
    check(f"header : champ {field} présent", field in ex.split("````{python}")[0])
check("header : level mappé (level='' → Elementary)", ":level: Elementary" in ex)
check("header : visibility All", ":visibility: All" in ex)
check("header : concepts = notions", "NOTION_TEST" in ex)
check("header : une seule enveloppe {exercise}", ex.count("`````{exercise}") == 1)

# ── 3bis. Mode déclinaisons (QCM + QAT, LLM mocké, analyse partagée) ─────────
ANALYSIS_CALLS["n"] = 0
PEDAGO_CALLS["n"] = 0
decl_results = orchestrator.run_declinaisons(
    content=SMOKE_SOURCE, filename="smoke.md", level="", model_idx=0,
    lang="fr", types=["qcm", "qat"])
check("déclinaisons : 2 sorties (QCM + QAT)", len(decl_results) == 2)
check("déclinaisons : analyse partagée (1 seul appel)", ANALYSIS_CALLS["n"] == 1)
check("audit pédagogique : appelé (QCM + QAT)", PEDAGO_CALLS["n"] >= 2)

qcm = dict(decl_results)["qcm"]
qat = dict(decl_results)["qat"]
check("QCM : harnais VERT", qcm["harness"]["ok"])
check("QCM : 5 options, 1 seule bonne", qcm["exercise"].count("{mcqAnswer}") == 5
      and qcm["exercise"].count(":isRightAnswer: true") == 1)
check("QCM : « None » en dernière option",
      "Aucune de ces réponses" in qcm["exercise"].split(":isRightAnswer: false")[-1])
check("QCM : titre suffixé - MCQ", " - MCQ" in qcm["exercise"].split("````{python}")[0])
check("QAT : harnais VERT", qat["harness"]["ok"])
check("QAT : :solution: + {input} présents",
      ':solution: [["ord"' in qat["exercise"] and "{input}`" in qat["exercise"])
check("QAT : displayedSolution présent", "{displayedSolution}" in qat["exercise"])
check("déclinaisons : decl_type exposé", qcm["decl_type"] == "qcm" and qat["decl_type"] == "qat")
check("audit pédagogique : verdict exposé (QCM)",
      isinstance(qcm.get("pedagogical"), dict) and qcm["pedagogical"]["verdict"] == "OK")

# Audit pédagogique ROUGE → escalade en mode auto (harnais VERT mais qualité A_REVOIR).
_ped_calls = {"n": 0}


def mock_llm_pedago_escalade(prompt, model_idx=0, temperature=0.0, max_tokens=4096,
                             image_b64=None, system_prompt="", reasoning=False, model=None):
    if "expert en analyse d'exercices" in prompt:
        return MOCK_ANALYSIS
    if "auditeur PyxiScience" in prompt:
        return json.dumps({"verdict": "OK", "issues": []})
    if "RELECTEUR PÉDAGOGIQUE" in prompt:
        _ped_calls["n"] += 1
        # Échelon 1 : audit + post-réparation restent A_REVOIR (2 appels) → la
        # réparation n'améliore pas, donc ESCALADE. Échelon 2+ : qualité OK.
        if _ped_calls["n"] <= 2:
            return json.dumps({"verdict": "A_REVOIR", "score": 40, "issues": [
                {"gravite": "haute", "ou": "Q0", "probleme": "distracteur devinable",
                 "correction": "grille miroir"}]})
        return json.dumps({"verdict": "OK", "score": 92, "issues": []})
    if "défauts de QUALITÉ" in prompt:            # réparation pédagogique → sortie VERTE mais non améliorée
        return MOCK_MCQ_PAIR
    if "Tu déclines un exercice" in prompt or "RÈGLES D'ASSEMBLAGE PAR PAIRE" in prompt:
        return MOCK_MCQ_PAIR
    return "{}"


for _m in (analyze, audit, generate, orchestrator):
    _m.process_with_openrouter = mock_llm_pedago_escalade
_sols_p = __import__("app.pipeline.solutions", fromlist=["x"])
_tr_p = __import__("app.pipeline.translate", fromlist=["x"])
_sols_p.process_with_openrouter = mock_llm_pedago_escalade
_tr_p.process_with_openrouter = mock_llm_pedago_escalade

res_ped = orchestrator.run_with_policy(
    content=SMOKE_SOURCE, filename="ped.md", lang="fr", policy="auto", decl_type="qcm")
tel_ped = res_ped["policy_telemetry"]
check("escalade pédagogique : ≥2 échelons tentés", len(tel_ped["tried"]) >= 2)
check("escalade pédagogique : 1er échelon qualité A_REVOIR",
      tel_ped["tried"][0]["pedago"] == "A_REVOIR")
check("escalade pédagogique : gagnant qualité OK",
      tel_ped["pedago_verdict"] == "OK" and not tel_ped["needs_review"])

for _m in (analyze, audit, generate, orchestrator):
    _m.process_with_openrouter = mock_llm
_sols_p.process_with_openrouter = mock_llm
_tr_p.process_with_openrouter = mock_llm

# Harnais étendu : un MCQ avec collision d'options doit être ROUGE.
from app.validation import harness as _harness  # noqa: E402

_collision = qcm["exercise"].replace("{{d1Aff}}", "{{sumAff}}")   # distracteur == bonne réponse
_rep = _harness.validate_text(_collision, seeds=10)
check("harnais étendu : collision d'options MCQ détectée (ROUGE)",
      not _rep["ok"] and _rep["n_mcq_collisions"] > 0)
_two_true = qcm["exercise"].replace(":isRightAnswer: false", ":isRightAnswer: true", 1)
_rep2 = _harness.validate_text(_two_true, seeds=5)
check("harnais étendu : 2 bonnes réponses détectées (statique)",
      not _rep2["ok"] and any("isRightAnswer" in e for e in _rep2["static_errors"]))
_bad_arity = qat["exercise"].replace('[["ord","${{sumAff}}$"],["0"]]',
                                     '[["ord","${{sumAff}}$","$2$"],["0","0"]]')
_rep3 = _harness.validate_text(_bad_arity, seeds=5)
check("harnais étendu : arité FGQ incohérente détectée",
      not _rep3["ok"] and any("arité" in e for e in _rep3["static_errors"]))

# Validation API du mode (sans lancer de job).
r_bad_mode = client.post("/api/jobs", json={"content": "x", "mode": "zzz"})
check("API : mode invalide → 400", r_bad_mode.status_code == 400)
r_no_types = client.post("/api/jobs", json={"content": "x", "mode": "declinaisons", "types": {}})
check("API : declinaisons sans type → 400", r_no_types.status_code == 400)

# ── 3ter. Politiques de modèle + escalade + retrait de Fable ────────────────
from app.models.catalog import CATALOG, CANDIDATES  # noqa: E402
from app.models import policy as _mp  # noqa: E402

check("Fable absent du catalogue",
      not any("fable" in k.lower() for k in CATALOG)
      and not any("fable" in v["openrouter_id"].lower() for v in CATALOG.values()))
from app.config import AVAILABLE_MODELS as _AM  # noqa: E402
check("Fable absent d'AVAILABLE_MODELS",
      not any("fable" in v.lower() for v in _AM.values()))
check("Fable absent du fallback policy",
      not any("fable" in str(_mp.DEFAULT_RECOMMENDED).lower() for _ in [0]))

# best / cheap / manual suivent recommended.json (source VIVANTE : le banc la
# réécrit — on vérifie la cohérence de la résolution, pas des noms figés).
_rec_gen = _mp.load_recommended()["generate"]
check("policy best suit recommended.json",
      _mp.resolve("generate", "best") == _rec_gen["best"])
check("policy cheap suit recommended.json",
      _mp.resolve("generate", "cheap") == _rec_gen["cheap"])
check("policy manual respecté",
      _mp.resolve("generate", "manual", {"generate": "deepseek-v4-pro"}) == "deepseek-v4-pro")
check("difficulté : matrices → difficile",
      _mp.classify_difficulty("Matrix systeme " * 100 + ":::::{question}" * 6) == "difficile")

# Escalade : 1er échelon forcé ROUGE (options en collision) → échelon 2 VERT.
MOCK_MCQ_RED = MOCK_MCQ_PAIR.replace("{{d1Aff}}", "{{sumAff}}")
_calls = {"n": 0}


def mock_llm_escalade(prompt, model_idx=0, temperature=0.0, max_tokens=4096,
                      image_b64=None, system_prompt="", reasoning=False, model=None):
    if "expert en analyse d'exercices" in prompt:
        return MOCK_ANALYSIS
    if "auditeur PyxiScience" in prompt:
        return json.dumps({"verdict": "OK", "issues": []})
    if "RELECTEUR PÉDAGOGIQUE" in prompt:   # qualité OK → escalade pilotée par le harnais seul
        return json.dumps({"verdict": "OK", "score": 95, "issues": []})
    if "harnais" in prompt and "REJETÉ" in prompt:
        return MOCK_MCQ_RED          # la réparation échoue aussi sur l'échelon 1
    if "Tu déclines un exercice" in prompt or "RÈGLES D'ASSEMBLAGE PAR PAIRE" in prompt:
        _calls["n"] += 1
        # 1re GÉNÉRATION (échelon 1) rouge ; la suivante (échelon 2) verte.
        return MOCK_MCQ_RED if _calls["n"] <= 1 else MOCK_MCQ_PAIR
    return "{}"


for _m in (analyze, audit, generate, orchestrator):
    _m.process_with_openrouter = mock_llm_escalade
import app.pipeline.solutions as _sols  # noqa: E402
import app.pipeline.translate as _tr  # noqa: E402
_sols.process_with_openrouter = mock_llm_escalade
_tr.process_with_openrouter = mock_llm_escalade

res_esc = orchestrator.run_with_policy(
    content=SMOKE_SOURCE, filename="esc.md", lang="fr",
    policy="auto", decl_type="qcm")
tel = res_esc["policy_telemetry"]
check("escalade : ≥2 échelons tentés", len(tel["tried"]) >= 2)
check("escalade : échelon 1 ROUGE puis gagnant VERT",
      tel["tried"][0]["ok"] is False and tel["tried"][-1]["ok"] is True)
check("escalade : échelon gagnant journalisé",
      tel["winning_model"] == tel["tried"][-1]["model"] and not tel["needs_review"])

# Restaure les mocks standards pour la suite.
for _m in (analyze, audit, generate, orchestrator):
    _m.process_with_openrouter = mock_llm
_sols.process_with_openrouter = mock_llm
_tr.process_with_openrouter = mock_llm

# API : policy invalide → 400 ; manual avec modèle hors rôle → 400.
check("API : policy invalide → 400",
      client.post("/api/jobs", json={"content": "x", "policy": "zzz"}).status_code == 400)
check("API : manual modèle hors rôle → 400",
      client.post("/api/jobs", json={"content": "x", "policy": "manual",
                                     "models": {"generate": "glm-4-7-flash"}}).status_code == 400)
check("/api/models expose catalogue par rôle sans Fable",
      "fable" not in json.dumps(client.get("/api/models").get_json()).lower())

# ── 3quater. Aération, originalExerciseId, annulation (bouton Stop) ─────────
from app.pipeline.postprocess import aerate_blocks  # noqa: E402

_compact = (":::::{question}\n:questionType: MCQ\n::::{questionStatement}\n"
            "texte\n::::\n::::{mcqAnswer}\n:isRightAnswer: true\nx\n::::")
_aered, _n_aer = aerate_blocks(_compact)
check("aération : lignes vides avant chaque bloc",
      _n_aer == 2 and "\n\n::::{questionStatement}" in _aered
      and "\n\n::::{mcqAnswer}" in _aered)
check("aération : idempotente", aerate_blocks(_aered)[1] == 0)

from app.pipeline.generate import build_exercise_metadata  # noqa: E402

check("déclinaison : originalExerciseId = id du QST source",
      ":originalExerciseId: abc-123" in build_exercise_metadata(
          ":id: abc-123\n:title: T", "", {}, "", decl_type="qcm"))
check("déclinaison : originalExerciseId présent même sans id source",
      "\n:originalExerciseId:" in build_exercise_metadata(
          ":title: T", "", {}, "", decl_type="qcm"))
check("pythonise : pas d'originalExerciseId",
      "originalExerciseId" not in build_exercise_metadata(
          ":title: T", "", {}, "", decl_type=None))

# Annulation : job 3 fichiers avec mock LENT, cancel immédiat → cancelled.
check("annulation : job inconnu → 404",
      client.post("/api/jobs/zzz/cancel").status_code == 404)

import time as _time  # noqa: E402


def mock_llm_slow(*a, **k):
    _time.sleep(0.15)
    return mock_llm(*a, **k)


for _m in (analyze, audit, generate, orchestrator):
    _m.process_with_openrouter = mock_llm_slow
_sols.process_with_openrouter = mock_llm_slow
_tr.process_with_openrouter = mock_llm_slow

_rc_start = client.post("/api/jobs", json={
    "files": [{"filename": f"c{i}.md", "content": SMOKE_SOURCE} for i in range(3)]})
_jid_c = _rc_start.get_json()["job_id"]
check("annulation : cancel accepté (202)",
      client.post(f"/api/jobs/{_jid_c}/cancel").status_code == 202)
_st_c = None
for _ in range(400):
    _st_c = client.get(f"/api/jobs/{_jid_c}").get_json()
    if _st_c["status"] != "running":
        break
    _time.sleep(0.05)
check("annulation : statut final cancelled", _st_c["status"] == "cancelled")
check("annulation : arrêt anticipé (résultats partiels conservés)",
      _st_c["files_done"] < 3 and isinstance(_st_c["results"], list))
check("annulation : re-cancel d'un job terminé → 409",
      client.post(f"/api/jobs/{_jid_c}/cancel").status_code == 409)

for _m in (analyze, audit, generate, orchestrator):
    _m.process_with_openrouter = mock_llm
_sols.process_with_openrouter = mock_llm
_tr.process_with_openrouter = mock_llm

# Banc : --dry-run (plomberie complète hors ligne).
import subprocess  # noqa: E402

bench_proc = subprocess.run(
    [sys.executable, "-m", "bench", "run", "--dry-run",
     "--roles", "generate", "--models", "claude-sonnet-5,claude-opus-4-8",
     "--seeds", "5"],
    capture_output=True, text=True, timeout=600,
    cwd=str(Path(__file__).resolve().parent.parent),
)
check("bench --dry-run : exit 0", bench_proc.returncode == 0)
check("bench --dry-run : reco produite", "best=" in bench_proc.stdout)
check("bench --dry-run : recommended.json non modifié",
      "NON modifié" in bench_proc.stdout)

# ── 4. Téléchargement ZIP (endpoint, sans LLM) ───────────────────────────────
import io as _io  # noqa: E402
import zipfile as _zipfile  # noqa: E402

import app.server as _server  # noqa: E402

_fake = {
    "status": "done", "step_label": "Terminé", "current_file": "b.md",
    "files_total": 2, "files_done": 2, "error": None, "summary": {},
    "results": [
        {"filename": "a.md", "status": "done",
         "result": {"exercise": result["exercise"], "warnings": [],
                    "harness": {"ok": True, "seeds": 100}, "cost": {"usd": 0.01}}},
        {"filename": "a.md", "status": "done",   # collision de nom volontaire
         "result": {"exercise": "````{python}\nglobals()\n````\n`````", "warnings": [{}],
                    "harness": {"ok": False, "seeds": 100}, "cost": {"usd": 0.02}}},
        {"filename": "c.md", "status": "error", "error": "boom"},
    ],
}
with _server._JOBS_LOCK:
    _server._JOBS["smoketest"] = _fake
resp = client.get("/api/jobs/smoketest/download")
check("ZIP : 200 + mimetype zip", resp.status_code == 200 and "zip" in resp.mimetype)
zf = _zipfile.ZipFile(_io.BytesIO(resp.data))
names = zf.namelist()
check("ZIP : 2 .md (collision dédupliquée) + récap",
      "a_pythonise.md" in names and "a_pythonise_2.md" in names
      and "_recapitulatif.md" in names)
check("ZIP : 404 si job inconnu", client.get("/api/jobs/zzz/download").status_code == 404)

# ── Bilan ────────────────────────────────────────────────────────────────────
failed = [n for n, ok in PASS if not ok]
print(f"\n{len(PASS) - len(failed)}/{len(PASS)} smoke tests verts")
if failed:
    print("ÉCHECS :", failed)
    sys.exit(1)
print("✅ SMOKE OK")
