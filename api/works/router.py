from fastapi import APIRouter, Depends

from api.ds import BaseResSuccessModel, ListResModel, STATUS_OK
from api.user.utils import get_authed_user
from api.works.ds import Work
from packages.general.db import coll_work

works_router = APIRouter(prefix="/works", tags=["works"])


@works_router.get('/', response_model=ListResModel[Work])
async def get_collection_of_works(username: str):
    data = list(coll_work.find({"username": username}))
    return {
        "status": STATUS_OK,
        "data": {
            "size": len(data),
            "data": data
        }
    }


@works_router.post('/add', response_model=BaseResSuccessModel[str])
async def post_work(work: Work, user=Depends(get_authed_user)):
    data = {"username": user.username, **work.dict()}
    res = coll_work.insert_one(data)
    return {
        "status": STATUS_OK,
        "data": str(res.inserted_id)
    }
