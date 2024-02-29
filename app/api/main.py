from fastapi import APIRouter, HTTPException
from app.api.root.main import router as root_routers
from app.api.auth.main import router as auth_routers
from app.api.users.main import router as users_routers

router = APIRouter(
    prefix="/api"
)

router.include_router(root_routers)
router.include_router(auth_routers)
router.include_router(users_routers)