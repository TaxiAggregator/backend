"""db utilities and configuration"""
from motor.motor_asyncio import AsyncIOMotorClient

from odmantic import AIOEngine

# Todo read following values from env file
client = AsyncIOMotorClient("mongodb://localhost:27017/")
DATABASE = "test"

engine = AIOEngine(motor_client=client, database=DATABASE)
