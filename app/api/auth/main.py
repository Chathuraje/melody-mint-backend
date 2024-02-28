from fastapi import APIRouter
from app.api.auth.routes.auth import router as auth_routers

router = APIRouter(
    tags=["Authentiactions"],
    prefix="/auth"
)

router.include_router(auth_routers)
