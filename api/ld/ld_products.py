import time
from typing import List

import uuid

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from api.ld.ds import ProductModel, BillModel, BillActionType, TradedProductModel
from api.ld.ld_bills import coll_ld_bills, add_bill_record
from api.user.ds import User, UserInDB
from api.user.utils import get_authed_user
from packages.general.db import db

ld_products_router = APIRouter(prefix='/products', tags=['ld'])

coll_ld_products = db['ld_products']

# since each product can be purchased by multiple users, we should separate in another table
coll_ld_products_traded = db['ld_products_traded']


@ld_products_router.get('/all', tags=['open'])
def show_all_products():
    return list(coll_ld_products.find({}))


@ld_products_router.get('/list', tags=['authentication'])
def get_my_products(user: User = Depends(get_authed_user)):
    """
    todo: do we need to return the detailed product info ?
    :param user:
    :return:
    """
    return list(coll_ld_products_traded.find({"username": user.username}))


@ld_products_router.post('/add', tags=['open'])
def add_product(product: ProductModel):
    return coll_ld_products.insert_one(product.dict()).inserted_id


@ld_products_router.delete('/clear', tags=['open'])
def clear_products():
    return coll_ld_products.delete_many({}).raw_result


@ld_products_router.post('/redeem', tags=['authentication'])
def redeem_product(trade: TradedProductModel, user: UserInDB = Depends(get_authed_user)):
    product_id_str = trade.product_id
    try:
        product_id = ObjectId(product_id_str)
    except InvalidId as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=e.args)

    print({"redeem": {"product_id": product_id_str, "username": user.username}})

    product = coll_ld_products.find_one({"_id": product_id})  # BsonID

    # check product exist (in case of frontend is passed)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail='Not exist product of id=' + product_id_str
        )

    # check product redeemed (in case of duplication)
    if coll_ld_products_traded.find_one({"username": user.username, "product_id": product_id_str}):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='You have redeemed this product')

    # check user balance
    price = product['price']
    if price > user.ld_balance:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="You have not enough points!")

    # do the trade
    coll_ld_products_traded.insert_one(dict(**trade.dict(), username=user.username))

    # sync with bill
    bill = BillModel(
        action=BillActionType.redeem,
        change=-price,
        detail=product
    )
    return add_bill_record(bill, user)
