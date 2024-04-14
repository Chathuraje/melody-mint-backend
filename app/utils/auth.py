from datetime import datetime, timedelta, timezone
from fastapi import security
from jose import jwt
from app.api.v1.libraries.user.db import db_get_stored_message
from app.api.v1.libraries.user.user import get_user_by_wallet_address
from app.api.v1.responses.user import UserResponse
from app.api.v1.schemas.auth import TokenDataRequest
from app.api.v1.schemas.user import UserCreateRequest
from app.api.v1.utils.common import is_user_exist
from app.config import settings
from app.utils.web3 import web3_verify_signature

env = settings.get_settings()
oauth2_bearer = security.OAuth2PasswordBearer(tokenUrl="/api/v1/auth/access_token")


# TODO: Try to add better authentication mechanism
async def authenticate_user(token_data: TokenDataRequest) -> None | UserResponse:
    user_data = UserCreateRequest(
        moralis_id=token_data.moralis_id,
        wallet_address=token_data.wallet_address,
        chain_id=token_data.chain_id,
    )
    user = await is_user_exist(user_data)
    if user is None:
        return None

    message = await db_get_stored_message(user_data.wallet_address)
    if message is None:
        return None

    if not await web3_verify_signature(
        message, token_data.signature, token_data.wallet_address, token_data.chain_id
    ):
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


def create_refresh_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, env.JWT_SECRET_REFRESH, algorithm=env.JWT_ALGORITHM
    )

    return encoded_jwt
