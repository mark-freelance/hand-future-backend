from enum import Enum
from typing import List, Dict

from fastapi import APIRouter, Body
from pydantic import BaseModel, Field

from api.hero.notion import initHeroesFromNotion, parseHeroesInfo
from db import coll_hero

hero_router = APIRouter(prefix="/hero", tags=["hero"])


class Sex(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class HeroModel(BaseModel):
    id: str
    name: str
    sex: Sex
    title: str
    desc: str
    avatar: str

    class Config:
        schema_extra = {
            "example": {
                "id": "suyang@gkleifeng.com",
                "name": '苏阳',
                "sex": Sex.MALE,
                "avatar": '/Users/mark/Projects/HandFuture/website/2.12 分享卡片设计文件夹(_F)/Links/苏阳_avatar.jpg',
                "title": '杰出的民族摇滚音乐家、当代艺术家',
                "desc": '他将“花儿”、“秦腔”等西北民间音乐及传统曲艺形式，与流行音乐进行嫁接、改良和解构，经由西方现代音乐的理论和手法，创造出一种全新的音乐语言。',
            }
        }


@hero_router.post("/update_basic")
def update_basic(data: HeroModel):
    result = coll_hero.update_one(
        {"id": data.id},
        {"$set": {
            "name": data.name,
            "sex": data.sex,
            "title": data.title,
            "desc": data.desc,
            "avatar": data.avatar
        }},
        upsert=True
    )
    return result.raw_result


@hero_router.get("/list")
def get_list() -> Dict:
    data = list(coll_hero.find({}, {"_id": False}))
    return {
        "size": data.__len__(),
        "list": data
    }


@hero_router.get("/init")
def get_init_list() -> Dict:
    """
    todo: use raw (but should query the list)
    :return:
    """
    raw_data = initHeroesFromNotion()
    data = parseHeroesInfo(raw_data)
    return {
        "size": data.__len__(),
        "list": data
    }
