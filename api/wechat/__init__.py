from fastapi import APIRouter

from packages.wechat.article import parse_wechat_article

wechat_router = APIRouter(prefix="/wechat", tags=["wechat"])


@wechat_router.get("/article")
async def get_from_wechat_article(url: str):
    return parse_wechat_article(url)
