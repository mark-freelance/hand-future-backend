from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from api.ld.ds import BillModel, ChargeModel
from api.user.ds import User
from api.user.utils import get_authed_user
from packages.general.db import db, coll_user

ld_bills_router = APIRouter(prefix='/bills', tags=['ld'])

coll_ld_bills = db['ld_bills']
FIELD_LD_POINT_BALANCE = "ld_points"


@ld_bills_router.get('/')
def get_current_points(user: User = Depends(get_authed_user)):
    return coll_user.find_one({"_id": user.username}).get(FIELD_LD_POINT_BALANCE, 0)


@ld_bills_router.get('/list', response_model=List[BillModel])
def get_bills(user: User = Depends(get_authed_user)):
    data = list(coll_ld_bills.find({"username": user.username}))
    return data


@ld_bills_router.post('/charge')
def charge_bills(charge_model: ChargeModel, user: User = Depends(get_authed_user)):
    # todo: add charge history
    return coll_user.find_one_and_update(
        {"_id": user.username},
        {"$inc": {FIELD_LD_POINT_BALANCE: charge_model.points}},
        return_document=True
    )[
        FIELD_LD_POINT_BALANCE]


@ld_bills_router.post('/redeem')
def redeem(bill: BillModel, user: User = Depends(get_authed_user), cur_points: int = Depends(get_current_points)):
    if bill.points > cur_points:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Failed to redeem this product since you have not enough points!"
        )
    coll_ld_bills.insert_one(dict(**bill.dict(), username=user.username))
    return coll_user.find_one_and_update(
        {"_id": user.username},
        {"$inc": {FIELD_LD_POINT_BALANCE: -bill.points}},
        return_document=True
    )
