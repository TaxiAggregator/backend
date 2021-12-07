"""factory class for user model"""
import factory
from server.config import CONFIG
from server.models import User

from .location import LocationFactory


class UserFactory(factory.Factory):
    """factory class for user model"""

    class Meta:
        """meta options"""

        model = User

    userid = factory.Sequence(lambda n: f"{n + 1}")
    name = factory.Sequence(lambda n: f"User_{n+1}")
    email = factory.Sequence(
        lambda n: "{0}+user.{n}@{1}".format(  # pylint: disable=consider-using-f-string
            *CONFIG.email.split("@"), n=n + 1
        )
    )
    location = factory.SubFactory(LocationFactory)
