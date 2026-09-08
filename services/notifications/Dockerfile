# Dockerfile multi-stage — fourni et commenté (TP4 : sachez expliquer chaque ligne).

# ---------- Étage 1 : construction -----------------------------------------
# On installe les dépendances dans une image temporaire ; seule le résultat
# sera copié dans l'image finale (image plus légère, pas d'outils de build).
FROM python:3.12-slim AS builder
WORKDIR /build
# On copie d'abord la description du projet : tant qu'elle ne change pas,
# Docker réutilise le cache de cette étape (builds beaucoup plus rapides).
COPY pyproject.toml .
COPY app/ app/
RUN pip install --no-cache-dir .

# ---------- Étage 2 : image finale ------------------------------------------
FROM python:3.12-slim
# Un utilisateur non root : si le conteneur est compromis, les dégâts sont limités.
RUN useradd --create-home appuser
# On récupère uniquement les paquets installés (et les exécutables comme uvicorn).
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
WORKDIR /srv
COPY app/ app/
USER appuser
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
