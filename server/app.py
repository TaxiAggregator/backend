"""FastAPI backend application"""
from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from server.config import CONFIG
from server.models import __beanie_models__

app = FastAPI(title="Taxi Aggregator", version=CONFIG.version)


@app.on_event("startup")
async def startup_event():
    """startup code"""
    # init beanie
    app.db = AsyncIOMotorClient(CONFIG.mongo_connection)[CONFIG.mongo_db]  # type: ignore
    await init_beanie(database=app.db, document_models=__beanie_models__)  # type: ignore
