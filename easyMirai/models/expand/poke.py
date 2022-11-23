import json

from rich.console import Console
import requests as po

from .echo import echoTypeMode
from .utils import getApi

api = getApi("expand")


class Poke:
    def __init__(self, url, session, target):
        self._url = url
        self._session = session
        self._target = target
        self._c = Console()

    def _context(self, name: str, to: str):
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "messageChain": [
                {
                    "type": "Poke",
                    "name": name
                }
            ]
        }
        data = po.post(self._url + api["send"]["friend"][to], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：戳一戳发送成功", "详细：" + str(self._target) + "(Friend) <- '" + name + "'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：戳一戳发送失败", style="#ff8f8f")
        return echoTypeMode(data)

    @property
    def poke(self):
        return self._context("poke", "sendFriendMessage")

    @property
    def FangDaZhao(self):
        return self._context("FangDaZhao", "sendFriendMessage")
