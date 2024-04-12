from fastapi import APIRouter
from app.api.v1.routes.root import root_router
from app.api.v1.routes.auth import auth_router
from app.api.v1.routes.user import user_router

v1_routes = APIRouter(prefix="/v1")

v1_routes.include_router(root_router)
v1_routes.include_router(auth_router)
v1_routes.include_router(user_router)
