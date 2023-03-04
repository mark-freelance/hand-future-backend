from pydantic import BaseModel


class HeroModel(BaseModel):
    id: str
    name: str
    avatar: str
    title: str = None
    cities: str = None


class NotionHeroModel(HeroModel):
    avatar_notion: str
