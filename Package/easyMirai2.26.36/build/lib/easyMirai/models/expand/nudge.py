import json

from rich.console import Console
import requests as po

from .echo import echoTypeMode
from .utils import getApi

api = getApi("expand")


class Nudge:
    def __init__(self, url, session, target):
        self._url = url
        self._session = session
        self._target = target
        self._c = Console()

    def _context(self, name: str, by: str, to: str, subject: int):
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "subject": subject,
            "kind": name
        }
        data = po.post(self._url + api["send"][by][to], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：捏捏发送成功",
                            "详细：" + str(self._target) + "(" + name + " " + str(subject) + ") <- '捏捏'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：捏捏发送失败", style="#ff8f8f")
        return echoTypeMode(data)

    @property
    def friend(self):
        return self._context("Friend", "nudge", "sendNudge", self._target)

    def group(self, gid: int):
        return self._context("Group", "nudge", "sendNudge", gid)
