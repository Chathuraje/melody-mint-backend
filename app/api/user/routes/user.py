from typing import Annotated
from fastapi import APIRouter, Depends
from app.api.auth.utils.authentication import get_current_user
from app.model.User import UserProfile
from app.utils import logging
from app.api.user.libraries import user


logger = logging.getLogger()
router = APIRouter()

user_dependacy = Annotated[dict, Depends(get_current_user)]


@router.post("/profile/me", description="Get User Profile", response_model=UserProfile)
async def get_profile(user_data: user_dependacy):
    logger.info("Get User Profile endpoint accessed")

    return await user.get_profile(user_data)
