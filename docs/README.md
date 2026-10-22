# Documentation du projet

À compléter au fil des séances :

| Fichier            | Séance | Contenu attendu |
|--------------------|--------|-----------------|
| architecture.md    | TP1-2  | Schéma des services de votre thème, responsabilités, données |
| docker.md          | TP4    | Réponses aux questions sur le Dockerfile, scénario de panne |
| resilience.md      | TP5    | Temps de réponse en panne avant/après protection, choix 503 vs dégradé |
| events.md          | TP6    | Vos événements : nom, déclencheur, contenu, consommateurs |
| saga.md            | TP7    | Schéma de votre saga : étapes, événements, compensations |
| securite.md        | TP8    | Qui a le droit de faire quoi (rôles, autorisations par ressource) |
| chaos.md           | TP10   | Journal des pannes : incident, symptôme, correction |

## Démarrage rapide

```bash
cp .env.example .env
docker compose up --build -d
docker compose ps
```

## Vérification des services

Après le démarrage avec Docker Compose, les endpoints de santé sont disponibles ici :

```text
http://localhost:8000/health
http://localhost:8002/health
```

Résultats attendus :

```json
{"status":"ok","service":"vehicules"}
```

```json
{"status":"ok","service":"locations"}
```

Ces endpoints permettent de vérifier rapidement que les deux microservices sont démarrés et répondent correctement.
