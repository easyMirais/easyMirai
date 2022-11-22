import json
import re

from rich.console import Console
import requests as po

from .expand.utils import getApi
from .expand.echo import echoTypeMode
from .expand.nudge import Nudge
from .expand.poke import Poke
from .expand.other import uploadImage
from .expand.temp import Temp

api = getApi("models")


class sendTypeMode:
    # 发送者目标
    def __init__(self, session, uri):
        self._session = session
        self._url = uri
        self._c = Console()

    def __repr__(self):
        return "请选择一个信息执行模式"

    def friend(self, target: int):
        return friendTypeMode(session=self._session, url=self._url, target=target)

    def group(self, target: int):
        return groupTypeMode(session=self._session, target=target, url=self._url)

    def temp(self, gid: int):
        return tempTypeMode(session=self._session, gid=gid, url=self._url)

    def nudge(self, target: int):
        return Nudge(self._url, self._session, target)

    def recall(self, target: int):
        data = {
            "sessionKey": self._session,
            "target": target
        }
        data = po.post(self._url + str(api["send"]["recall"]), data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：撤回成功",
                            "详细：" + str(target) + "(get) <- '撤回'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：撤回失败", style="#ff8f8f")
        return echoTypeMode(data)


class friendTypeMode:
    # 好友发送消息类型
    def __init__(self, session, url: str, target: int):
        self._session = session
        self._url = url
        self._target = target
        self._c = Console()

    def plain(self, context: str = " "):
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "messageChain": [
                {"type": "Plain", "text": context},
            ]
        }
        data = po.post(self._url + api["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：文本发送成功", "详细：" + str(self._target) + "(Friend) <- '" + str(context) + "'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：文本发送失败", style="#ff8f8f")
        return echoTypeMode(data)

    def image(self, path: str):
        rec = re.compile(r'[a-zA-z]+://[^\s]*')
        if re.search(rec, path):
            data = {
                "sessionKey": self._session,
                "target": self._target,
                "messageChain": [
                    {"type": "Image", "url": path},
                ]
            }
        else:
            data = {
                "sessionKey": self._session,
                "target": self._target,
                "messageChain": [
                    {
                        "type": "Image",
                        "url": uploadImage(path, self._session, "friend", self._url)
                    }
                ]
            }
        data = po.post(self._url + api["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
        if data["code"] == 0:
            self._c.log("[Notice]：图片发送成功", "详细：" + str(self._target) + "(Friend) <- '" + str(path) + "'",
                        style="#a4ff8f")
        else:
            self._c.log("[Error]：图片发送失败", style="#ff8f8f")
        return echoTypeMode(data)

    def face(self, faceId: int, name: str = ""):
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "messageChain": [
                {
                    "type": "Face",
                    "faceId": faceId,
                    "name": name
                }
            ]
        }
        data = po.post(self._url + api["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：表情发送成功", "详细：" + str(self._target) + "(Friend) <- '" + str(faceId) + "'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：表情发送失败", style="#ff8f8f")
        return echoTypeMode(data)

    def voice(self, voiceId: str = "", url: str = "", length: int = 1024):
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "messageChain": [
                {
                    "type": "Voice",
                    "voiceId": voiceId,
                    "url": url,
                    "path": "null",
                    "base64": "null",
                    "length": length,
                }
            ]
        }

        data = po.post(self._url + api["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
        if data["code"] == 0:
            self._c.log("[Notice]：语音发送成功", "详细：" + str(self._target) + "(Friend) <- '" + str(voiceId) + "'",
                        style="#a4ff8f")
        else:
            self._c.log("[Error]：语音发送失败", style="#ff8f8f")
        return echoTypeMode(data)

    @property
    def poke(self):
        return Poke(self._url, self._session, self._target)

    def dice(self, value: int = 1):
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "messageChain": [
                {
                    "type": "Dice",
                    "value": value
                }
            ]
        }
        data = po.post(self._url + api["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：骰子发送成功", "详细：" + str(self._target) + "(Friend) <- '未知'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：骰子发送失败", style="#ff8f8f")
        return echoTypeMode(data)

    def musicShare(self, value: int = 1):
        # 待解决
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "messageChain": [
                {
                    "type": "MusicShare",
                    "kind": "String",
                    "title": "String",
                    "summary": "String",
                    "jumpUrl": "String",
                    "pictureUrl": "String",
                    "musicUrl": "String",
                    "brief": "String"
                }
            ]
        }
        data = po.post(self._url + api["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：骰子发送成功", "详细：" + str(self._target) + "(Friend) <- '未知'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：骰子发送失败", style="#ff8f8f")
        return echoTypeMode(data)

    def app(self, content: str):
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "messageChain": [
                {
                    "type": "App",
                    "content": content
                }
            ]
        }
        data = po.post(self._url + api["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：APP卡片发送成功", "详细：" + str(self._target) + "(Friend) <- 'APP卡片'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：APP卡片发送失败", style="#ff8f8f")
        return echoTypeMode(data)

    def other(self, data: dict):
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "messageChain": [
                data
            ]
        }
        data = po.post(self._url + api["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：信息发送成功", "详细：" + str(self._target) + "(Friend) <- '未知'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：信息发送失败", style="#ff8f8f")
        return echoTypeMode(data)


class groupTypeMode:
    def __init__(self, session: str, url: str, target: int):
        self._url = url
        self._session = session
        self._c = Console()
        self._target = target

    # 发送群消息类型
    def at(self, target: int, display: str = ""):
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "messageChain": [
                {
                    "type": "At",
                    "target": target,
                    "display": display
                }
            ]
        }
        data = po.post(self._url + api["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)

            if data["code"] == 0:
                self._c.log("[Notice]：At发送成功", "详细：" + str(self._target) + "(Group) <- 'at " + str(target) + "'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：At发送失败", style="#ff8f8f")
        return echoTypeMode(data)

    @property
    def atAll(self):
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "messageChain": [
                {
                    "type": "AtAll"
                }
            ]
        }
        data = po.post(self._url + api["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)

            if data["code"] == 0:
                self._c.log("[Notice]：AtAll发送成功",
                            "详细：" + str(self._target) + "(Group) <- 'at " + str(self._target) + "'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：AtAll发送失败", style="#ff8f8f")
        return echoTypeMode(data)

    def plain(self, context: str):
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "messageChain": [
                {"type": "Plain", "text": context},
            ]
        }
        data = po.post(self._url + api["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：文本发送成功",
                            "详细：" + str(self._target) + "(Group " + str(self._target) + ") <- '" + str(context) + "'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：文本发送失败", style="#ff8f8f")
        return echoTypeMode(data)

    def image(self, path: str):
        rec = re.compile(r'[a-zA-z]+://[^\s]*')
        if re.search(rec, path):
            data = {
                "sessionKey": self._session,
                "target": self._target,
                "messageChain": [
                    {"type": "Image", "url": path},
                ]
            }
        else:
            data = {
                "sessionKey": self._session,
                "target": self._target,
                "messageChain": [
                    {
                        "type": "Image",
                        "url": uploadImage(path, self._session, "group", self._url)
                    }
                ]
            }
        data = po.post(self._url + api["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
        if data["code"] == 0:
            self._c.log("[Notice]：图片发送成功",
                        "详细：" + str(self._target) + "(Group " + str(self._target) + ") <- '" + str(path) + "'",
                        style="#a4ff8f")
        else:
            self._c.log("[Error]：图片发送失败", style="#ff8f8f")
        return echoTypeMode(data)

    def face(self, faceId: int, name: str = ""):
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "messageChain": [
                {
                    "type": "Face",
                    "faceId": faceId,
                    "name": name
                }
            ]
        }
        data = po.post(self._url + api["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：表情发送成功",
                            "详细：" + str(self._target) + "(Group " + str(self._target) + ") <- '" + str(faceId) + "'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：表情发送失败", style="#ff8f8f")
        return echoTypeMode(data)

    def voice(self, voiceId: str = "", url: str = "", length: int = 1024):
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "messageChain": [
                {
                    "type": "Voice",
                    "voiceId": voiceId,
                    "url": url,
                    "path": "null",
                    "base64": "null",
                    "length": length,
                }
            ]
        }

        data = po.post(self._url + api["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
        if data["code"] == 0:
            self._c.log("[Notice]：语音发送成功",
                        "详细：" + str(self._target) + "(Group " + str(self._target) + ") <- '" + str(voiceId) + "'",
                        style="#a4ff8f")
        else:
            self._c.log("[Error]：语音发送失败", style="#ff8f8f")
        return echoTypeMode(data)

    def poke(self):
        return Poke(self._url, self._session, self._target)

    def dice(self, value: int = 1):
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "messageChain": [
                {
                    "type": "Dice",
                    "value": value
                }
            ]
        }
        data = po.post(self._url + api["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：骰子发送成功",
                            "详细：" + str(self._target) + "(Group " + str(self._target) + ") <- '" + str(value) + "'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：骰子发送失败", style="#ff8f8f")
        return echoTypeMode(data)

    def app(self, content: str):
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "messageChain": [
                {
                    "type": "App",
                    "content": content
                }
            ]
        }
        data = po.post(self._url + api["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：APP卡片发送成功",
                            "详细：" + str(self._target) + "(Group " + str(self._target) + ") <- 'APP卡片'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：APP卡片发送失败", style="#ff8f8f")
        return echoTypeMode(data)

    def other(self, data: dict):
        data = po.post(self._url + api["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：信息发送成功", "详细：" + str(self._target) + "(Group) <- '未知'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：信息发送失败", style="#ff8f8f")
        return echoTypeMode(data)


class tempTypeMode:
    def __init__(self, session: str, url: str, gid: int):
        self._url = url
        self._session = session
        self._c = Console()
        self._gid = gid

    # 发送群临时消息类型
    def to(self, target: int):
        return Temp(self._url, self._session, target, self._gid)
