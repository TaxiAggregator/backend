"""api backend for the taxi aggrigator capstone project (ACSE IIT Madras)"""
from fastapi import FastAPI, APIRouter
from routers import taxi_router, user_router

app = FastAPI()
api_v1 = APIRouter(prefix="/api/v1")

api_v1.include_router(user_router)
api_v1.include_router(taxi_router)

app.include_router(api_v1)
