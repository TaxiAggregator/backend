"""routes for taxi"""
from typing import List

from beanie.operators import In, Near
from fastapi import APIRouter, HTTPException, status
from server.models import Taxi

router = APIRouter(prefix="/taxis", tags=["Taxis"])


@router.get("/", response_model=List[Taxi])
async def read_list(skip: int = 0, limit: int = 10):
    """fetch all taxis"""
    taxis = await Taxi.find_all(skip=skip, limit=limit).to_list()
    if not taxis:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return taxis


@router.post("/", response_model=List[Taxi])
async def create(taxis: List[Taxi]):
    """Register new taxi(s)"""
    result = await Taxi.insert_many(taxis)
    return await Taxi.find(In(Taxi.id, result.inserted_ids)).to_list()


@router.get("/near", response_model=List[Taxi])
async def fetch_taxis_within_radius(
    longitude: float,
    latitude: float,
    max_distance: int = 1000,
    skip: int = 0,
    limit: int = 5,
):
    """list taxis within the given distance (1km by default)"""
    taxis = await Taxi.find_many(
        Near(
            Taxi.location,
            longitude=longitude,
            latitude=latitude,
            max_distance=max_distance,
        ),
        skip=skip,
        limit=limit,
    ).to_list()

    if not taxis:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return taxis


@router.get("/nearest", response_model=List[Taxi])
async def fetch_nearest_taxis(
    longitude: float, latitude: float, skip: int = 0, limit: int = 5
):
    """list nearest taxis (limited to 2 by default)"""
    taxis = await Taxi.find_many(
        Near(Taxi.location, longitude=longitude, latitude=latitude),
        skip=skip,
        limit=limit,
    ).to_list()
    if not taxis:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return taxis
