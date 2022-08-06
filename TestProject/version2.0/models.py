# -*- coding: utf-8 -*-
import json

import requests as po

try:
    from rich.console import Console

    rh: bool = True
except ImportError as ip:
    rh: bool = False

_config = {
    "send": {
        "friend": {
            "sendFriendMessage": "/sendFriendMessage"
        },
        "group": {
            "sendGroupMessage": "/sendGroupMessage"
        },
        "temp": {
            "sendTempMessage": "/sendTempMessage"
        }
    }
}


class targetMode:
    # 发送者目标
    def __init__(self, session, uri):
        self.session = session
        self.url = uri

    def __repr__(self):
        return "请选择一个发送模式"

    def friend(self, target: int):
        return friendTypeMode(session=self.session, url=self.url, target=target)

    def group(self, target: int):
        return groupTypeMode(session=self.session, target=target, url=self.url)


class friendTypeMode:
    # 好友发送消息类型
    def __init__(self, session, url: str, target: int):
        self.session = session
        self.url = url
        self.target = target
        self.c = Console()

    def text(self, context: str = " "):
        data = {
            "sessionKey": self.session,
            "target": self.target,
            "messageChain": [
                {"type": "Plain", "text": context},
            ]
        }
        data = po.post(self.url + _config["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self.c.log("[Notice]：文本发送成功", "详细：" + str(self.target) + "(Friend) <- '" + str(context) + "'",
                           style="#a4ff8f")
            else:
                self.c.log("[Error]：文本发送失败", style="#ff8f8f")
        return echoTypeMode(data)

    def image(self, url: str = " "):
        data = {
            "sessionKey": self.session,
            "target": self.target,
            "messageChain": [
                {"type": "Image", "url": url},
            ]
        }
        data = po.post(self.url + _config["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self.c.log("[Notice]：图片发送成功", "详细：" + str(self.target) + "(Friend) <- '" + str(url) + "'",
                           style="#a4ff8f")
            else:
                self.c.log("[Error]：图片发送失败", style="#ff8f8f")
        return echoTypeMode(data)

    def face(self, faceId: int, name: str = ""):
        data = {
            "sessionKey": self.session,
            "target": self.target,
            "messageChain": [
                {
                    "type": "Face",
                    "faceId": faceId,
                    "name": name
                }
            ]
        }
        data = po.post(self.url + _config["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self.c.log("[Notice]：表情发送成功", "详细：" + str(self.target) + "(Friend) <- '" + str(faceId) + "'",
                           style="#a4ff8f")
            else:
                self.c.log("[Error]：表情发送失败", style="#ff8f8f")
        return echoTypeMode(data)

    def voice(self, voiceId: str = "", url: str = "", length: int = 1024):
        data = {
            "sessionKey": self.session,
            "target": self.target,
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

        data = po.post(self.url + _config["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
        if data["code"] == 0:
            self.c.log("[Notice]：语音发送成功", "详细：" + str(self.target) + "(Friend) <- '" + str(voiceId) + "'",
                       style="#a4ff8f")
        else:
            self.c.log("[Error]：语音发送失败", style="#ff8f8f")
        return echoTypeMode(data)

    def other(self, data: dict):
        data = {
            "sessionKey": self.session,
            "target": self.target,
            "messageChain": [
                data
            ]
        }
        data = po.post(self.url + _config["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self.c.log("[Notice]：信息发送成功", "详细：" + str(self.target) + "(Friend) <- '未知'",
                           style="#a4ff8f")
            else:
                self.c.log("[Error]：信息发送失败", style="#ff8f8f")
        return echoTypeMode(data)

    @property
    def poke(self):
        return expandPoke(self.url, self.session, self.target)

    def dice(self, value: int = 1):
        data = {
            "sessionKey": self.session,
            "target": self.target,
            "messageChain": [
                {
                    "type": "Dice",
                    "value": value
                }
            ]
        }
        data = po.post(self.url + _config["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self.c.log("[Notice]：骰子发送成功", "详细：" + str(self.target) + "(Friend) <- '未知'",
                           style="#a4ff8f")
            else:
                self.c.log("[Error]：骰子发送失败", style="#ff8f8f")
        return echoTypeMode(data)

    def musicShare(self, value: int = 1):
        data = {
            "sessionKey": self.session,
            "target": self.target,
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
        data = po.post(self.url + _config["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self.c.log("[Notice]：骰子发送成功", "详细：" + str(self.target) + "(Friend) <- '未知'",
                           style="#a4ff8f")
            else:
                self.c.log("[Error]：骰子发送失败", style="#ff8f8f")
        return echoTypeMode(data)

    def app(self, content: str):
        data = {
            "sessionKey": self.session,
            "target": self.target,
            "messageChain": [
                {
                    "type": "App",
                    "content": content
                }
            ]
        }
        data = po.post(self.url + _config["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self.c.log("[Notice]：APP卡片发送成功", "详细：" + str(self.target) + "(Friend) <- 'APP卡片'",
                           style="#a4ff8f")
            else:
                self.c.log("[Error]：APP卡片发送失败", style="#ff8f8f")
        return echoTypeMode(data)


class expandPoke:
    def __init__(self, url, session, target):
        self.url = url
        self.session = session
        self.target = target
        self.c = Console()

    def _context(self, name: str, to: str):
        data = {
            "sessionKey": self.session,
            "target": self.target,
            "messageChain": [
                {
                    "type": "Poke",
                    "name": name
                }
            ]
        }
        data = po.post(self.url + _config["send"]["friend"][to], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self.c.log("[Notice]：戳一戳发送成功", "详细：" + str(self.target) + "(Friend) <- '" + name + "'",
                           style="#a4ff8f")
            else:
                self.c.log("[Error]：戳一戳发送失败", style="#ff8f8f")
        return echoTypeMode(data)

    @property
    def poke(self):
        return self._context("poke", "sendFriendMessage")

    @property
    def showLove(self):
        return self._context("ShowLove", "sendFriendMessage")

    @property
    def like(self):
        return self._context("Like", "sendFriendMessage")

    @property
    def heartbroken(self):
        return self._context("Heartbroken", "sendFriendMessage")

    @property
    def SixSixSix(self):
        return self._context("Heartbroken", "sendFriendMessage")

    @property
    def FangDaZhao(self):
        return self._context("FangDaZhao", "sendFriendMessage")


class groupTypeMode:
    def __init__(self, session: str, url: str, target: int):
        self.url = url
        self.session = session
        self.c = Console()
        self.target = target

    # 发送群消息类型
    def at(self, target: int, display: str = ""):
        data = {
            "sessionKey": self.session,
            "target": self.target,
            "messageChain": [
                {
                    "type": "At",
                    "target": target,
                    "display": display
                }
            ]
        }
        data = po.post(self.url + _config["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)

            if data["code"] == 0:
                self.c.log("[Notice]：At发送成功", "详细：" + str(self.target) + "(Group) <- 'at " + str(target) + "'",
                           style="#a4ff8f")
            else:
                self.c.log("[Error]：At发送失败", style="#ff8f8f")
        return echoTypeMode(data)

    def text(self, context: str = " "):
        data = {
            "sessionKey": self.session,
            "target": self.target,
            "messageChain": [
                {"type": "Plain", "text": context},
            ]
        }
        data = po.post(self.url + _config["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self.c.log("[Notice]：文本发送成功", "详细：" + str(self.target) + "(Group) <- '" + str(context) + "'",
                           style="#a4ff8f")
            else:
                self.c.log("[Error]：文本发送失败", style="#ff8f8f")
        return echoTypeMode(data)

    def image(self, url: str = " "):
        data = {
            "sessionKey": self.session,
            "target": self.target,
            "messageChain": [
                {"type": "Image", "url": url},
            ]
        }
        data = po.post(self.url + _config["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self.c.log("[Notice]：图片发送成功", "详细：" + str(self.target) + "(Group) <- '" + str(url) + "'",
                           style="#a4ff8f")
            else:
                self.c.log("[Error]：图片发送失败", style="#ff8f8f")
        return echoTypeMode(data)

    def other(self, data: dict):
        data = po.post(self.url + _config["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self.c.log("[Notice]：信息发送成功", "详细：" + str(self.target) + "(Group) <- '未知'",
                           style="#a4ff8f")
            else:
                self.c.log("[Error]：信息发送失败", style="#ff8f8f")
        return echoTypeMode(data)


class tempTypeMode:
    def __init__(self, target):
        self.target = target

    # 发送群消息类型
    def text(self):
        print("send group type is at message")
        print("我at了 " + self.target)

        return echoTypeMode("send group type is at message")


class echoTypeMode:
    """
    输出类型选择
    """

    def __init__(self, context):
        self.context = context

    def __repr__(self):
        return str(self.context)

    @property
    def json(self) -> str:
        """
        格式化输出为json文本
        """
        data = json.dumps(self.context)
        return data

    @property
    def dictionary(self) -> dict:
        """
        格式化输出为字典
        """
        return self.context
