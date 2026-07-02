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


def mock_llm(prompt, model_idx=0, temperature=0.0, max_tokens=4096,
             image_b64=None, system_prompt="", reasoning=False):
    if "expert en analyse d'exercices" in prompt:
        ANALYSIS_CALLS["n"] += 1
        return MOCK_ANALYSIS
    if "auditeur PyxiScience" in prompt:
        return json.dumps({"verdict": "OK", "issues": []})
    if "Tu déclines un exercice" in prompt:
        return MOCK_MCQ_PAIR if "QCM (MCQ)" in prompt else MOCK_FGQ_PAIR
    if "RÈGLES D'ASSEMBLAGE PAR PAIRE" in prompt:
        return MOCK_PAIR
    return "{}"


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
decl_results = orchestrator.run_declinaisons(
    content=SMOKE_SOURCE, filename="smoke.md", level="", model_idx=0,
    lang="fr", types=["qcm", "qat"])
check("déclinaisons : 2 sorties (QCM + QAT)", len(decl_results) == 2)
check("déclinaisons : analyse partagée (1 seul appel)", ANALYSIS_CALLS["n"] == 1)

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
