from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.utils import config
from app.utils.auth import auth

ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta is not None:
        expire = datetime.utcnow() + timedelta(expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)
    return encoded_jwt

def authenticate_user(wallet_address: str, password: str):
    user = auth.get_user_by_wallet(wallet_address)
    if not user:
        return False
    if not verify_password(password, user["hash_password"]):
        return False
    return user