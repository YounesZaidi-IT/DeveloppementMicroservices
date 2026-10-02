from pydantic import BaseModel, ConfigDict, Field


class VehiculeCreate(BaseModel):
    modele: str = Field(min_length=1, max_length=100)
    tarif_par_jour: float = Field(gt=0)
    places: int = Field(ge=2, le=9)


class VehiculeRead(VehiculeCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)