"""location factory"""

import factory
from server.models import Location


class LocationFactory(factory.Factory):
    """location factory class"""

    class Meta:
        """meta options"""

        model = Location

    type = "Point"
    coordinates = [28.123, 72.123]
