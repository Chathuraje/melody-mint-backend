from fastapi import APIRouter
from app.api.root.routes.root import routers as root_routers

routers = APIRouter(
    tags=["Root"]
)

routers.include_router(root_routers)
