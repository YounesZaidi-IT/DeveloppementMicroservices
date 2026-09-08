"""Point d'entrée du service Auth — squelette fourni.

Fonctionne dès le TP1 (route /health). Les routeurs que vous créerez au fil
des TP sont branchés automatiquement s'ils existent (import défensif).
"""
from fastapi import FastAPI

app = FastAPI(title="Service Auth")


@app.get("/health", tags=["monitoring"])
async def health():
    return {"status": "ok", "service": "auth"}


# Le routeur métier (app/routes.py) est branché dès que vous le créez (TP2).
try:
    from app.routes import router  # noqa: E402

    app.include_router(router)
except ImportError:
    pass
