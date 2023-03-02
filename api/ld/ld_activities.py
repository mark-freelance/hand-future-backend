from typing import List

from fastapi import APIRouter, Depends

from api.ld.ds import ActivityModel
from api.user.ds import User
from api.user.utils import get_authed_user
from packages.general.db import db

ld_activities_router = APIRouter(prefix='/activities', tags=['ld'])

coll_ld_activities = db['ld_activities']


@ld_activities_router.get('/list', response_model=List[ActivityModel])
def get_activities(user: User = Depends(get_authed_user)):
    data = list(coll_ld_activities.find({"username": user.username}))
    return data


@ld_activities_router.post('/add')
def add_activity(activity: ActivityModel, user: User = Depends(get_authed_user)):
    return coll_ld_activities.insert_one(dict(**activity.dict(), username=user.username)).inserted_id


@ld_activities_router.delete('/clear')
def clear_activities(user: User = Depends(get_authed_user)):
    return coll_ld_activities.delete_many({}).raw_result
