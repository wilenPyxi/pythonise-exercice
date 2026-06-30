"""Point d'entrée : `python run.py` → http://127.0.0.1:5000
(équivalent : `python -m app`). Reloader OFF — FAISS/HF lourds à charger."""

from app import create_app
from app.config import HOST, PORT

app = create_app()

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True, use_reloader=False)
