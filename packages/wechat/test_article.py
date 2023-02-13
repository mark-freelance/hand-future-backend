from unittest import TestCase

from packages.wechat.article import parse_wechat_article, WechatArticleModel


class Test(TestCase):
    def test_parse_wechat_article(self):
        data = {
            "url": "https://mp.weixin.qq.com/s/5eONLhWjvh2Pj1yK2LSd9g",
            "title": "电脑截长图，看这篇文章就够了",
            "desc": "学会这几个插件，关于电脑截长图的需求你都可以得到满足。",
            "cover_url": "http://mmbiz.qpic.cn/mmbiz_jpg/1iaW67Z9d8OKUK8OianKu0Ecb9iaAibPqsLQpa08Iwtxgk6R4MFJicjic49icVmLZpbnV9z4tCgtxTzvz9aGiah6XSTVEQ/0?wx_fmt=jpeg",
        }
        model_req = WechatArticleModel(**data)
        model_res = parse_wechat_article(data["url"])
        self.assertEqual(model_req, model_res)
