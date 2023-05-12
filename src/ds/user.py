from __future__ import annotations

from enum import Enum
from typing import Optional, List

from src.ds.mongo import MongoModel


class RoleType(str, Enum):
    user = 'user'
    admin = 'admin'


class HeroModel(MongoModel):
    name: Optional[str]
    is_hero: Optional[bool] = False

    # hero
    avatar: Optional[str]
    cover: Optional[str]
    title: Optional[str]
    cities: Optional[str]
    partners: Optional[List[str]]


class UserModel(HeroModel):
    email: Optional[str]
    role: Optional[RoleType] = RoleType.user


class UserInDBModel(UserModel):
    hashed_password: str

    register_time: int
    activated: bool = False
    activation_code: str
