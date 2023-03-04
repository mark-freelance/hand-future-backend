import json
import os
from datetime import datetime
from pprint import pprint
from typing import List
from urllib.parse import quote

from api.hero.ds import NotionHeroModel
from config import NOTION_COOKIE, NOTION_COL_MAP
from log import getLogger
from packages.general.re import parse_p1
from packages.general.session import session
from path import CACHE_DATA_DIR

logger = getLogger("notion")


def get_notion_avatar_url(user_id: str, avatar_uri: str) -> str:
    """
    quote(s: str) 不会转义 /，结合 safe 参数可以，ref: https://www.urlencoder.io/python/

    :param user_id:
    :param avatar_uri:
    :return:
    """
    return 'https://gkleifeng.notion.site/image/' + quote(avatar_uri, safe='') + \
        f'?table=block&id={user_id}&spaceId=5a775ac8-377b-4c22-918d-36dd67f5e3a2&width=600&userId=&cache=v2'


def crawl_notion_heroes():
    data = {
        'source': {
            'type': 'collection',
            'id': '151215d5-10a7-494d-96cd-5bf7b2bff3b6',
            'spaceId': '5a775ac8-377b-4c22-918d-36dd67f5e3a2'
        },
        'collectionView': {
            'id': '465c7d46-9ce6-40df-8fb4-77875b3e7dca',
            'spaceId': '5a775ac8-377b-4c22-918d-36dd67f5e3a2'
        },
        'loader': {
            'type': 'reducer',
            'reducers': {
                'collection_group_results': {'type': 'results', 'limit': 100},
                'table:uncategorized:title:count': {
                    'type': 'aggregation',
                    'aggregation': {'property': 'title', 'aggregator': 'count'}
                },
                'table:uncategorized:XoE{:unique': {
                    'type': 'aggregation',
                    'aggregation': {'property': 'XoE{', 'aggregator': 'unique'}
                }
            },
            'sort': [],
            'searchQuery': '',
            'userTimeZone': 'Asia/Shanghai'
        }
    }

    res = session.post(
        'https://gkleifeng.notion.site/api/v3/queryCollection?src=reset',
        json=data,
        headers={'Cookie': NOTION_COOKIE},
    )

    data = res.json()
    # 持久化方便复查
    with open(os.path.join(CACHE_DATA_DIR, f"notin_users_{datetime.now().isoformat()}.json"), "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return data


def parse_notion_heroes_info(data) -> List[NotionHeroModel]:
    coll_id = '151215d5-10a7-494d-96cd-5bf7b2bff3b6'  # this will be used in later parse on property key map
    property_key_map = data['recordMap']['collection'][coll_id]['value']['schema']

    raw_items = data['recordMap']['block'].items()
    items: List[NotionHeroModel] = []
    for user_id, user_data in raw_items:

        # 这些应该是空行！
        # self.assertIn('properties', user_data['value'])
        if 'properties' not in user_data['value']: continue

        item = {}
        for key, vals in user_data['value']['properties'].items():
            if key in property_key_map:
                item[property_key_map[key]['name']] = vals  # 编码列 --> 可读列

        try:
            notion_hero_model = NotionHeroModel(
                avatar='',
                id=user_id,
                name=parse_p1(r'([\u4e00-\u9fa5]+)', item[NOTION_COL_MAP["name"]]),
                avatar_notion=get_notion_avatar_url(
                    user_id,
                    parse_p1(r"(http.*?)'", item[NOTION_COL_MAP["avatar"]])
                ),
                title=parse_p1(r'([\u4e00-\u9fa5]+)', item.get(NOTION_COL_MAP["title"])),
                cities=parse_p1(r'([\u4e00-\u9fa5]+)', item.get(NOTION_COL_MAP["cities"]))
            )
            items.append(notion_hero_model)
        except Exception as e:
            # pprint(item)
            pass
    logger.info({"stat": {"raw_times": len(raw_items), "parsed": len(items)}})
    return items


if __name__ == '__main__':
    data = parse_notion_heroes_info(crawl_notion_heroes())
    pprint(data)
