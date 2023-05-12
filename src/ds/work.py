from enum import Enum
from typing import List

from pydantic import BaseModel

from src.ds.mongo import MongoModel, ID


class WorkType(str, Enum):
    image = "image"
    text = "text"
    bilibiliVideo = "bilibiliVideo"
    wechatArticle = "wechatArticle"
    others = "others"


class TypographyLayoutType(str, Enum):
    typography_plain = 'typography_plain',
    typography_horizontal_bg = 'typography_horizontal_bg',
    typography_horizontal = 'typography_horizontal',
    typography_vertical = 'typography_vertical',


class SourcePlatformType(str, Enum):
    plain = 'plain',
    bilibiliVideo = 'bilibiliVideo',
    wechatArticle = 'wechatArticle',


class WorkSourceModel(BaseModel):
    platform: SourcePlatformType
    url: str = None


class WorkModel(MongoModel):
    user_id: ID
    layout: TypographyLayoutType
    title: str
    cover: str
    description: str
    content: str
    connections: List[str]
    source: WorkSourceModel
