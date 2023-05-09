from datetime import timedelta, datetime
from typing import Union

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from starlette import status

from src.ds.user import TokenData, UserInDB
from src.libs.db import coll_user
from src.libs.env import ENV_SECRET_KEY, ENV_SECURITY_ALGO
from src.libs.log import getLogger

logger = getLogger("Auth")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")  # specify token path, !important


def verify_password(plain_password, hashed_password):
    result = pwd_context.verify(plain_password, hashed_password)
    logger.info({"plain_password": plain_password, "hashed_password": hashed_password, "verify_result": result})
    return result


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str):
    user = coll_user.find_one({"_id": username})
    if user:
        return UserInDB(**user)


def authenticate_user(username: str, password: str):
    logger.info(f"authenticating username={username}, password={password}")
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_authed_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, ENV_SECRET_KEY, algorithms=[ENV_SECURITY_ALGO])
        username: str = payload.get("sub")
        if username is None:
            logger.warning(f'[401] username in payload is None')
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        logger.warning(f'[401] JWTError')
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        logger.warning(f'[401] username in database is None')
        raise credentials_exception
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, ENV_SECRET_KEY, algorithm=ENV_SECURITY_ALGO)
    return encoded_jwt
