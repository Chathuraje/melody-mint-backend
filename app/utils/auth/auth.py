from app.utils.database import user_collection
from fastapi import HTTPException, Depends
from app.models.Users import User
from fastapi import HTTPException, Depends
from app.models.Users import User, TokenData
from fastapi.security import OAuth2PasswordBearer
from app.utils import config
from jose import jwt, JWSError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user_by_wallet(wallet_address: str):
    user = user_collection.find_one({"wallet_address": wallet_address})
    
    if user:
        user["_id"] = str(user["_id"])
        return user
    
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])
        wallet_address: str = payload.get("sub")
        if wallet_address is None:
            raise credentials_exception
        token_data = TokenData(**payload)
    except JWSError:
        raise credentials_exception
    user = await get_user_by_wallet(wallet_address=token_data.wallet_address)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user