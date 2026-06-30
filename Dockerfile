# Image de déploiement pour Hugging Face Spaces (SDK Docker).
# Slim : pas de torch/sentence-transformers (le défaut openai-3-small passe par
# l'API ; l'import HuggingFace est devenu paresseux). Cache FAISS openai-3-small
# (~1,2 Mo) embarqué → aucune reconstruction au démarrage.

FROM python:3.11-slim

# libgomp1 : requis par faiss-cpu.
RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# HF Spaces exécute le conteneur en utilisateur 1000 (bonne pratique).
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    HOST=0.0.0.0 \
    PORT=7860 \
    MPLCONFIGDIR=/tmp/mpl \
    PYTHONUNBUFFERED=1

WORKDIR /home/user/app

COPY --chown=user requirements-deploy.txt .
RUN pip install --no-cache-dir --user -r requirements-deploy.txt

COPY --chown=user . .

EXPOSE 7860

# UN SEUL worker (job store en mémoire + threads d'arrière-plan partagés),
# plusieurs threads pour que le polling et un job tournent en parallèle.
CMD ["gunicorn", "-w", "1", "--threads", "8", "--timeout", "120", \
     "-b", "0.0.0.0:7860", "run:app"]
