"""user data model"""
from odmantic import Model
from pydantic import constr
from pymongo import GEOSPHERE

from .db import engine
from .location import Location


class User(Model):  # pylint:disable=too-few-public-methods
    """user data model"""

    name: constr(min_length=3, max_length=30)  # type: ignore
    location: Location


# create indexes
collection = engine.get_collection(User)
collection.create_index([("location", GEOSPHERE)])
