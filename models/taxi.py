"""taxi data model"""
from enum import Enum

from odmantic import Model
from pydantic.types import constr
from pymongo import GEOSPHERE

from .db import engine
from .location import Location


class TaxiType(str, Enum):
    """taxi type choices"""

    BASIC = "Basic"
    DELUXE = "Deluxe"
    LUXURY = "Luxury"


class Taxi(Model):  # pylint:disable=too-few-public-methods
    """taxi data model"""

    name: constr(min_length=3, max_length=30)  # type: ignore
    type: TaxiType
    location: Location

    class Config:
        """class config"""

        schema_extra = {
            "example": {
                "name": "Pavan",
                "type": "Deluxe",
                "location": {"type": "Point", "coordinates": [28.66542, 77.23154]},
            }
        }


collection = engine.get_collection(Taxi)
collection.create_index([("location", GEOSPHERE)])
