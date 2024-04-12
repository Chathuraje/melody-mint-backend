from fastapi import APIRouter
from app.api.v1 import v1_routes

api_router = APIRouter(responses={404: {"description": "Not found"}})

api_router.include_router(v1_routes)
