from typing import List, TypedDict, Set

from fastapi import APIRouter

from api.hero.router import get_heroes_list
from packages.general.db import db

heroes2_router = APIRouter(prefix='/heroes2', tags=['heroes2'])

coll_heroes2 = db['heroes2']


class GraphLink(TypedDict):
    source: str
    target: str


class GraphData(TypedDict):
    nodes: List[dict]
    links: List[GraphLink]


AVATAR_MAP = {}


def init_avatars():
    for hero in get_heroes_list():
        AVATAR_MAP[hero['id']] = hero['avatar']


@heroes2_router.get('/graph_data')
def get_graph_data():
    init_avatars()

    items = list(coll_heroes2.find(
        {"$expr": {"$gt": [{"$size": "$properties.照片.files"}, 0]}},
        {
            "_id": 0,
            "id": 1,
            # ref: https://stackoverflow.com/a/39196636/9422455
            "notion_avatar": {"$first": "$properties.照片.files.file.url"},
            "name": {"$first": "$properties.嘉宾姓名.title.plain_text"},
            "relations": "$properties.携手嘉宾.relation.id",
        }
    )
    )

    ids: Set[str] = set()
    nodes: List[dict] = []
    links: List[GraphLink] = []
    for item in items:
        id = item['id']
        if id in AVATAR_MAP:
            item['avatar'] = AVATAR_MAP[id]
            ids.add(id)
            relations = item.pop("relations")
            nodes.append(item)
            for relation in relations:
                # links中的结点由于被筛选可能不存在
                if relation in ids:
                    links.append({"source": item['id'], "target": relation})

    graph_data: GraphData = {
        "nodes": nodes,
        "links": links
    }
    # print(graph_data)
    return graph_data


if __name__ == '__main__':
    get_graph_data()
