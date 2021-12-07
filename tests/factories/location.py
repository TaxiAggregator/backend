"""location factory"""
# from faker import Faker
from random import uniform

import factory
from server.config import CONFIG
from server.models import Location


class LocationFactory(factory.Factory):
    """location factory class"""

    class Meta:
        """meta options"""

        model = Location

    type = "Point"
    coordinates = factory.LazyAttribute(
        lambda _: [
            uniform(CONFIG.longitude_min, CONFIG.longitude_max),  # nosec
            uniform(CONFIG.latitude_min, CONFIG.latitude_max),  # nosec
        ]
    )
