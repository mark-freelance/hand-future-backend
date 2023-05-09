from __future__ import annotations

from typing import Optional, List

from pydantic import BaseModel


class HeroModel(BaseModel):
    id: str
    name: str
    avatar: Optional[str]
    title: Optional[str]
    cities: Optional[str]

    is_hero: bool = False
    partners: Optional[List[str]]


class NotionHeroModel(HeroModel):
    avatar_notion: str
