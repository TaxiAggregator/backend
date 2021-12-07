"""settings model"""
from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):  # pylint:disable=too-few-public-methods
    """settings model"""

    mongo_connection: str
    mongo_db: str
    version: str
    email: EmailStr

    longitude_min: float
    longitude_max: float
    latitude_min: float
    latitude_max: float


CONFIG = Settings(_env_file=".env")
