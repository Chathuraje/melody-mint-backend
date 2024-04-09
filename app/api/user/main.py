from fastapi import APIRouter
from app.api.user.routes.user import router as user_routes


router = APIRouter(tags=["Users"], prefix="/users")

router.include_router(user_routes)
