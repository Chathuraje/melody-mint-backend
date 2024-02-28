from fastapi import APIRouter, HTTPException
from app.api.root.routes.main import routers as root_routers

routers = APIRouter(
    prefix="/api"
)

routers.include_router(root_routers)