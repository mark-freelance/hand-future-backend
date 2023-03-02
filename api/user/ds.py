from typing import Union, Optional

from pydantic import BaseModel


class TokenData(BaseModel):
    username: str = None


class User(BaseModel):
    username: str = None
    email: str = None
    nickname: str = None


class UserSocial(BaseModel):
    following: int = 0
    followed: int = 0
    likes: int = 0


class UserProfile(User):
    avatar: str = None
    social: Optional[UserSocial]
    role: str = None


class UserInDB(UserProfile):
    hashed_password: str
    activated: bool
    activation_code: str
    register_time: float

    # ld_admin project
    ld_point_balance: int = 0
