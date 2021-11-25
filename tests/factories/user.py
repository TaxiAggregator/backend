"""factory class for user model"""
import factory
from server.models import User

from .location import LocationFactory


class UserFactory(factory.Factory):
    """factory class for user model"""

    class Meta:
        """meta options"""

        model = User

    name = factory.Sequence(lambda n: f"User_{n}")
    location = factory.SubFactory(LocationFactory)
