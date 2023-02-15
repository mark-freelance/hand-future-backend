from pprint import pprint
from typing import List, TypedDict

from pydantic import BaseModel

from log import getLogger
from packages.general.re import parse_p1
from session import session

logger = getLogger("notion")


def initHeroesFromNotion():
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
        headers={
            'Cookie':
                'notion_browser_id=ee0024cf-69ba-452f-8b2e-aee3ac87fc25; intercom-id-gpfdrxfd=d072f01b-ec07-4e0a-8790-8c5735d46497; intercom-device-id-gpfdrxfd=54b4c53d-f4de-4ec2-a9f9-aca5640eabc4; intercom-session-gpfdrxfd=; notion_check_cookie_consent=false; __cf_bm=mXmsTZyOCNbeA5vtjpbTt6AzwXRCutaWn4l2POVinmA-1676470443-0-Ac4TUhTOuPhmaSFYtoevUDjRbBbxI0HccHqmCAKpnrYffK2TY/OBLY6uqLa+A6s3KAFGrGkVAt37WQPgoZXkQfY=; amp_af43d4=ee0024cf69ba452f8b2eaee3ac87fc25...1gpabddt6.1gpamrb1l.ji.8.jq',
        },
    )
    return res.json()


class UserBasicModel(TypedDict):
    user_id: str
    name: str
    avatar: str
    title: str


def parseHeroesInfo(data) -> List[UserBasicModel]:
    # logger.info(data)
    collectionId = '151215d5-10a7-494d-96cd-5bf7b2bff3b6'  # this will be used in later parse on property key map
    propertyKeyMap = data['recordMap']['collection'][collectionId]['value']['schema']
    # pprint(propertyKeyMap)

    items = []
    for user_id, user_data in data['recordMap']['block'].items():
        pprint({"user_id": user_id, "user_data": user_data})
        if 'properties' not in user_data['value']: continue
        item = {}
        for key, vals in user_data['value']['properties'].items():
            if key in propertyKeyMap:
                item[propertyKeyMap[key]['name']] = vals  # 编码列 --> 可读列

        targetItem = {}
        targetItem['user_id'] = user_id
        targetItem['name'] = parse_p1(r'([\u4e00-\u9fa5]+)', str(item.get('嘉宾姓名', ''))) or ""
        targetItem['avatar'] = parse_p1(r"(http.*?)'", str(item.get('照片', ''))) or ''
        targetItem['title'] = parse_p1(r'([\u4e00-\u9fa5]+)', str(item.get("title", ''))) or ''
        if targetItem['name'] and targetItem['avatar'] and targetItem['title']:
            items.append(targetItem)
    return items


if __name__ == '__main__':
    data = parseHeroesInfo(initHeroesFromNotion())
    pprint(data)
