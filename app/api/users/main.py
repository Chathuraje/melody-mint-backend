from fastapi import APIRouter
from app.api.users.routes.users import router as users_routers

router = APIRouter(
    tags=["User Managment"],
    prefix="/users"
)

router.include_router(users_routers)
