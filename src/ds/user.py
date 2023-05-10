from enum import Enum

from src.ds.hero import HeroModel


class RoleType(str, Enum):
    user = 'user'
    admin = 'admin'


class UserModel(HeroModel):
    role: RoleType = RoleType.user


class UserInDBModel(UserModel):
    hashed_password: str

    register_time: int
    activated: bool = False
    activation_code: str
