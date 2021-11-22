"""location embedded model"""
from pydantic import BaseModel, conlist


class Location(BaseModel):  # pylint:disable=too-few-public-methods
    """location embedded model"""

    type: str = "Point"
    coordinates: conlist(float, min_items=2, max_items=2)  # type: ignore
