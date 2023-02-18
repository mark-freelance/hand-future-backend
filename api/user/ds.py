from typing import Union

from pydantic import BaseModel


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    nickname: Union[str, None] = None


class UserSocial(BaseModel):
    following: int = 0
    followed: int = 0
    likes: int = 0


class UserProfile(User):
    avatar: str = ''
    social: UserSocial


class UserInDB(UserProfile):
    hashed_password: str
    activated: bool
    activation_code: str
    register_time: float
