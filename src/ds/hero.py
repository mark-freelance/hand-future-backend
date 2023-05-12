from __future__ import annotations

from typing import Optional, List

from bson import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    """
    ref: https://www.mongodb.com/developer/languages/python/python-quickstart-fastapi/
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class HeroModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    name: Optional[str]
    is_hero: Optional[bool] = False

    # hero
    avatar: Optional[str]
    title: Optional[str]
    cities: Optional[str]
    partners: Optional[List[str]]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True  # required for the _id
        json_encoders = {ObjectId: str}  # ref: https://stackoverflow.com/a/68580662/9422455
