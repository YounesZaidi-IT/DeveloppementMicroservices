# Microservices en Python — dépôt template

Point de départ du projet fil rouge du module **Développement de Microservices en Python**
(Master formation continue, Pr. LOUZAR Oumaima, 2026-2027).

## Développeur

**Younes Zaidi**
Développeur — Projet Microservices en Python [12-09-2026]

## Démarrage rapide

```bash
cp .env.example .env
docker compose up --build
# puis ouvrir http://localhost:8000/docs  (service Catalogue)
```

## Structure

```
├── .devcontainer/        # environnement Codespaces / VS Code (option B)
├── .github/workflows/    # pipeline CI (complété au TP9)
├── docker-compose.yml    # orchestration (complété au fil des TP)
├── services/
│   ├── catalogue/        # service exemple : le plus complet, servez-vous-en de modèle
│   ├── commandes/
│   ├── auth/
│   ├── paiement/         # simulateur de paiement (TP7)
│   └── notifications/    # consommateur d'événements (TP6)
├── scripts/              # check_tp2.py, chaos.py, trafic.py
└── docs/                 # vos schémas et décisions (architecture, saga, sécurité…)
```

Chaque service suit la même structure : `app/` (code FastAPI), `tests/`, `Dockerfile`, `pyproject.toml`,
et pour ceux qui ont une base : `alembic/` (migrations).

## Règles du module

- Un tag Git par séance : `git tag s01 && git push --tags` en fin de TP.
- Le fichier `.env` n'est **jamais** versionné ; `.env.example` liste les variables attendues.
- Le rendu final est le tag `v1.0`.

## Ce qui est déjà fait pour vous

- Dockerfiles commentés, Compose de départ, configuration Alembic, squelettes lançables (`/health`).
- Fixtures de test (`tests/conftest.py`) et squelette de pipeline CI.
- Scripts du cours : vérification du TP2, campagne de chaos et générateur de trafic (TP10).

## Ce que vous allez écrire

Le code métier : schémas, routes, modèles, migrations, clients HTTP, événements, saga, sécurité, tests.
Chaque TP vous dit exactement quoi faire — et comment vérifier que ça marche.
