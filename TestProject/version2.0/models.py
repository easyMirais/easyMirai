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
        return groupTypeMode(session=self.session, content=target, url=self.url)


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


class groupTypeMode:
    def __init__(self, session: str, url: str, content=None):
        self.content = content
        self.url = url
        self.session = session
        self.c = Console()

    # 发送群消息类型
    def at(self, target=None):
        return echoTypeMode("send group type is at message")


class tempTypeMode:
    def __init__(self, target):
        self.target = target

    # 发送群消息类型
    def text(self):
        print("send group type is at message")
        print("我at了 " + self.target)

        return echoTypeMode("send group type is at message")


class echoTypeMode:
    def __init__(self, context):
        self.context = context

    def __repr__(self):
        return str(self.context)

    @property
    def text(self):
        return self.context

    @property
    def json(self):
        print("echo type is json message")
        return self.context + "this is json"
