"""routes for users"""
from typing import List

from beanie import PydanticObjectId
from beanie.operators import In
from fastapi import APIRouter, HTTPException, status
from server.models import User, UserUpdateSchema

router = APIRouter(prefix="/users", tags=["Users"])


# create path operation functions
@router.post(
    "/", response_model=List[User], status_code=status.HTTP_201_CREATED
)
async def create(users: List[User]):
    """signup new user(s)"""
    result = await User.insert_many(users)
    return await User.find(In(User.id, result.inserted_ids)).to_list()


# read path operation functions
@router.get("/", response_model=List[User], status_code=status.HTTP_200_OK)
async def read_list(skip: int = 0, limit: int = 10):
    """fetch all users"""
    users = await User.find_all(skip=skip, limit=limit).to_list()
    if not users:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return users


@router.get("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def read_one_by_id(user_id: PydanticObjectId):
    """fetch user by id"""
    user = await User.find_one(User.id == user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return user


# update path operation functions
@router.patch("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_by_id(
    user_id: PydanticObjectId, patch: UserUpdateSchema
):
    """update user by id"""
    user = await User.find_one(User.id == user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    patch_dict = patch.dict(exclude_unset=True)
    for field, value in patch_dict.items():
        setattr(user, field, value)

    await user.save()


# delete path operation functions
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(user_id: PydanticObjectId):
    """delete user by id"""
    user = await User.find_one(User.id == user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    await user.delete()
