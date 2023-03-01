from fastapi import APIRouter, HTTPException
from starlette import status

from packages.wechat.article import parse_wechat_article

wechat_router = APIRouter(prefix="/wechat", tags=["wechat"])


@wechat_router.get("/article")
async def get_from_wechat_article(url: str):
    try:
        return parse_wechat_article(url)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"Invalid URL !"
        )
