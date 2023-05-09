from __future__ import annotations

from typing import Optional, List

from pydantic import BaseModel


class HeroModel(BaseModel):
    id: str
    name: Optional[str]
    is_hero: Optional[bool] = False

    # hero
    avatar: Optional[str]
    title: Optional[str]
    cities: Optional[str]
    partners: Optional[List[str]]
