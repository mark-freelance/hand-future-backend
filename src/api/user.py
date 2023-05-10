from typing import List

from fastapi import APIRouter

from src.ds.user import UserModel
from src.libs.db import coll_user
from src.libs.log import getLogger

user_router = APIRouter(prefix='/user', tags=['user'])

logger = getLogger('user-router')


@user_router.get("/", response_model=List[UserModel])
async def list_users():
    """
    todo: add more restriction on return (what about dynamic data structure ? should we separate tables ?)

    """
    return list(coll_user.find())


@user_router.get("/{user_id}", response_model=UserModel | None)
async def get_user(user_id: str):
    """
    todo: add more restriction on return (what about dynamic data structure ? should we separate tables ?)

    """
    return coll_user.find_one({"_id": user_id})


@user_router.patch(
    '/update',
    description="""
partial update, ref: https://fastapi.tiangolo.com/tutorial/body-updates/

理论上不可修改 username、password、email，其他的可以更改

~~cancelled: do more restriction~~

升级：允许对任意子表进行修改（例如 SYS，基于另一个项目），这样就不方面做很多限制了
    """
)
async def update_user(data: UserModel):
    data = coll_user.find_one_and_update(
        {"_id": data.id},
        {"$set": data.dict(exclude_unset=True, exclude_defaults=True)},
        upsert=True,
        return_document=True
    )
    return data
