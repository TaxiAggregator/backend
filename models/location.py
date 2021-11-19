from odmantic import EmbeddedModel
from pydantic.types import conlist


class Location(EmbeddedModel):
    type: str = "Point"
    coordinates: conlist(float, min_items=2, max_items=2)  # type: ignore
