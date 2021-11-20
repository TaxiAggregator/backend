"""user data model"""
from typing import Optional

from odmantic import Model
from pydantic import BaseModel, constr
from pymongo import GEOSPHERE

from .db import engine
from .location import Location


class User(Model):  # pylint:disable=too-few-public-methods
    """user data model"""

    name: constr(min_length=3, max_length=30)  # type: ignore
    location: Location


class UserUpdateSchema(BaseModel):  # pylint:disable=too-few-public-methods
    """Schema for updating the user"""

    name: Optional[constr(min_length=3, max_length=30)]  # type: ignore
    location: Optional[Location]


# create indexes
collection = engine.get_collection(User)
collection.create_index([("location", GEOSPHERE)])
