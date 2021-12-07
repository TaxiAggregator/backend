"""factory class for taxi model"""
from random import choice

import factory
from server.config import CONFIG
from server.models.taxi import Taxi, TaxiType

from .location import LocationFactory


class TaxiFactory(factory.Factory):
    """factory class for taxi model"""

    class Meta:
        """meta options"""

        model = Taxi

    taxiid = factory.Sequence(lambda n: f"{n + 1}")
    email = factory.Sequence(
        lambda n: "{0}+taxi.{n}@{1}".format(  # pylint: disable=consider-using-f-string
            *CONFIG.email.split("@"), n=n + 1
        )
    )
    name = factory.Sequence(lambda n: f"Taxi_{n+1}")
    type = choice([type.value for type in TaxiType])  # nosec
    location = factory.SubFactory(LocationFactory)
