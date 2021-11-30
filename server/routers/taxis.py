"""routes for taxi"""
from typing import List

from beanie import PydanticObjectId
from beanie.operators import In, Near
from fastapi import APIRouter, HTTPException, status
from server.models import Taxi, TaxiUpdateSchema

router = APIRouter(prefix="/taxis", tags=["Taxis"])


# create path operation functions
@router.post(
    "/", response_model=List[Taxi], status_code=status.HTTP_201_CREATED
)
async def create(taxis: List[Taxi]):
    """Register new taxi(s)"""
    result = await Taxi.insert_many(taxis)
    return await Taxi.find(In(Taxi.id, result.inserted_ids)).to_list()


# read path operation functions
@router.get("/", response_model=List[Taxi])
async def read_list(skip: int = 0, limit: int = 10):
    """fetch all taxis"""
    taxis = await Taxi.find_all(skip=skip, limit=limit).to_list()
    if not taxis:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return taxis


# geospatial query path operation functions
# These might be moved to booking service
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


@router.get("/{taxi_id}", response_model=Taxi, status_code=status.HTTP_200_OK)
async def read_one_by_id(taxi_id: PydanticObjectId):
    """fetch taxi by id"""
    taxi = await Taxi.find_one(Taxi.id == taxi_id)
    if not taxi:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return taxi


# update path operation functions
@router.patch("/{taxi_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_taxi_by_id(
    taxi_id: PydanticObjectId, patch: TaxiUpdateSchema
):
    """update taxi by id"""
    taxi = await Taxi.find_one(Taxi.id == taxi_id)
    if not taxi:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    patch_dict = patch.dict(exclude_unset=True)
    for field, value in patch_dict.items():
        setattr(taxi, field, value)

    await taxi.save()


# delete path operation functions
@router.delete("/{taxi_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_taxi_by_id(taxi_id: PydanticObjectId):
    """delete taxi by id"""
    taxi = await Taxi.find_one(Taxi.id == taxi_id)
    if not taxi:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    await taxi.delete()
