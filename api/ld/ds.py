from enum import Enum

from pydantic import BaseModel, HttpUrl, Field


class BillActionType(str, Enum):
    charge = 'charge'
    redeem = 'redeem'


class BaseEventModel(BaseModel):
    class Config:
        use_enum_values = True  # ref: https://stackoverflow.com/a/65211727/9422455


class BillModel(BaseEventModel):
    action: BillActionType
    change: int
    detail: dict = None


class ActivityModel(BaseEventModel):
    activity_name: str
    organizer_name: str
    description: str


class ProductModel(BaseEventModel):
    activity_name: str
    organizer_name: str
    picture_url: HttpUrl = Field(
        ...,
        # ref: https://fastapi.tiangolo.com/tutorial/schema-extra-example/#field-additional-arguments
        example='https://tailwindcss.com/_next/static/media/tailwindcss-mark.79614a5f61617ba49a0891494521226b.svg'
    )
    description: str
    price: float


class TradedProductModel(BaseEventModel):
    product_id: str
