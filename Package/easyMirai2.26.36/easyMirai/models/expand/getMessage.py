import json

from rich.console import Console
import requests as po

from .echo import echoTypeMode
from .utils import getApi

api = getApi("expand")


class GetMessage:
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
                            "详细：" + message + "(get) <- '获取信息'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：获取失败", style="#ff8f8f")
        return echoTypeMode(data)

    @property
    def count(self):
        data = {
            "sessionKey": self._session
        }
        return self._request("count", "count", data)

    def fetch(self, count: int):
        data = {
            "sessionKey": self._session,
            "count": count
        }
        return self._request("fetchMessage", "fetchMessage", data)

    def fetchLatest(self, count: int):
        data = {
            "sessionKey": self._session,
            "count": count
        }
        return self._request("fetchLatestMessage", "fetchLatestMessage", data)

    def peek(self, count: int):
        data = {
            "sessionKey": self._session,
            "count": count
        }
        return self._request("peekMessage", "peekMessage", data)

    def peekLatest(self, count: int):
        data = {
            "sessionKey": self._session,
            "count": count
        }
        return self._request("peekLatestMessage", "peekLatestMessage", data)

    def fromId(self, mid: int):
        data = {
            "sessionKey": self._session,
            "id": mid
        }
        return self._request("messageFromId", "messageFromId", data)
