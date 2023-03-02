import time

from pydantic import BaseModel, HttpUrl, validator


class BaseEventModel(BaseModel):
    timestamp: float

    @validator('timestamp')
    def time_should_latest(cls, v):
        cur_time = time.time()
        # 这里的校验，不但会在 create 时执行，还会在 query 时执行
        if not 0 < v < cur_time:
            raise ValueError(f'invalid timestamp: {v}, current: {cur_time}')
        return v


class BillModel(BaseEventModel):
    activity_name: str
    action: str
    points: int


class ChargeModel(BaseEventModel):
    points: int


class ActivityModel(BaseEventModel):
    activity_name: str
    organizer_name: str
    picture_url: HttpUrl  # ref: https://docs.pydantic.dev/usage/types/#urls
    description: str
