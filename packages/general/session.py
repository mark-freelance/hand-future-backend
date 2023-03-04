import os
from urllib.parse import urljoin

from requests import Session

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"


class LiveServerSession(Session):
    """
    ref: https://stackoverflow.com/a/51026159/9422455
    """

    def __init__(self, base_url=None):
        super().__init__()
        self.base_url = base_url

    def request(self, method, url, *args, **kwargs):
        joined_url = urljoin(self.base_url, url)
        return super().request(method, joined_url, *args, **kwargs)


session = LiveServerSession(base_url=os.environ['BACKEND_ENDPOINT'])
session.headers = {
    "user_agent": USER_AGENT
}
