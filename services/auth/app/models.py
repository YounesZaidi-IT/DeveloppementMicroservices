"""Modèle utilisateur du service Auth — fourni (TP8)."""
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Utilisateur(Base):
    __tablename__ = "utilisateurs"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    mot_de_passe_hache: Mapped[str]
    role: Mapped[str] = mapped_column(default="client")  # "client" ou "admin"
