"""Génère une déclinaison réelle et sauvegarde la sortie pour inspection.

    PYTHONPATH=. .venv/bin/python tests/gen_decl_sample.py [qcm|qat] [exo]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import _load_env, _setup_logging

_setup_logging()
_load_env()

from app.pipeline.orchestrator import run_declinaisons

decl = sys.argv[1] if len(sys.argv) > 1 else "qcm"
SRC = Path(sys.argv[2]) if len(sys.argv) > 2 else \
    Path(__file__).resolve().parent.parent / "bench" / "corpus" / "trinome_pythonise.md"

content = SRC.read_text(encoding="utf-8")
(dt, res), = run_declinaisons(content, filename=SRC.name, lang="fr",
                              types=[decl])
out = Path(f"/tmp/decl_{decl}_sample.md")
out.write_text(res["exercise"], encoding="utf-8")
print(f"harnais : {'VERT' if res['harness']['ok'] else 'ROUGE'} → {out}")
