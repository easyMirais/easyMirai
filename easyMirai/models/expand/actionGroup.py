import json

from rich.console import Console
import requests as po

from .echo import echoTypeMode
from .utils import getApi

api = getApi("expand")


class ActionGroup:
    def __init__(self, url, session, gid):
        self._url = url
        self._session = session
        self._target = gid
        self._c = Console()

    def mute(self, target: int):
        return ActionGroupMute(self._url, self._session, self._target, target)

    def unmute(self, target: int):
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "memberId": target,
        }
        data = po.post(self._url + api["action"]["unmute"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)

            if data["code"] == 0:
                self._c.log("[Notice]：解除禁言成功",
                            "详细：" + str(self._target) + "(Group) <- '" + str(target) + "'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：解除禁言失败", style="#ff8f8f")
        return echoTypeMode(data)

    @property
    def muteAll(self):
        data = {
            "sessionKey": self._session,
            "target": self._target,
        }
        data = po.post(self._url + api["action"]["muteAll"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)

            if data["code"] == 0:
                self._c.log("[Notice]：全体禁言成功",
                            "详细：" + str(self._target) + "(Group) <- 'muteAll'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：全体禁言失败", style="#ff8f8f")
        return echoTypeMode(data)

    @property
    def unMuteAll(self):
        data = {
            "sessionKey": self._session,
            "target": self._target,
        }
        data = po.post(self._url + api["action"]["unmuteAll"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)

            if data["code"] == 0:
                self._c.log("[Notice]：全体禁言成功",
                            "详细：" + str(self._target) + "(Group) <- 'unMuteAll'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：全体禁言失败", style="#ff8f8f")
        return echoTypeMode(data)

    def kick(self, target: int):
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "memberId": target,
            "msg": "您已被移出群聊"
        }
        data = po.post(self._url + api["action"]["kick"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：移除群成员成功",
                            "详细：" + str(self._target) + "(Group) <- '" + str(target) + "'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：移除群成员失败", style="#ff8f8f")
        return echoTypeMode(data)

    @property
    def quit(self):
        data = {
            "sessionKey": self._session,
            "target": self._target,
        }
        data = po.post(self._url + api["action"]["quit"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：退出群聊成功",
                            "详细：" + str(self._target) + "(Group) <- 'quit'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：退出群聊失败", style="#ff8f8f")
        return echoTypeMode(data)


class ActionGroupMute:
    def __init__(self, url, session, target, memberId):
        self._url = url
        self._session = session
        self._target = target
        self._memberId = memberId
        self._c = Console()

    def _request(self, time: int):
        if time >= 2592000:
            time = 2591999
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "memberId": self._memberId,
            "time": time
        }
        data = po.post(self._url + api["action"]["mute"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：禁言成功",
                            "详细：" + str(self._target) + "(Group) <- '" + str(time) + " s " + str(self._memberId) + "'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：禁言失败", style="#ff8f8f")
        return echoTypeMode(data)

    def s(self, second: int):
        return self._request(second)

    def m(self, minute: int):
        second = minute * 60
        return self._request(second)

    def h(self, minute: int):
        second = minute * 60 * 60
        return self._request(second)

    def d(self, day: int):
        second = day * 60 * 24 * 60
        return self._request(second)
