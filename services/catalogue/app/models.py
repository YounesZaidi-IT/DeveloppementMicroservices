from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Vehicule(Base):
    __tablename__ = "vehicules"

    id: Mapped[int] = mapped_column(primary_key=True)
    modele: Mapped[str]
    tarif_par_jour: Mapped[float]
    places: Mapped[int]