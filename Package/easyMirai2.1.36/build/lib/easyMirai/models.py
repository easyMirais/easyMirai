# -*- coding: utf-8 -*-
import json
import re

import requests as po
from .expand import (
    expandPoke,
    expandNudge,
    expandTemp,
    expandGetMessage,
    expandGetList,
    expandGetProFile,
    expandEventNewFriend,
    expandEventJoinGroup,
    expandEventBotJoinGroup,
    expandUploadImage,
    expandActionGroup,
    expandActionFriend,
    expandSetGroupConfig
)

from rich.console import Console

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
        },
        "recall": "/recall"
    },
    "get": {
        "info": "/about",
        "groupConfig": "/groupConfig"
    },
    "set": {
        "essence": "/setEssence"
    }
}


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
        return expandNudge(self._url, self._session, target)

    def recall(self, target: int):
        data = {
            "sessionKey": self._session,
            "target": target
        }
        data = po.post(self._url + str(_config["send"]["recall"]), data=json.dumps(data))
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
        data = po.post(self._url + _config["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
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
                        "url": _uploadImage(path, self._session, "friend", self._url)
                    }
                ]
            }
        data = po.post(self._url + _config["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
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
        data = po.post(self._url + _config["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
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

        data = po.post(self._url + _config["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
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
        return expandPoke(self._url, self._session, self._target)

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
        data = po.post(self._url + _config["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
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
        data = po.post(self._url + _config["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
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
        data = po.post(self._url + _config["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
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
        data = po.post(self._url + _config["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
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
        data = po.post(self._url + _config["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
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
        data = po.post(self._url + _config["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
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
        data = po.post(self._url + _config["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
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
                        "url": _uploadImage(path, self._session, "group", self._url)
                    }
                ]
            }
        data = po.post(self._url + _config["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
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
        data = po.post(self._url + _config["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
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

        data = po.post(self._url + _config["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
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
        return expandPoke(self._url, self._session, self._target)

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
        data = po.post(self._url + _config["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
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
        data = po.post(self._url + _config["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
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
        data = po.post(self._url + _config["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：信息发送成功", "详细：" + str(self._target) + "(Group) <- '未知'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：信息发送失败", style="#ff8f8f")
        return echoTypeMode(data)


class getTypeMode:
    def __init__(self, session: str, uri: str):
        self._url = uri
        self._session = session
        self._c = Console()

    def _get(self, message: str):
        data = po.get(self._url + str(_config["get"]["info"]))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：获取成功",
                            "详细：" + message + "(get) <- '获取'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：获取失败", style="#ff8f8f")
        return echoTypeMode(data)

    @property
    def info(self):
        return self._get("插件信息")

    @property
    def message(self):
        return expandGetMessage(self._url, self._session)

    @property
    def list(self):
        return expandGetList(self._url, self._session)

    @property
    def proFile(self):
        return expandGetProFile(self._url, self._session)

    def groupConfig(self, target: int):
        data = {
            "sessionKey": self._session,
            "target": target
        }
        data = po.get(self._url + _config["get"]["groupConfig"], params=data)
        if data.status_code == 200:
            data = json.loads(data.text)
            if "code" not in data:
                self._c.log("[Notice]：获取成功",
                            "详细：获取群设置(get) <- " + str(target),
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：获取失败", style="#ff8f8f")
        return echoTypeMode(data)


class setTypeMode:
    def __init__(self, session: str, uri: str):
        self._url = uri
        self._session = session
        self._c = Console()

    def essence(self, target: int):
        data = {
            "sessionKey": self._session,
            "target": target,
        }
        data = po.post(self._url + _config["set"]["essence"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：设置成功",
                            "详细：群精华消息(set) <- " + str(target),
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：设置失败", style="#ff8f8f")
        return echoTypeMode(data)

    @property
    def message(self):
        return expandGetMessage(self._url, self._session)

    @property
    def list(self):
        return expandGetList(self._url, self._session)

    @property
    def proFile(self):
        return expandGetProFile(self._url, self._session)

    def group(self, target: int):
        # 修改群相关设置
        return expandSetGroupConfig(self._url, self._session, target)


class tempTypeMode:
    def __init__(self, session: str, url: str, gid: int):
        self._url = url
        self._session = session
        self._c = Console()
        self._gid = gid

    # 发送群临时消息类型
    def to(self, target: int):
        return expandTemp(self._url, self._session, target, self._gid)


class uploadTypeMode:
    # 上传模式
    def __init__(self, session, uri):
        self._session = session
        self._url = uri

    def __repr__(self):
        return "请选择上传模式"

    def image(self, path: str):
        return expandUploadImage(self._url, self._session, path)


class actionTypeMode:
    # 操作模式
    def __init__(self, session, uri):
        self._session = session
        self._url = uri

    def __repr__(self):
        return "请选择群操作模式"

    def group(self, target: int):
        return expandActionGroup(self._url, self._session, target)

    @property
    def friend(self):
        return expandActionFriend(self._url, self._session)


class eventTypeMode:
    # 操作模式
    def __init__(self, session, uri, eventId):
        self._session = session
        self._url = uri
        self._eventId = eventId  # 事件ID

    def __repr__(self):
        return "请选择事件处理类型"

    def newFriend(self, target: int, groupId: int = 0):
        return expandEventNewFriend(self._url, self._session, target, self._eventId, groupId)

    def newJoinGroup(self, target: int, groupId: int):
        return expandEventJoinGroup(self._url, self._session, target, self._eventId, groupId)

    def newBotJoinGroup(self, target: int, groupId: int, fromId: int):
        return expandEventBotJoinGroup(self._url, self._session, target, self._eventId, groupId, fromId)


class echoTypeMode:

    def __init__(self, context):
        self._context = context

    def __repr__(self):
        return "<Request [OK]>"

    @property
    def json(self) -> str:
        """
        将返回值格式化为字符串类型
        @return: str
        """
        data = json.dumps(self._context)
        return data

    @property
    def dictionary(self) -> dict:
        """
        将返回值格式化为字典类型
        @return: dict
        """
        return self._context


def _uploadImage(path: str, session, name, url: str):
    message = {"sessionKey": session, "type": name}
    onfiles = {'img': ('send.png', open(path, 'rb'), 'image/png', {})}
    data = po.request(method="POST", url=url + "/uploadImage", data=message, files=onfiles)
    if data.status_code == 200:
        data = json.loads(data.text)
        if "code" not in data:
            return data["url"]
        else:
            return "error"
