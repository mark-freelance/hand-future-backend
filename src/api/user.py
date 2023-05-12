from fastapi import APIRouter

from src.ds.hero import PyObjectId
from src.ds.user import UserModel
from src.libs.db import coll_user
from src.libs.log import getLogger

user_router = APIRouter(prefix='/user', tags=['user'])

logger = getLogger('user-router')

KEY_USER_ID = 'email'  # 受限于 next-auth + EmailProvider + mongodb-adapter


@user_router.get("/", response_model=UserModel | None)
async def get_user(id: PyObjectId = None, email: str = None):
    """
    todo: add more restriction on return (what about dynamic data structure ? should we separate tables ?)

    """
    query = {}
    if id:
        query['_id'] = id
    if email:
        query["email"] = email
    return coll_user.find_one(query)


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
        {KEY_USER_ID: data.email},
        {"$set": data.dict(exclude_unset=True, exclude_defaults=True)},
        upsert=True,
        return_document=True
    )
    return data
