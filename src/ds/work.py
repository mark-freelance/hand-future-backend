from enum import Enum
from typing import List

from pydantic import BaseModel


class WorkType(str, Enum):
    image = "image"
    text = "text"
    bilibiliVideo = "bilibiliVideo"
    wechatArticle = "wechatArticle"
    others = "others"


class TypographyLayout(str, Enum):
    typography_plain = 'typography_plain',
    typography_horizontal_bg = 'typography_horizontal_bg',
    typography_horizontal = 'typography_horizontal',
    typography_vertical = 'typography_vertical',


class SourcePlatform(str, Enum):
    plain = 'plain',
    bilibiliVideo = 'bilibiliVideo',
    wechatArticle = 'wechatArticle',


class WorkSource(BaseModel):
    platform: SourcePlatform
    url: str = None


class IWork(BaseModel):
    id: str
    user_id: str
    layout: TypographyLayout
    title: str
    cover: str
    description: str
    content: str
    connections: List[str]
    source: WorkSource
