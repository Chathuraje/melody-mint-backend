# Route: Get User Profile
from fastapi import HTTPException
from app.api.user.utils.UserDbController import get_user_by_id


async def get_user(user_id: str):
    user = await get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID: {user_id} not found.",
        )
    return user
