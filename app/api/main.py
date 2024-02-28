from fastapi import APIRouter, HTTPException
from app.api.root.main import router as root_routers

router = APIRouter(
    prefix="/api"
)

router.include_router(root_routers)