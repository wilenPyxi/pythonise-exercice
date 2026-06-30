"""`python -m app` → serveur de dev (reloader OFF : FAISS/HF lourds à charger)."""

from app import create_app
from app.config import HOST, PORT

create_app().run(host=HOST, port=PORT, debug=True, use_reloader=False)
