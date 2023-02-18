"""
ref: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
"""
import time
from datetime import timedelta

from fastapi import Depends, HTTPException, status, APIRouter, Form
from fastapi.security import OAuth2PasswordRequestForm
from api.user.utils import get_password_hash, authenticate_user, create_access_token, get_authed_user

from config import SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES
from api.user.ds import User, UserInDB, UserProfile
from db import coll_user
from log import getLogger

from packages.general.rand import gen_random_activation_code
from packages.general.mail import MyMail

user_router = APIRouter(prefix="/user", tags=["user"])

my_mail = MyMail()
logger = getLogger("Auth")


@user_router.post('/register')
async def register(
        username: str = Form(...),
        password: str = Form(...),
        nickname: str = Form(...),
        email: str = Form(...)
):
    if coll_user.find_one({"username": username, "activated": True}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User has been existed!")

    # send email for validation
    code = gen_random_activation_code()
    my_mail.send_hand_future_activation_mail([email], code, "html")

    user_data = {
        "username": username,
        "hashed_password": get_password_hash(password),
        "nickname": nickname,
        "email": email,
        "avatar": '',
        "social": {
            "following": 0,
            "followed": 0,
            "likes": 0
        },
        "activated": False,
        "activation_code": code,
        "register_time": time.time(),
    }
    # validate user_data
    UserInDB(**user_data)
    coll_user.update_one({"username": username}, {"$set": user_data}, upsert=True)
    return True


@user_router.put('/activate')
async def activate(username: str = Form(...), code: str = Form(...)):
    user = coll_user.find_one({"username": username, "activated": False})
    # user 被抢先注册！
    if not user:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="You Account has been occupied, please consider re-register !"
        )
    if user["activation_code"] != code or user["register_time"] < time.time() - 60 * 10:  # 10 分钟
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Invalid / Incorrect Activation Code !"
        )
    coll_user.update_one(
        {"username": user["username"]},
        {"$set": {
            "activated": True,
            "activation_time": time.time()
        }},
        return_document=True
    )
    return True


@user_router.post("/token", description='要返回token字段，其他api要用')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    logger.info({"access_token": access_token})
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.get("/me", response_model=UserProfile)
async def read_user(user: User = Depends(get_authed_user)):
    return user


@user_router.post('/update')
async def update_user(data: UserProfile, user: User = Depends(get_authed_user)):
    """
    更新时不可修改 username、password、email
    其他的可以更改

    :param data:
    :param user:
    :return:
    """
    result = coll_user.update_one(
        {"username": user.username},
        {"$set": {
            "avatar": data.avatar,
            "nickname": data.nickname
        }
        })
    return result.raw_result
