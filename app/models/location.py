"""location embedded model"""
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, conlist


class LocationType(str, Enum):
    """taxi type choices"""

    POINT = "Point"
    POLYGON = "Polygon"


class Location(BaseModel):  # pylint:disable=too-few-public-methods
    """location embedded model"""

    type: LocationType
    coordinates: conlist(Decimal, min_items=2, max_items=2)  # type: ignore
