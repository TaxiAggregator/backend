"""api backend for the taxi aggrigator capstone project (ACSE IIT Madras)"""
from fastapi import FastAPI, APIRouter
from routers import user_router

app = FastAPI()
api_v1 = APIRouter(prefix="/api/v1")

api_v1.include_router(user_router)

app.include_router(api_v1)
