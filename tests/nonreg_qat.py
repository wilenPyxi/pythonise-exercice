"""Non-régression RÉELLE du mode déclinaisons QAT (non couvert par le banc,
qui exerce le chemin QCM). LLM réels + harnais 300 graines.

    PYTHONPATH=. .venv/bin/python tests/nonreg_qat.py [chemin_exo]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import _load_env, _setup_logging

_setup_logging()
_load_env()

from app.pipeline.orchestrator import run_declinaisons
from app.validation import harness

SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else \
    Path(__file__).resolve().parent.parent / "bench" / "corpus" / "trinome_pythonise.md"

content = SRC.read_text(encoding="utf-8")
out = run_declinaisons(content, filename=SRC.name, lang="fr", types=["qat"],
                       set_step=lambda s: print(f"  · {s}", flush=True))

(decl_type, res), = out
tele = res["policy_telemetry"]
print(f"\nharnais porte : {'VERT' if res['harness']['ok'] else 'ROUGE'}")
print(f"policy        : gagnant={tele['winning_model']} échelons={len(tele['tried'])}")
print(f"coût          : {res['cost']}")

# (les contrôles déclinaison sont auto-détectés par validate_text)
rep = harness.validate_text(res["exercise"], seeds=300)
print(f"harnais 300   : {'VERT' if rep['ok'] else 'ROUGE'}")
if not rep["ok"]:
    print("échecs:", rep["first_failures"][:5])
    sys.exit(1)
print("NON-RÉGRESSION QAT OK")
