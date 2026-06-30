"""
Centralised loader for API keys.

Loads variables from a `.env` file at the project root if present, then exposes
them as module-level constants. Never hardcode secrets here — put them in `.env`.
"""

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env")  # pythonisation_app/.env
except ImportError:
    # python-dotenv is optional; env vars can also be set directly in the shell
    pass

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENAI_API_KEY     = os.getenv("OPENAI_API_KEY", "")

if not OPENROUTER_API_KEY:
    print("[ld.py] WARNING: OPENROUTER_API_KEY is empty. Set it in .env or the shell environment.")
