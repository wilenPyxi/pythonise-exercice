# Pythonise Exercice — v2

App Flask à deux modes :
- **Pythonisation** d'exercices PyxiScience MyST (valeurs fixes → randomisées) ;
- **Déclinaisons** (2026-07) : génération de versions **QCM** (MCQ) et/ou
  **QAT** (FGQ, champs libres ordonnés) d'un exercice, randomisées elles aussi.

Pipeline async : analyse LLM + notions + RAG (parallèles, **partagés entre QCM
et QAT**) → génération par paires → audit LLM → filets déterministes → **porte
harnais** (100 graines + contrôles étendus déclinaisons : unicité des options
MCQ sur toutes les graines, 1 seule bonne réponse, « None » en dernier, arité
FGQ, `:solution:` JSON) ; verdict exposé dans l'UI.

## Architecture (refonte 2026-06)

```
run.py                      Lancement : python run.py   (ou python -m app)
app/
├── __init__.py             create_app() + logging + .env
├── config.py               TOUTE la config : modèles, PYTHON_FENCE_BACKTICKS=4,
│                           ANALYSIS_MODEL_IDX, RAG_TOP_K, USE_REASONING,
│                           DEFAULT_LANG, JOB_TTL, chemins, prix
├── server.py               routes Flask (/, /health, /api/models, /api/jobs)
├── keys.py                 chargement des clés API (.env)
├── pipeline/
│   ├── orchestrator.py     chef d'orchestre (1 exercice)
│   ├── analyze.py          analyse + notions + RAG en PARALLÈLE
│   ├── generate.py         découpage + génération par paires
│   ├── audit.py            audit LLM ≤2 itérations + filet de sécurité patches
│   ├── postprocess.py      filets déterministes (auto-lift {{}}, ${}, fences 4,
│   │                       renommage camelCase, décimales/langue, dédoublonnage)
│   ├── solutions.py        substitution des solutions validées (règle 8.1)
│   ├── translate.py        langue cible fr/en/both (prose seule, Python masqué)
│   ├── prompts.py          tous les prompts (v1 archivée dans knowledge/)
│   └── fewshots.py         sélection d'un exemple canonique par type détecté
├── rag/                    functions.py (FAISS) · formatter.py · notions.py ·
│                           catalogue.py (catalogue curé injecté par domaine)
├── llm/                    client.py (OpenRouter + reasoning opt.) · cost.py
├── validation/             harness.py (porte qualité) · sandbox.py (exec sandboxée)
├── knowledge/              pythonisation_rules.md · rules_digest.py ·
│                           fewshots/ (exemples VERTS) · prompts_v1_archive.md ·
│                           functions_catalogue.md (catalogue curé des helpers)
├── corpus/                 5 fichiers de fonctions PyxiScience (RAG)
└── web/templates/index.html  UI (batch, langue, verdict harnais, coût)
data/                       notions.xlsx · faiss_cache/
tests/smoke.py              smoke tests hors-ligne (LLM mocké)
```

## Installation (WSL Ubuntu)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt        # faiss-cpu + sentence-transformers ≈ 1.5 Go
cp .env.example .env                   # renseigner OPENROUTER_API_KEY / OPENAI_API_KEY
python run.py                          # http://127.0.0.1:5000
```

Smoke tests (sans réseau) : `.venv/bin/python tests/smoke.py`
Validation d'une sortie : `python ../.claude/skills/validation-harness/harness.py <fichier>.md --seeds 300`

### Endpoints

| Méthode | URL              | Description                                            |
|---------|------------------|--------------------------------------------------------|
| GET     | `/`              | UI web                                                 |
| GET     | `/health`        | sanity check                                           |
| GET     | `/api/models`    | roster des modèles + défauts                           |
| POST    | `/api/jobs`      | démarre un job (1 fichier OU batch) → `{job_id}`       |
| GET     | `/api/jobs/<id>` | suivi + résultats par fichier (harnais, coût, langue)  |
| GET     | `/api/jobs/<id>/download` | ZIP de toutes les sorties `.md` + `_recapitulatif.md` |

POST body :
```json
{
  "files": [{"filename": "exo.md", "content": "<MyST>"}, ...],
  "lang": "fr | en | both",
  "level": "",
  "model_idx": 1,
  "mode": "pythonise | declinaisons",
  "types": {"qcm": true, "qat": true}
}
```
(`mode` absent ⇒ `pythonise`, rétro-compatible ; `types` requis en mode
`declinaisons`, au moins un `true` — les deux cochés ⇒ 2 fichiers par source,
nommés `<source>_QCM.md` / `<source>_QAT.md`, avec UNE seule analyse partagée.
Rétro-compat : `{"content": "...", "filename": "..."}` accepté pour 1 fichier.)

Résultat par fichier : `exercise`, `analysis`, `notions`, `audit_patches`,
`warnings`, **`harness` {ok, seeds, summary}**, **`lang` {source, target, action}**,
**`cost` {usd, eur, requests}**, `duration_s`.

**Téléchargement** (UI, panneau Résultat) : bouton **« Télécharger .md »**
(sortie pythonisée du fichier affiché, suffixe `_pythonise.md` pour ne pas
écraser la source) ; en **batch**, bouton **« Tout (.zip) »** → ZIP de toutes
les sorties + un `_recapitulatif.md` (verdict harnais / warnings / coût par fichier).

## Sécurité

🚨 **Les clés API dans `.env` étaient en clair dans le zip d'origine** —
considère-les comme exposées et **rotate-les** :
- OpenRouter : https://openrouter.ai/keys
- OpenAI : https://platform.openai.com/api-keys

La sandbox (`app/validation/sandbox.py`) exécute le code généré par le LLM
avec builtins restreints, imports whitelistés et timeout (mono-poste : le
modèle de menace est l'accident LLM, pas un adversaire).

## Notes

- Premier lancement : reconstruit le cache FAISS si absent (≈ 30 s).
- Modèles (IDs vérifiés sur OpenRouter 2026-06-12) : Opus 4.8, **Sonnet 4.6
  (défaut)**, Fable 5, Haiku 4.5, Gemini 2.5 Pro, GPT-5.2.
- L'étape d'analyse suit le modèle choisi par l'utilisateur
  (`ANALYSIS_MODEL_IDX=None` dans config.py pour ce comportement).
- Mode batch : fichiers traités séquentiellement ; un échec n'arrête pas les
  autres ; récapitulatif VERT/ROUGE/erreurs + coût total.
