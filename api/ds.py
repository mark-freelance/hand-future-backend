"""
generic ref: https://stackoverflow.com/a/71682732/9422455
"""

from typing import Any, TypeVar, Generic, List

from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T", int, str)

STATUS_OK = "ok"
STATUS_ERROR = "error"


class BaseResSuccessModel(GenericModel, Generic[T]):
    status = STATUS_OK
    data: T


class BaseResFailModel(BaseModel):
    status = STATUS_ERROR
    msg: str


class ListDataModel(GenericModel, Generic[T]):
    size: int
    data: List[T]


ListResModel = BaseResSuccessModel[ListDataModel]
