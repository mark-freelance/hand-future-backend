import time
from typing import List

from fastapi import APIRouter

from api.ld.ds import ActivityModel
from packages.general.db import db

ld_activities_router = APIRouter(prefix='/activities', tags=['ld'])

coll_ld_activities = db['ld_activities']


@ld_activities_router.get('/all', tags=['open'])
def show_all_activities():
    return list(coll_ld_activities.find({}))


@ld_activities_router.post('/add', tags=['open'])
def add_activity(activity: ActivityModel):
    return coll_ld_activities.insert_one(dict(**activity.dict(), timestamp=time.time())).inserted_id


@ld_activities_router.delete('/clear', tags=['open'])
def clear_activities():
    return coll_ld_activities.delete_many({}).raw_result
