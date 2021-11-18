"""routes for users"""
from typing import List
from fastapi import APIRouter

from models import engine, User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[User])
async def read_list(skip: int = 0, limit: int = 10):
    """fetch all users"""
    users = await engine.find(User)
    return users


@router.post("/signup", response_model=User)
async def create(user: User):
    """signup new user"""
    await engine.save(user)
    return user
