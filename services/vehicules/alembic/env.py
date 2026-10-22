"""Configuration Alembic (asynchrone) — fournie, vous n'avez pas à la modifier.

Dès que app/models.py définit `Base` (TP3), l'autogénération fonctionne :
    alembic revision --autogenerate -m "..."
    alembic upgrade head
"""
import asyncio
import os

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

# La cible des migrations : la metadata de vos modèles (créés au TP3).
try:
    from app.models import Base

    target_metadata = Base.metadata
except ImportError:
    target_metadata = None

DATABASE_URL = os.environ.get("DATABASE_URL", "")


def run_migrations_offline() -> None:
    context.configure(url=DATABASE_URL, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def _do_run_migrations(connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    engine = create_async_engine(DATABASE_URL)
    async with engine.connect() as connection:
        await connection.run_sync(_do_run_migrations)
    await engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
