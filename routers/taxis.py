from typing import List
from fastapi import APIRouter

from models import engine, Taxi

router = APIRouter(prefix="/taxis", tags=["Taxis"])


@router.get("/", response_model=List[Taxi])
async def read_list(skip: int = 0, limit: int = 10):
    """fetch all taxis"""
    taxis = await engine.find(Taxi, skip=skip, limit=limit)
    return taxis


@router.post("/", response_model=Taxi)
async def create(taxi: Taxi):
    await engine.save(taxi)
    return taxi
