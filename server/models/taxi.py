"""taxi data model"""
from enum import Enum
from typing import Optional

from beanie import Document
from pydantic import BaseModel, EmailStr
from pydantic.types import constr
from pymongo import ASCENDING, GEOSPHERE

from .location import Location


# pylint:disable=too-few-public-methods
class TaxiType(str, Enum):
    """taxi type choices"""

    BASIC = "Basic"
    DELUXE = "Deluxe"
    LUXURY = "Luxury"


class Taxi(Document):
    """taxi data model"""

    taxiid: str
    email: EmailStr
    name: constr(min_length=3, max_length=30)  # type: ignore
    type: TaxiType
    location: Location

    class Collection:
        """index fields"""

        indexes = [[("location", GEOSPHERE)], [("taxiid", ASCENDING)]]


class TaxiUpdateSchema(BaseModel):
    """schema for update the taxi"""

    email: Optional[EmailStr]
    name: Optional[constr(min_length=3, max_length=30)]  # type: ignore
    type: Optional[TaxiType]
    location: Optional[Location]
