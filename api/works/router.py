from fastapi import APIRouter

from api.works.ds import IWork
from packages.general.db import coll_work

works_router = APIRouter(prefix="/works", tags=["works"])


@works_router.get('/')
async def get_collection_of_works(user_id: str):
    return list(coll_work.find({"user_id": user_id}))


@works_router.patch('/update')
async def update_work(work: IWork):
    work_dict = work.dict(exclude_unset=True)
    work_dict['_id'] = work_dict["id"]
    return coll_work.find_one_and_update(
        {"_id": work_dict["_id"]},
        {"$set": work_dict},
        return_document=True,
        upsert=True
    )


@works_router.delete('/')
async def delete_work(id: str):
    return coll_work.delete_one({"_id": id}).raw_result
