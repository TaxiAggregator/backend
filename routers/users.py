"""routes for users"""
from typing import List

from fastapi import APIRouter, HTTPException, status
from models import User, UserUpdateSchema, engine
from odmantic import ObjectId

router = APIRouter(prefix="/users", tags=["Users"])


# create path operation functions
@router.post("/signup", response_model=List[User], status_code=status.HTTP_201_CREATED)
async def create(users: List[User]):
    """signup new user"""
    await engine.save_all(users)
    return users


# read path operation functions
@router.get("/", response_model=List[User], status_code=status.HTTP_200_OK)
async def read_list(skip: int = 0, limit: int = 10):
    """fetch all users"""
    users = await engine.find(User, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def read_one_by_id(user_id: ObjectId):
    """fetch user by id"""
    user = await engine.find_one(User, User.id == user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return user


# update path operation functions
@router.patch("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_by_id(user_id: ObjectId, patch: UserUpdateSchema):
    """update user by id"""
    user = await engine.find_one(User, User.id == user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    patch_dict = patch.dict(exclude_unset=True)
    for field, value in patch_dict.items():
        setattr(user, field, value)
    await engine.save(user)


# delete path operation functions
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(user_id: ObjectId):
    """delete user by id"""
    user = await engine.find_one(User, User.id == user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    await engine.delete(user)
