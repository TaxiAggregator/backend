"""routes for users"""
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
async def get_all(skip: int = 0, limit: int = 20):
    """fetch all users"""
    return {"data": [f"user {i}" for i in range(skip, limit)]}


@router.get("/signup")
async def signup():
    """signup users"""
    return {"data": [f"user {i}" for i in range(1, 6)]}
