"""Non-régression RÉELLE du mode pythonise sous politique `auto`.

Lance le pipeline complet (LLM réels) sur l'énoncé de référence Exercice_1,
puis valide la sortie au harnais 300 graines. À lancer ponctuellement après
un chantier (le smoke hors-ligne reste la vérif de routine).

    PYTHONPATH=. .venv/bin/python tests/nonreg_pythonise.py [chemin_exo]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import _load_env, _setup_logging

_setup_logging()
_load_env()

from app.pipeline.orchestrator import run_with_policy
from app.validation import harness

SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else \
    Path(__file__).resolve().parent.parent.parent / "Exemples d'exercices" / "Exercice_1.md"

content = SRC.read_text(encoding="utf-8")
res = run_with_policy(content, filename=SRC.name, lang="fr", policy="auto",
                      set_step=lambda s: print(f"  · {s}", flush=True))

out = Path("/tmp/nonreg_pythonise_out.md")
out.write_text(res["exercise"], encoding="utf-8")

tele = res["policy_telemetry"]
print(f"\nharnais porte : {'VERT' if res['harness']['ok'] else 'ROUGE'}")
print(f"policy        : mode={tele['mode']} difficulté={tele['difficulty']} "
      f"gagnant={tele['winning_model']} échelons={len(tele['tried'])}")
print(f"coût          : {res['cost']}")
print(f"sortie        : {out}")

# Contre-validation indépendante, 300 graines (plus dur que la porte à 100).
rep = harness.validate_text(res["exercise"], seeds=300)
print(f"harnais 300   : {'VERT' if rep['ok'] else 'ROUGE'}")
if not rep["ok"]:
    print("échecs:", rep["first_failures"][:5])
    sys.exit(1)
print("NON-RÉGRESSION OK")
