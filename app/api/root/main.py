from fastapi import APIRouter
from app.api.root.routes.root import router as root_routers


router = APIRouter(tags=["Root"])

router.include_router(root_routers)
