from typing import List

from fastapi import APIRouter

from src.ds.mongo import ID
from src.ds.work import WorkModel
from src.libs.db import coll_work

works_router = APIRouter(prefix="/work", tags=["work"])


@works_router.get('/', response_model=List[WorkModel], response_model_by_alias=False)
async def get_collection_of_works(user_id: ID):
    return list(coll_work.find({"user_id": user_id}))


@works_router.post('/', response_model=ID)
async def create_work(work: WorkModel):
    print("update_work: ", work)
    return coll_work.insert_one(work.dict(exclude_unset=True), ).inserted_id


@works_router.patch('/', response_model=WorkModel, response_model_by_alias=False)
async def update_work(work: WorkModel):
    print("update_work: ", work)
    return coll_work.find_one_and_update(
        {"_id": work.id},
        {"$set": work.dict(exclude_unset=True)},
        return_document=True,
        upsert=True
    )


@works_router.delete('/')
async def delete_work(id: ID):
    return coll_work.delete_one({"_id": id}).raw_result
