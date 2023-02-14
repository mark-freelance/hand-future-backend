from functools import partial

from pydantic import BaseModel

from log import getLogger
from packages.general.re import parse_p1
from session import session

logger = getLogger("WechatArticle")


class WechatArticleModel(BaseModel):
    url: str
    cover_url: str
    title: str
    desc: str


def parse_wechat_article(url: str) -> WechatArticleModel:
    """
    todo: add robust return when parsing invalid url like "ss"
    :param url:
    :return:
    """
    res = session.get(url)
    logger.debug({"url": url, "res": res, "text": res.text})

    parse = partial(lambda p: parse_p1(p, res.text))
    data = {
        "url": url,
        "cover_url": parse(r'var msg_cdn_url = "(.*?)";'),
        "title": parse(r"var msg_title = '(.*?)'.html\(false\);"),
        "desc": parse(r'''var msg_desc = htmlDecode\("(.*?)"\);'''),
    }
    logger.info(data)
    return WechatArticleModel(**data)
