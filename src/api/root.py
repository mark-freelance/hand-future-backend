from fastapi import APIRouter

from src.api.auth import auth_router
from src.api.files import files_router
from src.api.hero import hero_router
from src.api.user import user_router
from src.api.wechat import wechat_router
from src.api.works import works_router

root_router = APIRouter()

root_router.include_router(auth_router)
root_router.include_router(user_router)
root_router.include_router(hero_router)
root_router.include_router(works_router)
root_router.include_router(wechat_router)
root_router.include_router(files_router)


@root_router.get("/")
async def root():
    return {"message": "Hello World"}
