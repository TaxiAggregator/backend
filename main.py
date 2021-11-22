"""api backend for the taxi aggregator capstone project (ACSE IIT Madras)"""
from beanie import init_beanie
from fastapi import APIRouter, FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from models import Settings, __beanie_models__
from routers import taxi_router, user_router

settings = Settings(_env_file=".env")
app = FastAPI(title="Taxi Aggregator")


@app.on_event("startup")
async def startup_event():
    """startup code"""
    # init beanie
    client = AsyncIOMotorClient(settings.mongo_connection)
    await init_beanie(
        database=client[settings.mongo_db], document_models=__beanie_models__
    )

    # add routers
    api_v1 = APIRouter(prefix="/api/v1")
    api_v1.include_router(user_router)
    api_v1.include_router(taxi_router)

    app.include_router(api_v1)
