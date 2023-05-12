from fastapi import APIRouter, HTTPException

from src.ds.mongo import ID
from src.ds.user import UserModel
from src.libs.db import coll_user
from src.libs.log import getLogger

user_router = APIRouter(prefix='/user', tags=['user'])

logger = getLogger('user-router')


@user_router.get(
    "/",
    response_model=UserModel | None,
    response_model_by_alias=False,  # ref:https://stackoverflow.com/a/69679104/9422455
)
async def get_user(id: ID = None, email: str = None):
    """
    todo: add more restriction on return (what about dynamic data structure ? should we separate tables ?)

    """
    if not id and not email:
        raise HTTPException(406, detail='id 和 email 至少要有一个作为筛选条件')
    query = {}
    if id:
        query['_id'] = id
    if email:
        query["email"] = email
    return coll_user.find_one(query)


@user_router.patch(
    '/update',
    response_model=UserModel,
    response_model_by_alias=False,
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
    print("updated_user: ", data)
    return data
