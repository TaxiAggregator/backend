"""user data model"""
from typing import Optional

from beanie import Document
from pydantic import BaseModel, constr
from pymongo import GEOSPHERE

from .location import Location


# pylint:disable=too-few-public-methods
class User(Document):
    """user data model"""

    name: constr(min_length=3, max_length=30)  # type: ignore
    location: Location

    class Collection:
        """index fields"""

        indexes = [[("location", GEOSPHERE)]]


class UserUpdateSchema(BaseModel):
    """Schema for updating the user"""

    name: Optional[constr(min_length=3, max_length=30)]  # type: ignore
    location: Optional[Location]
