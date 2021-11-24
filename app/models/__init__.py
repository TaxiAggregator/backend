"""models package"""
from .location import Location
from .settings import Settings
from .taxi import Taxi
from .user import User, UserUpdateSchema

# All models to instantiate on load
__beanie_models__ = [Taxi, User]
