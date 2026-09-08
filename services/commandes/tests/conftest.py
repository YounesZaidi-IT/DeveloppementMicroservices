"""Fixtures de test — fournies. Elles évoluent avec votre projet :

- `client`        : client de test anonyme (TestClient FastAPI)
- `client_admin`  : client authentifié avec le rôle admin (utile à partir du TP8 ;
                    avant le TP8, il est identique à `client`)

À partir du TP3, la base PostgreSQL est remplacée par une base SQLite en mémoire
pour que les tests soient rapides et isolés.
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app

# ---- Base de test (activée dès que app/db.py et app/models.py existent, TP3+) ----
try:
    from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

    import app.db as db
    from app.models import Base

    _engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    db.engine = _engine
    db.SessionLocal = async_sessionmaker(_engine, expire_on_commit=False)

    @pytest.fixture(autouse=True)
    async def _creer_tables():
        async with _engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield
        async with _engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

except ImportError:  # avant le TP3 : stockage en mémoire, rien à faire
    pass


def _client_avec_utilisateur(payload):
    try:
        from app.security import utilisateur_courant

        app.dependency_overrides[utilisateur_courant] = lambda: payload
    except ImportError:  # avant le TP8 : pas d'authentification
        pass
    return TestClient(app)


@pytest.fixture
def client():
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def client_admin():
    yield _client_avec_utilisateur({"sub": "1", "role": "admin"})
    app.dependency_overrides.clear()


@pytest.fixture
def client_utilisateur():
    yield _client_avec_utilisateur({"sub": "2", "role": "client"})
    app.dependency_overrides.clear()
