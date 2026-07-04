"""
App « Pythonise Exercice v2 » — package applicatif.

    from app import create_app
    app = create_app()

Lancement : `python run.py` (ou `python -m app`).
"""

import logging
from pathlib import Path


def _load_env() -> None:
    """Charge .env AVANT tout import qui lit les clés."""
    try:
        from dotenv import load_dotenv
        load_dotenv(Path(__file__).resolve().parent.parent / ".env")
    except ImportError:
        logging.getLogger(__name__).warning(
            "python-dotenv absent ; variables d'environnement du shell utilisées.")


def _setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s — %(message)s",
        datefmt="%H:%M:%S",
    )
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("werkzeug").setLevel(logging.WARNING)


def create_app():
    _setup_logging()
    _load_env()

    # Serveur mono-process : le job (thread CPU-bound — harnais sympy) et les
    # requêtes de suivi partagent le GIL. Commutation à 1 ms (défaut 5 ms) pour
    # que /api/jobs/<id> réponde pendant les phases de calcul (coût ~négligeable).
    import sys
    sys.setswitchinterval(0.001)

    from flask import Flask
    from app.config import TEMPLATES_DIR
    from app.server import register_routes

    flask_app = Flask(__name__, template_folder=str(TEMPLATES_DIR))
    flask_app.config["JSON_SORT_KEYS"] = False
    register_routes(flask_app)
    return flask_app
