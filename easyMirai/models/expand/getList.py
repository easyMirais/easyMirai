import json

from rich.console import Console
import requests as po

from .echo import echoTypeMode
from .utils import getApi

api = getApi("expand")


class GetList:
    def __init__(self, url, session):
        self._url = url
        self._session = session
        self._c = Console()

    def _request(self, message, to: str, params: dict):
        data = po.get(self._url + str(api["get"][to]), params=params)
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：获取成功",
                            "详细：" + message + "(get) <- '获取'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：获取失败", style="#ff8f8f")
        return echoTypeMode(data)

    @property
    def friend(self):
        data = {
            "sessionKey": self._session
        }
        return self._request("friendList", "friendList", data)

    @property
    def group(self):
        data = {
            "sessionKey": self._session
        }
        return self._request("groupList", "groupList", data)

    def member(self, target: int):
        data = {
            "sessionKey": self._session,
            "target": target
        }
        return self._request("memberList", "memberList", data)
