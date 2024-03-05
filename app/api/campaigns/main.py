from fastapi import APIRouter
from app.api.campaigns.routes.campaigns import router as campaigns_routers

router = APIRouter(
    tags=["Campaigns Managment"],
    prefix="/campaigns"
)

router.include_router(campaigns_routers)
