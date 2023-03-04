"""
ref: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
"""
import os
import time
from datetime import timedelta
from typing import Any

from fastapi import Depends, HTTPException, status, APIRouter, Form, Query, Body
from fastapi.security import OAuth2PasswordRequestForm

from api.ds import BaseResSuccessModel, STATUS_OK
from api.user.utils import get_password_hash, authenticate_user, create_access_token, get_authed_user, get_user

from api.user.ds import User, UserInDB
from packages.general.db import coll_user, db
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
        email: str = Form(None),
        nickname: str = Form(None),
        avatar: str = Form(None),
        subject: str = Form(None)
):
    if coll_user.find_one({"username": username, "activated": True}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User has been existed!"
        )

    # send email for validation
    code = gen_random_activation_code()
    my_mail.send_hand_future_activation_mail([email], code, subject, "html")

    user_data = {
        "_id": username,
        "username": username,
        "hashed_password": get_password_hash(password),
        "nickname": nickname,
        "email": email,
        "avatar": avatar,
        "social": {
            "following": 0,
            "followed": 0,
            "likes": 0
        },
        "activated": False,
        "activation_code": code,
        "register_time": time.time(),

        "ld_point_balance": 0
    }
    # validate user_data
    UserInDB(**user_data)
    coll_user.update_one({"username": username}, {"$set": user_data}, upsert=True)
    return True


@user_router.post('/activate')
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
        {"_id": user["username"]},
        {"$set": {
            "activated": True,
            "activation_time": time.time()
        }},
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
    access_token_expires = timedelta(days=7)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    logger.info({"access_token": access_token})
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.get("/me")
async def read_user(user=Depends(get_authed_user)):
    """
    todo: add more restriction on return (what about dynamic data structure ? should we separate tables ?)

    :param user:
    :return:
    """
    return user


@user_router.get("/detail")
async def read_user(coll_name: str, user=Depends(get_authed_user)):
    """
    todo: add more restriction on return (what about dynamic data structure ? should we separate tables ?)

    :param coll_name:
    :param user:
    :return:
    """
    return db[coll_name].find_one({"_id": user.username})


@user_router.patch('/update', response_model=BaseResSuccessModel[Any])
async def update_user(coll_name: str = Query('user'), data: dict = Body(...), user: User = Depends(get_authed_user)):
    """
    partial update, ref: https://fastapi.tiangolo.com/tutorial/body-updates/

    理论上不可修改 username、password、email，其他的可以更改

    ~~cancelled: do more restriction~~

    升级：允许对任意子表进行修改（例如 SYS，基于另一个项目），这样就不方面做很多限制了

    :param coll_name: 更新一些其他表的信息

    :param data: ref: https://stackoverflow.com/a/65114346/9422455

    :param user:

    :return:
    """
    logger.info({"/user/update": {"coll_name": coll_name, "data": data}})
    data = db[coll_name].find_one_and_update(
        {"_id": user.username},
        {"$set": data},
        upsert=True,
        return_document=True
    )
    return {
        "status": STATUS_OK,
        "data": data
    }


@user_router.put('/set_role')
def set_role(username: str, role: str):
    user = get_user(username)
    if not user:
        raise HTTPException(status_code=404)
    return coll_user.find_one_and_update({"_id": username}, {"$set": {"role": role}}, return_document=True)
