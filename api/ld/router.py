from fastapi import APIRouter

from api.ld.ld_activities import ld_activities_router
from api.ld.ld_bills import ld_bills_router
from api.ld.ld_products import ld_products_router

ld_router = APIRouter(prefix='/ld', tags=['ld'])

ld_router.include_router(ld_bills_router)
ld_router.include_router(ld_activities_router)
ld_router.include_router(ld_products_router)
