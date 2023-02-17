from typing import Union

from pydantic import BaseModel


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    nickname: Union[str, None] = None


class UserInDB(User):
    hashed_password: str
    disabled: Union[bool, None] = None
    activation_code: str


class UserProfile(User):
    avatar: str = ''
