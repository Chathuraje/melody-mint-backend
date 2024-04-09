from typing import Annotated
from fastapi import APIRouter, Depends
from app.api.auth.utils.authentication import get_current_user
from app.model.User import UserResponse
from app.utils import logging
from app.api.user.libraries import user


logger = logging.getLogger()
router = APIRouter()

user_dependacy = Annotated[dict, Depends(get_current_user)]


@router.get("/{user_id}", description="Get User Profile", response_model=UserResponse)
async def get_user(user_id: str):
    logger.info("Get User Profile endpoint accessed")

    return await user.get_user(user_id)
