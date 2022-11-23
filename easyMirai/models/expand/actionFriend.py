import json

from rich.console import Console
import requests as po

from .echo import echoTypeMode
from .utils import getApi

api = getApi("expand")


class ActionFriend:
    def __init__(self, url, session):
        self._url = url
        self._session = session
        self._c = Console()

    def deleteFriend(self, target: int):
        data = {
            "sessionKey": self._session,
            "target": target,
        }
        data = po.post(self._url + api["action"]["deleteFriend"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：移除好友成功",
                            "详细：" + str(target) + "(Friend) <- 'deleteFriend'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：移除好友失败", style="#ff8f8f")
        return echoTypeMode(data)
