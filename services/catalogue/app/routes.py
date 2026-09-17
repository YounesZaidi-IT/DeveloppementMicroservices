from fastapi import APIRouter, HTTPException
from app.schemas import VehiculeCreate, VehiculeRead


router = APIRouter(prefix="/vehicules", tags=["vehicules"])

_db: dict[int, VehiculeRead] = {}
_next_id = 1


@router.get("", response_model=list[VehiculeRead])
async def lister():
    return list(_db.values())


@router.get("/{vehicule_id}", response_model=VehiculeRead)
async def consulter(vehicule_id: int):
    if vehicule_id not in _db:
        raise HTTPException(status_code=404, detail="Véhicule introuvable")
    return _db[vehicule_id]


@router.post("", response_model=VehiculeRead, status_code=201)
async def creer(vehicule: VehiculeCreate):
    global _next_id

    nouveau = VehiculeRead(id=_next_id, **vehicule.model_dump())
    _db[_next_id] = nouveau
    _next_id += 1

    return nouveau


@router.put("/{vehicule_id}", response_model=VehiculeRead)
async def modifier(vehicule_id: int, vehicule: VehiculeCreate):
    if vehicule_id not in _db:
        raise HTTPException(status_code=404, detail="Véhicule introuvable")

    nouveau = VehiculeRead(id=vehicule_id, **vehicule.model_dump())
    _db[vehicule_id] = nouveau

    return nouveau


@router.delete("/{vehicule_id}", status_code=204)
async def supprimer(vehicule_id: int):
    if vehicule_id not in _db:
        raise HTTPException(status_code=404, detail="Véhicule introuvable")

    del _db[vehicule_id]