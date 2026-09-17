from pydantic import BaseModel, Field


class VehiculeCreate(BaseModel):
    modele: str = Field(min_length=1, max_length=100)
    tarif_par_jour: float = Field(gt=0, description="Tarif par jour en dirhams, strictement positif")
    places: int = Field(ge=2, le=9)


class VehiculeRead(VehiculeCreate):
    id: int