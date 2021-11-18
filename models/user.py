from odmantic import Model
from pydantic.types import constr

from .location import Location


class User(Model):
    name: constr(min_length=3, max_length=30)
    location: Location
