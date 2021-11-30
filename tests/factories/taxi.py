"""factory class for taxi model"""
from random import choice

import factory
from server.models.taxi import Taxi, TaxiType

from .location import LocationFactory


class TaxiFactory(factory.Factory):
    """factory class for taxi model"""

    class Meta:
        """meta options"""

        model = Taxi

    name = factory.Sequence(lambda n: f"Taxi_{n}")
    type = choice([type.value for type in TaxiType])  # nosec
    location = factory.SubFactory(LocationFactory)
