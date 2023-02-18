from enum import Enum

from pydantic import BaseModel


class WorkType(str, Enum):
    image = "image"
    text = "text"
    bilibiliVideo = "bilibiliVideo"
    wechatArticle = "wechatArticle"
    others = "others"


class Work(BaseModel):
    type: WorkType
    content: str

    class Config:
        schema_extra = {
            "example": {
                "type": WorkType.bilibiliVideo,
                "content": "https://www.bilibili.com/video/BV11Y411i76T/"
            }
        }
