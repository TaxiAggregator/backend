from typing import List

from fastapi import APIRouter
from models import Location, Taxi, engine

router = APIRouter(prefix="/taxis", tags=["Taxis"])


@router.get("/", response_model=List[Taxi])
async def read_list(skip: int = 0, limit: int = 10):
    """fetch all taxis"""
    taxis = await engine.find(Taxi, skip=skip, limit=limit)
    return taxis


@router.post("/", response_model=Taxi)
async def create(taxi: Taxi):
    """Register new taxi"""
    await engine.save(taxi)
    return taxi


@router.get("/near", response_model=List[Taxi])
async def fetch_taxis_within_radius(
    lat: float, long: float, distance: int = 1000, skip: int = 0, limit: int = 3
):
    """list taxis within the given distance (1km by default)"""
    # todo fix the query
    query = {
        "location": [
            ("$near", [lat, long]),
            ("$maxDistance", distance),
        ]
    }
    taxis = await engine.find(Taxi, query, skip=skip, limit=limit)
    return taxis


@router.get("/nearest", response_model=List[Taxi])
async def fetch_nearest_taxis(
    lat: float, long: float, distance: int = 1000, skip: int = 0, limit: int = 2
):
    """list nearest taxis (limited to 2 by default)"""
    # todo fix the query
    query = {
        "location": [
            ("$near", [lat, long]),
        ]
    }
    taxis = await engine.find(Taxi, query, skip=skip, limit=limit)
    return taxis
