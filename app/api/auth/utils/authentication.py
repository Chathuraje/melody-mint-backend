from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, security
from jose import JWTError, jwt
from app.api.user.utils.UserDbController import get_user_by_wallet_address
from app.model.Auth import TokenData
from app.utils.config import JWT_ALGORITHM, JWT_EXPIRY_MINUTES, JWT_SECRET


oauth2_bearer = security.OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


def authenticate_user(token_data: TokenData):
    user = get_user_by_wallet_address(token_data.wallet_address, token_data.chain_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        moralis_id = payload.get("moralis_id")
        wallet_address = payload.get("wallet_address")
        signature = payload.get("signature")
        chain_id = payload.get("chain_id")

        if (
            moralis_id is None
            or wallet_address is None
            or signature is None
            or chain_id is None
        ):
            raise credentials_exception

        token_data = TokenData(
            moralis_id=moralis_id,
            signature=signature,
            chain_id=chain_id,
            wallet_address=wallet_address,
        )

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user_by_wallet_address(token_data.wallet_address, token_data.chain_id)
    if user is None:
        raise credentials_exception

    return user


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return encoded_jwt
