import time

from fastapi import APIRouter, Depends

from api.ld.ds import BillModel, BillActionType
from api.user.ds import User
from api.user.utils import get_authed_user
from packages.general.db import db, coll_user

ld_bills_router = APIRouter(prefix='/bills', tags=['ld'])

coll_ld_bills = db['ld_bills']
FIELD_LD_BALANCE = "ld_balance"


@ld_bills_router.get('/current', tags=['authentication'])
def get_current_balance(user: User = Depends(get_authed_user)):
    return coll_user.find_one({"_id": user.username}).get(FIELD_LD_BALANCE, 0)


@ld_bills_router.get('/list', tags=['authentication'])
def get_bill_history(action=None, user: User = Depends(get_authed_user)):
    return list(coll_ld_bills.find({"username": user.username, "action": action}))


@ld_bills_router.post('/charge', tags=['authentication'])
def charge_account(points: int, user: User = Depends(get_authed_user)):
    bill = BillModel(action=BillActionType.charge, change=points, detail={})
    return add_bill_record(bill, user)


@ld_bills_router.post('/add_record', tags=['authentication'])
def add_bill_record(bill: BillModel, user: User = Depends(get_authed_user)):
    cur_balance = get_current_balance(user)
    new_balance = cur_balance + bill.change

    # sync with user balance
    coll_user.update_one(
        {"_id": user.username},
        {"$set": {FIELD_LD_BALANCE: new_balance}},
    )

    # add bill record
    return coll_ld_bills.insert_one(dict(**bill.dict(), balance=new_balance, username=user.username)).inserted_id
