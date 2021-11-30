"""models package"""
from .location import Location
from .taxi import Taxi, TaxiUpdateSchema
from .user import User, UserUpdateSchema

# All models to instantiate on load
__beanie_models__ = [Taxi, User]
