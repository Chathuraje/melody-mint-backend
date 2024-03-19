from fastapi import APIRouter
from app.api.root.main import router as root_routers
from app.api.auth.main import router as auth_routers
from app.api.users.main import router as users_routers
from app.api.campaigns.main import router as campaigns_routers
from app.api.marketplace.main import router as marketplace_routers
from app.api.music_identifier.main import router as music_identifier_routers
from app.api.video_identifier.main import router as video_identifier_routers

router = APIRouter(
    prefix="/api"
)

router.include_router(root_routers)
router.include_router(auth_routers)
router.include_router(users_routers)
router.include_router(campaigns_routers)
router.include_router(marketplace_routers)
router.include_router(music_identifier_routers)
router.include_router(video_identifier_routers)