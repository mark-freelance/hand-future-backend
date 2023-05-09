import json
import os
import time
from pprint import pprint
from typing import List

from fastapi import APIRouter, Query
from notion_client import Client
from notion_client.helpers import collect_paginated_api
from starlette.background import BackgroundTasks

from src.config.notion import NOTION_DATABASE_ID
from src.ds.graph import IGraphData
from src.ds.hero import HeroModel
from src.ds.notion import NotionModel
from src.libs.db import coll_hero_notion, coll_user
from src.libs.log import getLogger
from src.libs.path import CACHE_DIR

hero_router = APIRouter(prefix="/hero", tags=["hero"])

logger = getLogger("API_Hero")

AVATAR_MAP = {}


@hero_router.get('/', summary='heroes 是 users 的子集', response_model=List[HeroModel])
async def list_heroes():
    return list(coll_user.find({"is_hero": True}, {}))


@hero_router.post(
    "/init_from_notion",
    summary='todo: 该接口要限速',
)
async def init_heroes(
        bt: BackgroundTasks,
        use_dump_json=False,
        use_dump_db=True,
        fields: list[str] = Query(['id']),
) -> list[dict]:
    """
    todo: limit the rate

    :param use_dump_json:
    :param use_dump_db:
    :param fields:
    :return:
    """
    notion_token = os.environ["NOTION_TOKEN"]
    notion_database_id = NOTION_DATABASE_ID
    print({"notion_token": notion_token, "notion_database_id": notion_database_id})

    notion = Client(auth=notion_token)

    # full data
    # ref: https://github.com/ramnes/notion-sdk-py#utility-functions
    data = collect_paginated_api(notion.databases.query, database_id=notion_database_id)

    def dump_json():
        fp = os.path.join(CACHE_DIR, f'data-{time.time_ns()}.json')
        with open(fp, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            print(f'written into file://{fp}')

    def dump_db():
        for seq, item in enumerate(data):
            id = item['id']
            # update raw data, in order to save a full mirror
            coll_hero_notion.update_one({"_id": id}, {"$set": dict(**item, _id=id)}, upsert=True)

            pprint(item)
            notion_model = NotionModel.parse_obj(item)
            hero_model = notion_model.to_hero_model(bt)
            coll_user.update_one({"_id": id}, {"$set": dict(**hero_model.dict(exclude_unset=True), _id=id)},
                                 upsert=True)
            print(f'updated seq={seq + 1}, id={id}')

    if use_dump_json: dump_json()

    if use_dump_db: dump_db()

    return [{key: item[key] for key in fields} for item in data]


@hero_router.get(
    '/graph_data',
    description='直接读取 user 表里是notion hero的用户，并筛选有头像的，进行携手链接'
)
async def get_graph_data():
    nodes = list(coll_user.find({"avatar": {"$ne": None}, "is_hero": True}))
    ids = [i['id'] for i in nodes]
    links = []
    seen = set()  # 要去重
    for node in nodes:
        source = node['id']
        if source in ids:
            for link in node['partners']:
                if link in ids:
                    target = link
                    cur = ",".join(sorted([source, target]))
                    if cur not in seen:
                        seen.add(cur)
                        links.append({"source": source, "target": target})

    graph_data: IGraphData = {"nodes": nodes, "links": links}
    # print(graph_data)
    return graph_data
