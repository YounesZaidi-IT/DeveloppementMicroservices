from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.db import SessionLocal
from app.models import Vehicule
from app.schemas import VehiculeCreate, VehiculeRead


router = APIRouter(prefix="/vehicules", tags=["vehicules"])


@router.get("", response_model=list[VehiculeRead])
async def lister():
    async with SessionLocal() as session:
        result = await session.execute(select(Vehicule))
        return result.scalars().all()


@router.get("/{vehicule_id}", response_model=VehiculeRead)
async def consulter(vehicule_id: int):
    async with SessionLocal() as session:
        vehicule = await session.get(Vehicule, vehicule_id)

        if not vehicule:
            raise HTTPException(status_code=404, detail="Véhicule introuvable")

        return vehicule


@router.post("", response_model=VehiculeRead, status_code=201)
async def creer(vehicule: VehiculeCreate):
    async with SessionLocal() as session:
        nouveau = Vehicule(**vehicule.model_dump())

        session.add(nouveau)
        await session.commit()
        await session.refresh(nouveau)

        return nouveau


@router.put("/{vehicule_id}", response_model=VehiculeRead)
async def modifier(vehicule_id: int, vehicule: VehiculeCreate):
    async with SessionLocal() as session:
        existant = await session.get(Vehicule, vehicule_id)

        if not existant:
            raise HTTPException(status_code=404, detail="Véhicule introuvable")

        existant.modele = vehicule.modele
        existant.tarif_par_jour = vehicule.tarif_par_jour
        existant.places = vehicule.places

        await session.commit()
        await session.refresh(existant)

        return existant


@router.delete("/{vehicule_id}", status_code=204)
async def supprimer(vehicule_id: int):
    async with SessionLocal() as session:
        vehicule = await session.get(Vehicule, vehicule_id)

        if not vehicule:
            raise HTTPException(status_code=404, detail="Véhicule introuvable")

        await session.delete(vehicule)
        await session.commit()