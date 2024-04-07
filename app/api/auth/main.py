from fastapi import APIRouter
from app.api.auth.routes.auth import router as auth_routes


router = APIRouter(tags=["Authentications"], prefix="/auth")

router.include_router(auth_routes)
