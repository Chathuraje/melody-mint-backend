from fastapi import APIRouter
from app.api.marketplace.routes.marketplace import router as marketplace_routers

router = APIRouter(
    tags=["Marketpalce Managment"],
    prefix="/marketplace"
)

router.include_router(marketplace_routers)
