from __future__ import annotations

from typing import List

from pydantic import BaseModel

from src.ds.user import HeroModel


class LinkModel(BaseModel):
    source: str
    target: str


class GraphData(BaseModel):
    nodes: List[HeroModel]
    links: List[LinkModel]
