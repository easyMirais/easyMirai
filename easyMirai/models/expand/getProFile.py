import json

from rich.console import Console
import requests as po

from .echo import echoTypeMode
from .utils import getApi

api = getApi("expand")


class GetProFile:
    def __init__(self, url, session):
        self._url = url
        self._session = session
        self._c = Console()

    def _request(self, message, to: str, params: dict):
        data = po.get(self._url + str(api["get"][to]), params=params)
        if data.status_code == 200:
            data = json.loads(data.text)
            if "code" not in data:
                self._c.log("[Notice]：获取成功",
                            "详细：" + message + "(get) <- '获取资料页'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：获取失败", style="#ff8f8f")
        return echoTypeMode(data)

    @property
    def bot(self):
        data = {
            "sessionKey": self._session
        }
        return self._request("botProfile", "botProfile", data)

    def friend(self, target: int):
        data = {
            "sessionKey": self._session,
            "target": target
        }
        return self._request("friendProfile", "friendProfile", data)

    def member(self, gid: int, target: int):
        data = {
            "sessionKey": self._session,
            "target": gid,
            "memberId": target,
        }
        return self._request("memberProfile", "memberProfile", data)

    def user(self, target: int):
        data = {
            "sessionKey": self._session,
            "target": target,
        }
        return self._request("userProfile", "userProfile", data)
