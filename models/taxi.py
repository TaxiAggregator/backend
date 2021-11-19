from enum import Enum
from odmantic import Model
from pydantic.types import constr
from pymongo import GEOSPHERE

from .db import engine
from .location import Location


class TaxiType(str, Enum):
    basic = "Basic"
    deluxe = "Deluxe"
    Luxury = "Luxury"


class Taxi(Model):
    name: constr(min_length=3, max_length=30)  # type: ignore
    type: TaxiType
    location: Location


user_collection = engine.get_collection(Taxi)
user_collection.create_index([("location", GEOSPHERE)])
