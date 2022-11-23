import json

from rich.console import Console
import requests as po

from .echo import echoTypeMode
from .utils import getApi

api = getApi("expand")


class EventNewFriend:
    def __init__(self, url, session, target, eventId, groupId):
        self._url = url
        self._session = session
        self._target = target
        self._eventId = eventId
        self._groupId = groupId
        self._c = Console()

    def _request(self, code: int, eventId, message):
        data = {
            "sessionKey": self._session,
            "eventId": self._eventId,
            "fromId": eventId,
            "groupId": self._groupId,
            "operate": code,
            "message": message
        }
        data = po.post(self._url + api["event"]["newFriend"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：好友添加事件处理成功",
                            "详细：" + str(self._target) + "(Friend) <- '" + str(code) + "'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：好友添加事件处理失败", style="#ff8f8f")
        return echoTypeMode(data)

    def yes(self, message: str = ""):
        return self._request(1, self._eventId, message)

    def no(self, message: str = ""):
        return self._request(0, self._eventId, message)

    def black(self, message: str = ""):
        return self._request(2, self._eventId, message)
