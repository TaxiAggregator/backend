"""routes for taxi"""
from typing import List

from fastapi import APIRouter, HTTPException, status
from models import engine, Location, Taxi, taxi_collection

router = APIRouter(prefix="/taxis", tags=["Taxis"])


@router.get("/", response_model=List[Taxi])
async def read_list(skip: int = 0, limit: int = 10):
    """fetch all taxis"""
    taxis = await engine.find(Taxi, skip=skip, limit=limit)
    return taxis


@router.post("/", response_model=List[Taxi])
async def create(taxis: List[Taxi]):
    """Register new taxi(s)"""
    await engine.save_all(taxis)
    return taxis


@router.post("/near", response_model=List[Taxi])
async def fetch_taxis_within_radius(customer_location: Location, radius: int = 1000):
    """list taxis within the given distance (1km by default)"""
    query = {
        "location": {
            "$nearSphere": {
                "$geometry": customer_location.dict(),
                "$maxDistance": radius,
            }
        }
    }
    taxis = []
    async for taxi in taxi_collection.find(query):
        taxis.append(Taxi.parse_doc(taxi))
    if not taxis:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return taxis


@router.post("/nearest", response_model=List[Taxi])
async def fetch_nearest_taxis(customer_location: Location, limit: int = 2):
    """list nearest taxis (limited to 2 by default)"""
    query = {"location": {"$nearSphere": {"$geometry": customer_location.dict()}}}
    taxis = list(map(Taxi.parse_doc, await taxi_collection.find(query).to_list(limit)))
    if not taxis:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return taxis
