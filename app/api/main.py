from fastapi import APIRouter
from app.api.root.main import router as root_routers
from app.api.auth.main import router as auth_routers
from app.api.user.main import router as user_routers

router = APIRouter(prefix="/api/v1")

router.include_router(root_routers)
router.include_router(auth_routers)
router.include_router(user_routers)
