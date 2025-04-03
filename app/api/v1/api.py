from fastapi import APIRouter
from app.api.v1.routers import shinsas

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(shinsas.router)
