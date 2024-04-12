from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, security
from jose import JWTError, jwt
from app.api.v1.libraries.user.user import get_user_by_wallet_address
from app.api.v1.responses.user import UserResponse
from app.api.v1.schemas.auth import TokenDataRequest
from app.config import settings


oauth2_bearer = security.OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")
env = settings.get_settings()


# TODO: Try to add better authentication mechanism
async def authenticate_user(token_data: TokenDataRequest) -> bool:
    user = await get_user_by_wallet_address(
        token_data.wallet_address, token_data.chain_id
    )

    return user is None or user.moralis_id != token_data.moralis_id


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate token.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, env.JWT_SECRET, algorithms=[env.JWT_ALGORITHM])
        id = payload.get("id")
        moralis_id = payload.get("moralis_id")
        wallet_address = payload.get("wallet_address")
        signature = payload.get("signature")
        chain_id = payload.get("chain_id")

        if (
            moralis_id is None
            or wallet_address is None
            or signature is None
            or chain_id is None
            or id is None
        ):
            raise credentials_exception

        # Check if token has expired
        expiration_timestamp = payload.get("exp")
        if (
            expiration_timestamp is None
            or datetime.fromtimestamp(expiration_timestamp) < datetime.now()
        ):
            raise credentials_exception

        token_data = TokenDataRequest(
            id=id,
            moralis_id=moralis_id,
            signature=signature,
            chain_id=chain_id,
            wallet_address=wallet_address,
        )

    except JWTError:
        raise credentials_exception

    user = authenticate_user(token_data)
    if not user:
        raise credentials_exception

    return user


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, env.JWT_SECRET, algorithm=env.JWT_ALGORITHM)

    return encoded_jwt
