from enum import Enum

from pydantic import BaseModel, HttpUrl, Field


class BillActionType(str, Enum):
    charge = 'charge'
    redeem_product = 'redeem_product'
    collect_activity = 'collect_activity'


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
    picture_url: HttpUrl = Field(
        ...,
        # ref: https://fastapi.tiangolo.com/tutorial/schema-extra-example/#field-additional-arguments
        example='https://tailwindcss.com/_next/static/media/tailwindcss-mark.79614a5f61617ba49a0891494521226b.svg'
    )
    points: int


class ProductModel(BaseEventModel):
    product_name: str
    picture_url: HttpUrl = Field(
        ...,
        # ref: https://fastapi.tiangolo.com/tutorial/schema-extra-example/#field-additional-arguments
        example='https://tailwindcss.com/_next/static/media/tailwindcss-mark.79614a5f61617ba49a0891494521226b.svg'
    )
    description: str
    price: float


class RedeemProductModel(BaseEventModel):
    product_id: str


class CollectActivityModel(BaseEventModel):
    activity_id: str
