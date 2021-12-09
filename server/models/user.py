"""user data model"""
from typing import Optional

from beanie import Document
from pydantic import BaseModel, EmailStr, constr
from pymongo import ASCENDING, GEOSPHERE

from .location import Location


# pylint:disable=too-few-public-methods
class User(Document):
    """user data model"""

    userid: str
    name: constr(min_length=3, max_length=30)  # type: ignore
    email: EmailStr
    location: Location

    class Collection:
        """index fields"""

        indexes = [[("location", GEOSPHERE)], [("userid", ASCENDING)]]


class UserUpdateSchema(BaseModel):
    """Schema for updating the user"""

    name: Optional[constr(min_length=3, max_length=30)]  # type: ignore
    email: Optional[EmailStr]
    location: Optional[Location]
