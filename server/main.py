"""api backend for the taxi aggregator capstone project (ACSE IIT Madras)"""

from fastapi import APIRouter

from server.app import app
from server.routers import taxi_router, user_router

# add routers
api_v1 = APIRouter(prefix="/api/v1")
api_v1.include_router(user_router)
api_v1.include_router(taxi_router)

app.include_router(api_v1)
