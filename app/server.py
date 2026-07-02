"""
server.py
─────────
Routes Flask — le minimum pour une app mono-fonctionnalité :

  GET  /                  UI
  GET  /health            sanity check
  GET  /api/models        roster des modèles + défauts
  POST /api/jobs          lance un job (1 fichier OU batch) → {job_id}
  GET  /api/jobs/<id>     suivi + résultats (par fichier)

Le job store reste en mémoire (mono-poste, mono-process — assumé) ; un job
batch traite ses fichiers SÉQUENTIELLEMENT et continue si l'un échoue.
"""

from __future__ import annotations

import io
import logging
import os
import re
import secrets
import threading
import time
import uuid
import zipfile

from flask import Response, jsonify, render_template, request, send_file

from app.config import (
    AVAILABLE_MODELS,
    DEFAULT_LANG,
    DEFAULT_MODE,
    DEFAULT_MODEL_IDX,
    DEFAULT_POLICY,
    JOB_TTL,
)
from app.pipeline.orchestrator import run_declinaisons, run_with_policy

logger = logging.getLogger(__name__)

_JOBS: dict = {}
_JOBS_LOCK = threading.Lock()

VALID_LANGS = ("fr", "en", "both")
VALID_LEVELS = ("", "Elementary", "Intermediate", "Advanced")
VALID_MODES = ("pythonise", "declinaisons")


def _set_job(job_id: str, **kwargs):
    with _JOBS_LOCK:
        if job_id in _JOBS:
            _JOBS[job_id].update(kwargs)


def _get_job(job_id: str):
    with _JOBS_LOCK:
        job = _JOBS.get(job_id)
        return dict(job) if job else None


def _safe_md_name(filename: str, used: set) -> str:
    """Nom de fichier .md sûr et unique pour le ZIP. Les déclinaisons portent
    déjà leur suffixe (_QCM/_QAT) ; la pythonisation reçoit _pythonise pour
    ne pas écraser la source."""
    base = re.sub(r"\.(md|txt)$", "", filename or "", flags=re.IGNORECASE)
    base = re.sub(r"[^\w.\-() ]+", "_", base).strip() or "exercice"
    suffix = "" if re.search(r"_(QCM|QAT)$", base) else "_pythonise"
    name = f"{base}{suffix}.md"
    i = 2
    while name in used:
        name = f"{base}{suffix}_{i}.md"
        i += 1
    used.add(name)
    return name


def _purge_old_jobs():
    cutoff = time.time() - JOB_TTL
    with _JOBS_LOCK:
        for jid in [jid for jid, j in _JOBS.items()
                    if j.get("status") in ("done", "error") and (j.get("finished_at") or 0) < cutoff]:
            del _JOBS[jid]


def _decl_output_name(source_name: str, decl_type: str) -> str:
    """foo.md + qcm → foo_QCM.md (nommage de sortie des déclinaisons)."""
    base = re.sub(r"\.(md|txt)$", "", source_name or "exercice", flags=re.IGNORECASE)
    return f"{base}_{'QCM' if decl_type == 'qcm' else 'QAT'}.md"


def _run_job(job_id: str, files: list[dict], level: str, model_idx: int,
             lang: str, mode: str = "pythonise", decl_types: list | None = None,
             policy: str = "auto", manual_models: dict | None = None):
    """Worker de job : boucle séquentielle sur les fichiers, robuste.
    En mode `declinaisons`, chaque source produit 1 résultat PAR type coché
    (analyse partagée entre types et échelons — aucun appel LLM redondant)."""
    results: list[dict] = []
    for i, f in enumerate(files):
        name = f.get("filename") or f"fichier_{i + 1}.md"
        _set_job(job_id, current_file=name, files_done=i,
                 step_label=f"[{i + 1}/{len(files)}] {name} — démarrage…")

        def set_step(label: str, _i=i, _name=name):
            _set_job(job_id, step_label=f"[{_i + 1}/{len(files)}] {_name} — {label}")

        try:
            if mode == "declinaisons":
                for decl_type, result in run_declinaisons(
                    content=f["content"],
                    filename=name,
                    level=level,
                    model_idx=model_idx,
                    lang=lang,
                    types=decl_types,
                    set_step=set_step,
                    policy=policy,
                    manual_models=manual_models,
                ):
                    out_name = _decl_output_name(name, decl_type)
                    results.append({"filename": out_name, "status": "done", "result": result})
                    logger.info("Déclinaison %s : harnais %s, modèle %s, %d warnings, %.1fs, %.4f$",
                                out_name, "VERT" if result["harness"]["ok"] else "ROUGE",
                                result.get("model_used"),
                                len(result["warnings"]), result["duration_s"],
                                result["cost"]["usd"])
            else:
                result = run_with_policy(
                    content=f["content"],
                    filename=name,
                    level=level,
                    lang=lang,
                    policy=policy,
                    manual_models=manual_models,
                    set_step=set_step,
                )
                results.append({"filename": name, "status": "done", "result": result})
                logger.info("Fichier %s : harnais %s, modèle %s, %d warnings, %.1fs, %.4f$",
                            name, "VERT" if result["harness"]["ok"] else "ROUGE",
                            result.get("model_used"),
                            len(result["warnings"]), result["duration_s"],
                            result["cost"]["usd"])
        except Exception as exc:
            logger.exception("Échec du pipeline sur %s", name)
            results.append({"filename": name, "status": "error", "error": str(exc)})
        _set_job(job_id, results=list(results), files_done=i + 1)

    ok = sum(1 for r in results
             if r["status"] == "done" and r["result"]["harness"]["ok"])
    warn = sum(1 for r in results
               if r["status"] == "done" and not r["result"]["harness"]["ok"])
    err = sum(1 for r in results if r["status"] == "error")
    total_cost = round(sum(r["result"]["cost"]["usd"] for r in results
                           if r["status"] == "done"), 4)
    _set_job(
        job_id,
        status="done",
        step_label="Terminé",
        finished_at=time.time(),
        summary={"total": len(files), "verts": ok, "rouges": warn,
                 "erreurs": err, "cost_usd": total_cost},
    )
    _purge_old_jobs()


def _auth_ok() -> bool:
    """Basic Auth si APP_PASSWORD est défini ; ouvert sinon (dev local)."""
    password = os.getenv("APP_PASSWORD", "")
    if not password:
        return True
    auth = request.authorization
    user = os.getenv("APP_USER", "pyxi")
    return bool(
        auth
        and auth.username == user
        and secrets.compare_digest(auth.password or "", password)
    )


def register_routes(app):

    @app.before_request
    def _gate():
        # /health reste ouvert (sonde de l'hébergeur) ; tout le reste est protégé
        # dès qu'un APP_PASSWORD est configuré (déploiement public).
        if request.path == "/health" or _auth_ok():
            return None
        return Response(
            "Authentification requise.",
            401,
            {"WWW-Authenticate": 'Basic realm="Pythonise Exercice"'},
        )

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/health")
    def health():
        return jsonify({
            "status": "ok",
            "openrouter_api_key": bool(os.getenv("OPENROUTER_API_KEY")),
            "openai_api_key": bool(os.getenv("OPENAI_API_KEY")),
        })

    @app.route("/api/models", methods=["GET"])
    def models():
        from app.models.catalog import CANDIDATES
        from app.models.policy import POLICIES, load_recommended
        return jsonify({
            "models": {str(k): v for k, v in AVAILABLE_MODELS.items()},
            "default_idx": DEFAULT_MODEL_IDX,
            "default_lang": DEFAULT_LANG,
            "policies": list(POLICIES),
            "default_policy": DEFAULT_POLICY,
            "catalog": CANDIDATES,          # candidats par rôle (sans Fable)
            "recommended": load_recommended(),
        })

    @app.route("/api/jobs", methods=["POST"])
    def start_job():
        """Body : {files: [{filename, content}, …], level?, model_idx?, lang?}
        (rétro-compat : {content, filename} accepté pour un fichier unique)."""
        data = request.get_json(force=True, silent=True) or {}

        files = data.get("files")
        if not files and data.get("content"):
            files = [{"filename": data.get("filename", "exercise.md"),
                      "content": data["content"]}]
        if not isinstance(files, list) or not files:
            return jsonify({"error": "Champ 'files' manquant ou vide."}), 400
        clean_files = []
        for f in files:
            if not isinstance(f, dict) or not str(f.get("content", "")).strip():
                return jsonify({"error": "Chaque fichier doit avoir un 'content' non vide."}), 400
            clean_files.append({
                "filename": str(f.get("filename") or "exercise.md"),
                "content": str(f["content"]).strip(),
            })

        level = (data.get("level") or "").strip()
        if level not in VALID_LEVELS:
            return jsonify({"error": f"'level' invalide : {level!r}."}), 400

        lang = (data.get("lang") or DEFAULT_LANG).strip()
        if lang not in VALID_LANGS:
            return jsonify({"error": f"'lang' invalide : {lang!r} (fr|en|both)."}), 400

        try:
            model_idx = int(data.get("model_idx", DEFAULT_MODEL_IDX))
        except (TypeError, ValueError):
            return jsonify({"error": "'model_idx' doit être un entier."}), 400
        if model_idx not in AVAILABLE_MODELS:
            return jsonify({
                "error": f"'model_idx' inconnu : {model_idx}. Valides : {sorted(AVAILABLE_MODELS)}."
            }), 400

        mode = (data.get("mode") or DEFAULT_MODE).strip()
        if mode not in VALID_MODES:
            return jsonify({"error": f"'mode' invalide : {mode!r} (pythonise|declinaisons)."}), 400
        decl_types: list = []
        if mode == "declinaisons":
            types_obj = data.get("types") or {}
            if not isinstance(types_obj, dict):
                return jsonify({"error": "'types' doit être un objet {qcm: bool, qat: bool}."}), 400
            decl_types = [t for t in ("qcm", "qat") if types_obj.get(t)]
            if not decl_types:
                return jsonify({"error": "En mode 'declinaisons', cocher au moins un type (qcm/qat)."}), 400

        # Politique de sélection de modèle (§5) — Fable absent du catalogue.
        from app.models.catalog import CATALOG, ROLES
        from app.models.policy import POLICIES
        policy = (data.get("policy") or DEFAULT_POLICY).strip()
        if policy not in POLICIES:
            return jsonify({"error": f"'policy' invalide : {policy!r} (auto|best|cheap|manual)."}), 400
        manual_models: dict = {}
        if policy == "manual":
            models_obj = data.get("models") or {}
            if not isinstance(models_obj, dict):
                return jsonify({"error": "'models' doit être un objet {generate, audit, mecanique}."}), 400
            for role in ROLES:
                key = models_obj.get(role)
                if not key:          # absent OU "" (select vide) → défaut config
                    continue
                if key not in CATALOG or role not in CATALOG[key]["roles"]:
                    return jsonify({"error": f"Modèle {key!r} invalide pour le rôle {role} "
                                             f"(catalogue : {[k for k, v in CATALOG.items() if role in v['roles']]})."}), 400
                manual_models[role] = key

        job_id = uuid.uuid4().hex
        with _JOBS_LOCK:
            _JOBS[job_id] = {
                "status": "running",
                "step_label": "Démarrage…",
                "current_file": clean_files[0]["filename"],
                "files_total": len(clean_files),
                "files_done": 0,
                "results": [],
                "summary": None,
                "error": None,
                "started_at": time.time(),
                "finished_at": None,
            }

        threading.Thread(
            target=_run_job,
            args=(job_id, clean_files, level, model_idx, lang, mode, decl_types,
                  policy, manual_models),
            daemon=True,
        ).start()
        return jsonify({"job_id": job_id}), 202

    @app.route("/api/jobs/<job_id>", methods=["GET"])
    def job_status(job_id: str):
        job = _get_job(job_id)
        if not job:
            return jsonify({"error": "Job inconnu."}), 404
        return jsonify({
            "status": job["status"],
            "step_label": job["step_label"],
            "current_file": job.get("current_file"),
            "files_total": job["files_total"],
            "files_done": job["files_done"],
            "results": job["results"],
            "summary": job.get("summary"),
            "error": job.get("error"),
        })

    @app.route("/api/jobs/<job_id>/download", methods=["GET"])
    def job_download_zip(job_id: str):
        """ZIP de toutes les sorties .md prêtes du job + un récapitulatif."""
        job = _get_job(job_id)
        if not job:
            return jsonify({"error": "Job inconnu (peut-être purgé)."}), 404
        done = [r for r in (job.get("results") or []) if r.get("status") == "done"]
        if not done:
            return jsonify({"error": "Aucun fichier prêt à télécharger."}), 404

        buf = io.BytesIO()
        used: set = set()
        recap = ["# Récapitulatif de pythonisation", ""]
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for r in done:
                name = _safe_md_name(r["filename"], used)
                zf.writestr(name, r["result"]["exercise"])
                h = r["result"]["harness"]
                recap.append(
                    f"- {name} — harnais {'VERT' if h['ok'] else 'ROUGE'} "
                    f"({h['seeds']} graines) · {len(r['result']['warnings'])} warnings "
                    f"· {r['result']['cost']['usd']} $"
                )
            for r in (job.get("results") or []):
                if r.get("status") == "error":
                    recap.append(f"- {r['filename']} — ERREUR : {r.get('error')}")
            zf.writestr("_recapitulatif.md", "\n".join(recap) + "\n")
        buf.seek(0)
        return send_file(
            buf, mimetype="application/zip", as_attachment=True,
            download_name=f"pythonise_{job_id[:8]}.zip",
        )
