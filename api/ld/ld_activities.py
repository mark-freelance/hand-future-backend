import time

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from api.ld.ds import ActivityModel, CollectActivityModel, BillModel, BillActionType
from api.ld.ld_bills import add_bill_record, coll_ld_bills
from api.user.ds import UserInDB, User
from api.user.utils import get_authed_user
from packages.general.db import db

ld_activities_router = APIRouter(prefix='/activities', tags=['ld'])

coll_ld_activities = db['ld_activities']


@ld_activities_router.get('/all', tags=['open'])
def show_all_activities():
    return list(coll_ld_activities.find({}))


@ld_activities_router.get('/list', tags=['authentication'])
def get_my_activities(user: User = Depends(get_authed_user)):
    return list(coll_ld_bills.find({"username": user.username, "action": BillActionType.collect_activity}))


@ld_activities_router.post('/add', tags=['open'])
def add_activity(activity: ActivityModel):
    return coll_ld_activities.insert_one(dict(**activity.dict(), timestamp=time.time())).inserted_id


@ld_activities_router.delete('/clear', tags=['open'])
def clear_activities():
    return coll_ld_activities.delete_many({}).raw_result


@ld_activities_router.post('/collect', tags=['authentication'])
def collect_activity(trade: CollectActivityModel, user: UserInDB = Depends(get_authed_user)):
    activity_id_str = trade.activity_id
    try:
        activity_id = ObjectId(activity_id_str)
    except InvalidId as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=e.args)

    activity = coll_ld_activities.find_one({"_id": activity_id})  # BsonID

    # check product exist (in case of frontend is passed)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail='Not exist activity of id=' + activity_id_str
        )

    # check product redeemed (in case of duplication)
    if coll_ld_bills.find_one(
            {
                "username": user.username,
                "action": BillActionType.collect_activity,
                "detail._id": activity_id
            }
    ):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='You have collected this activity')

    # check user balance
    points = activity['points']

    # do the trade
    bill = BillModel(action=BillActionType.collect_activity, change=points, detail=activity)
    return add_bill_record(bill, user)
