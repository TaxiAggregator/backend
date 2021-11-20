"""models package"""
# import engine
from .db import engine

# import embedded models
from .location import Location

# import models
from .user import User
from .taxi import Taxi

# import collections
from .user import collection as user_collection
from .taxi import collection as taxi_collection
