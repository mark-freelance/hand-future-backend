from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, Query, Body

from src.ds.user import User
from src.libs.auth import get_authed_user, get_user
from src.libs.db import db, coll_user, coll_hero_user
from src.libs.log import getLogger

user_router = APIRouter(prefix='/user', tags=['user'])

logger = getLogger('user-router')


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


@user_router.patch('/update')
async def update_user(
        coll_name: str = Query('user'),
        data: dict = Body(...),
        user: User = Depends(get_authed_user)
):
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
    return data


@user_router.put('/set_role')
def set_role(username: str, role: str):
    user = get_user(username)
    if not user:
        raise HTTPException(404)
    return coll_user.find_one_and_update({"_id": username}, {"$set": {"role": role}}, return_document=True)


@user_router.get("/")
def get_single(id: str) -> Dict:
    data = coll_hero_user.find_one({"_id": id})
    if not data:
        raise HTTPException(status_code=404, detail='id not exists')
    return data
