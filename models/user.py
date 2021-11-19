from odmantic import Model
from pydantic import constr, EmailStr

from .location import Location


class User(Model):
    name: constr(min_length=3, max_length=30)  # type: ignore
    location: Location
