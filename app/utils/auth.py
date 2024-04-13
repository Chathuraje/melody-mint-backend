from datetime import datetime, timedelta, timezone
from fastapi import security
from jose import jwt
from app.api.v1.libraries.user.user import get_user_by_wallet_address
from app.api.v1.responses.user import UserResponse
from app.api.v1.schemas.auth import TokenDataRequest
from app.config import settings

env = settings.get_settings()
oauth2_bearer = security.OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


# TODO: Try to add better authentication mechanism
async def authenticate_user(token_data: TokenDataRequest) -> None | UserResponse:

    user = await get_user_by_wallet_address(
        token_data.wallet_address, token_data.chain_id
    )

    if user is None:
        return None

    if user.moralis_id != token_data.moralis_id:
        return None

    return user


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, env.JWT_SECRET_ACCESS, algorithm=env.JWT_ALGORITHM
    )

    return encoded_jwt
