"""settings model"""
from pydantic import BaseSettings


class Settings(BaseSettings):  # pylint:disable=too-few-public-methods
    """settings model"""

    mongo_connection: str
    mongo_db: str
