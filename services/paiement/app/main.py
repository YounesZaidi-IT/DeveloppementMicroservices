"""Point d'entrée du service Paiement — squelette fourni.

Fonctionne dès le TP1 (route /health). Les routeurs que vous créerez au fil
des TP sont branchés automatiquement s'ils existent (import défensif).
"""
from fastapi import FastAPI

app = FastAPI(title="Service Paiement")


@app.get("/health", tags=["monitoring"])
async def health():
    return {"status": "ok", "service": "paiement"}


# Le routeur métier (app/routes.py) est branché dès que vous le créez (TP2).
try:
    from app.routes import router  # noqa: E402

    app.include_router(router)
except ImportError:
    pass


# Le consommateur démarre en tâche de fond avec le service.
# (Désactivable, par exemple pour les tests : CONSOMMATEUR_ACTIF=0)
import asyncio  # noqa: E402
import os  # noqa: E402
from contextlib import asynccontextmanager  # noqa: E402

from app.consumer import arret, consommer  # noqa: E402


@asynccontextmanager
async def lifespan(_app: FastAPI):
    tache = None
    if os.environ.get("CONSOMMATEUR_ACTIF", "1") != "0":
        tache = asyncio.create_task(consommer())
    yield
    if tache is not None:
        arret.set()
        tache.cancel()
        await asyncio.wait([tache], timeout=10)


app.router.lifespan_context = lifespan
