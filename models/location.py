"""location embedded model"""
from odmantic import EmbeddedModel
from pydantic.types import conlist


class Location(EmbeddedModel):  # pylint:disable=too-few-public-methods
    """location embedded model"""

    type: str = "Point"
    coordinates: conlist(float, min_items=2, max_items=2)  # type: ignore
