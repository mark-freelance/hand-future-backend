# quote avatar in db in case of CORS problem
from urllib.parse import quote, unquote

from packages.general.db import coll_hero

"""
用以解决当时文件命名没有 `quote` 导致的 image uri 无法被前端顺利访问（CORS）的问题：
 http://gkleifeng.com:3001/files/e28f823e-b064-11ed-aafd-5783702bc47d_%E5%91%A8%E6%A6%95.png
"""

for item in coll_hero.find({}):
    print("updating: ", item['avatar'])
    # 冒号不转义
    # item['avatar'] = quote(item['avatar'], safe=':')

    # item['avatar'] = unquote(item['avatar'])

    # item['avatar'] = item['avatar'][:36] + ".png"

    coll_hero.update_one({"_id": item["_id"]}, {"$set": {"avatar": item['avatar']}})
