from odmantic import Model
from pydantic import constr, EmailStr
from pymongo import GEOSPHERE

from .db import engine
from .location import Location


class User(Model):
    name: constr(min_length=3, max_length=30)  # type: ignore
    location: Location


# create indexes
user_collection = engine.get_collection(User)
user_collection.create_index([("location", GEOSPHERE)])
