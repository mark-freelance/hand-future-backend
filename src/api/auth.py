"""
ref: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
"""
import time
from datetime import timedelta

from fastapi import Depends, HTTPException, status, APIRouter, Form
from fastapi.security import OAuth2PasswordRequestForm

from src.ds.user import UserInDB
from src.libs.auth import get_password_hash, authenticate_user, create_access_token
from src.libs.db import coll_user
from src.libs.log import getLogger
from src.libs.mail import MyMail
from src.libs.rand import gen_random_activation_code

auth_router = APIRouter(prefix="/auth", tags=["auth"])

my_mail = MyMail()
logger = getLogger("Auth")


@auth_router.post('/register')
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


@auth_router.post('/activate')
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
        }
        },
    )
    return True


@auth_router.post("/token", description='要返回token字段，其他api要用')
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
