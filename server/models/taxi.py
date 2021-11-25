"""taxi data model"""
from enum import Enum

from beanie import Document
from pydantic.types import constr
from pymongo import GEOSPHERE

from .location import Location


# pylint:disable=too-few-public-methods
class TaxiType(str, Enum):
    """taxi type choices"""

    BASIC = "Basic"
    DELUXE = "Deluxe"
    LUXURY = "Luxury"


class Taxi(Document):
    """taxi data model"""

    name: constr(min_length=3, max_length=30)  # type: ignore
    type: TaxiType
    location: Location

    class Collection:
        """index fields"""

        indexes = [[("location", GEOSPHERE)]]
