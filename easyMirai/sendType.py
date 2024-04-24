#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : SFNCO-Studio
# @Time     : 2022/11/24 16:43
# @File     : models.py
# @Project  : Deep in easyMirai
# @Uri      : https://sfnco.com.cn/
import json
import os
import re

import requests

from easyMirai.echo.echoTypeMode import echoTypeMode
from easyMirai.data.getData import getApi
from easyMirai.logger import Logger

from easyMirai.globalvar import Uri, BotID, Session, IsSlice

api = getApi("expand")


class sendTypeMode:
    def __init__(self):
        self._c = Logger(IsSlice().get)

    def friend(self, target: int):
        return friendTypeMode(target=target)

    def group(self, target: int):
        return groupTypeMode(target=target)

    def temp(self, group: int):
        return tempTypeMode(group=group)

    def nudge(self, target: int):
        return nudge(target=target)


class friendTypeMode:
    # 好友发送消息类型
    def __init__(self, target: int):
        self._target = target
        self._c = Logger(IsSlice().get)

    def plain(self, text: str) -> echoTypeMode:
        print(Session().get)
        data = {
            "sessionKey": Session().get,
            "target": self._target,
            "messageChain": [
                {"type": "Plain", "text": text},
            ]
        }
        data = requests.post(Uri().get + api["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice("文本发送成功 详细：" + str(BotID().get) + "(Friend) <- '" + str(text) + "'")
            else:
                self._c.Error("文本发送失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}
        return echoTypeMode(data)

    def image(self, value: str) -> echoTypeMode:
        uriCompile = re.compile(r'[a-zA-z]+://[^\s]*')
        if re.search(uriCompile, value):
            # 如果是一段网址则直接发送
            data = {
                "sessionKey": Session().get,
                "target": self._target,
                "messageChain": [
                    {"type": "Image", "url": value},
                ]
            }
        else:
            # 如果不是网址则上传后发送
            data = {
                "sessionKey": Session().get,
                "target": BotID().get,
                "messageChain": [
                    {
                        "type": "Image",
                        "url": _uploadImage(value, Session().get, "friend", Uri().get)
                    }
                ]
            }
        data = requests.post(Uri().get + api["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice("图片发送成功详细：" + str(BotID().get) + "(Friend) <- '" + str(value) + "'")
            else:
                self._c.Error("图片发送失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def face(self, value: int, name: str = "") -> echoTypeMode:

        data = {
            "sessionKey": Session().get,
            "target": self._target,
            "messageChain": [
                {
                    "type": "Face",
                    "faceId": value,
                    "name": name
                }
            ]
        }

        data = requests.post(Uri().get + api["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice("表情发送成功 详细：" + str(BotID().get) + "(Friend) <- '" + str(value) + "'")
            else:
                self._c.Error("表情发送失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def voice(self):
        pass

    @property
    def poke(self):
        return poke(target=self._target)

    def dice(self, value: int = 1):

        data = {
            "sessionKey": Session().get,
            "target": BotID().get,
            "messageChain": [
                {
                    "type": "Dice",
                    "value": value
                }
            ]
        }
        data = requests.post(Uri().get + api["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice("骰子发送成功 详细：" + str(BotID().get) + "(Friend) <- '" + str(value) + "'")
            else:
                self._c.Error("骰子发送失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}
        return echoTypeMode(data)

    def recall(self, messageId: int):
        data = {
            "sessionKey": Session().get,
            "messageId": messageId,
            "target": self._target
        }
        data = requests.post(Uri().get + str(api["send"]["recall"]), data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice("撤回成功 详细：" + str(self._target) + "(get) <- '撤回'")
            else:
                self._c.Error("撤回失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def clone(self, to: int):
        pass


class groupTypeMode:
    def __init__(self, target: int):
        self._target = target
        self._c = Logger(IsSlice().get)

    # 发送群消息类型
    def at(self, target: int, display: str = ""):
        data = {
            "sessionKey": Session().get,
            "target": self._target,
            "messageChain": [
                {
                    "type": "At",
                    "target": target,
                    "display": display
                }
            ]
        }

        data = requests.post(Uri().get + api["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)

            if data["code"] == 0:
                self._c.Notice("At发送成功 详细：" + str(BotID().get) + "(Group) <- 'at " + str(target) + "'")
            else:
                self._c.Error("At发送失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def ats(self, target: int, display: str = ""):
        return AtType(target, self._target, display)

    @property
    def atAll(self):
        data = {
            "sessionKey": Session().get,
            "target": BotID().get,
            "messageChain": [
                {
                    "type": "AtAll"
                }
            ]
        }
        data = requests.post(Uri().get + api["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)

            if data["code"] == 0:
                self._c.Notice(
                    "AtAll发送成功 详细：" + str(BotID().get) + "(Group) <- 'at " + str(BotID().get) + "'")
            else:
                self._c.Error("AtAll发送失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def plain(self, context: str):
        data = {
            "sessionKey": Session().get,
            "target": self._target,
            "messageChain": [
                {"type": "Plain", "text": context},
            ]
        }
        data = requests.post(Uri().get + api["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice(
                    "文本发送成功 详细：" + str(BotID().get) + "(Group " + str(BotID().get) + ") <- '" + str(
                        context) + "'")
            else:
                self._c.Error("文本发送失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def image(self, value: str):
        uriCompile = re.compile(r'[a-zA-z]+://[^\s]*')
        if re.search(uriCompile, value):
            data = {
                "sessionKey": Session().get,
                "target": self._target,
                "messageChain": [
                    {"type": "Image", "url": value},
                ]
            }
        else:
            data = {
                "sessionKey": Session().get,
                "target": self._target,
                "messageChain": [
                    {
                        "type": "Image",
                        "url": _uploadImage(value, Session().get, "group", Uri().get)
                    }
                ]
            }

        data = requests.post(Uri().get + api["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)

            if data["code"] == 0:
                self._c.Notice(
                    "图片发送成功 详细：" + str(BotID().get) + "(Group " + str(BotID().get) + ") <- '" + str(
                        value) + "'")
            else:
                self._c.Error("图片发送失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def face(self, faceId: int, name: str = ""):
        data = {
            "sessionKey": Session().get,
            "target": self._target,
            "messageChain": [
                {
                    "type": "Face",
                    "faceId": faceId,
                    "name": name
                }
            ]
        }
        data = requests.post(Uri().get + api["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice(
                    "表情发送成功 详细：" + str(BotID().get) + "(Group " + str(BotID().get) + ") <- '" + str(
                        faceId) + "'")
            else:
                self._c.Error("表情发送失败")

        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def voice(self, voiceId: str = "", url: str = "", length: int = 1024):
        pass  # todo 编写voice 等待实验

    @property
    def poke(self):
        return groupPoke(target=self._target)

    def dice(self, value: int = 1):
        data = {
            "sessionKey": Session().get,
            "target": self._target,
            "messageChain": [
                {
                    "type": "Dice",
                    "value": value
                }
            ]
        }
        data = requests.post(Uri().get + api["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice(
                    "骰子发送成功 详细：" + str(BotID().get) + "(Group " + str(BotID().get) + ") <- '" + str(
                        value) + "'")
            else:
                self._c.Error("骰子发送失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def recall(self, messageId: int):
        data = {
            "sessionKey": Session().get,
            "messageId": messageId,
            "target": self._target
        }
        data = requests.post(Uri().get + str(api["send"]["recall"]), data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice("撤回成功 详细：" + str(self._target) + "(get) <- '撤回'")
            else:
                self._c.Error("撤回失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def app(self, content: str):
        pass

    def other(self, data: dict):
        pass


class tempTypeMode:
    def __init__(self, group: int):
        self._c = Logger(IsSlice().get)
        self._gid = group

    # 发送群临时消息类型
    def to(self, target: int):
        return Temp(gid=target)


class nudge:
    def __init__(self, target):
        self._target = target
        self._c = Logger(IsSlice().get)

    def _context(self, name: str, by: str, to: str, subject: int):
        data = {
            "sessionKey": Session().get,
            "target": self._target,
            "subject": subject,
            "kind": name
        }
        data = requests.post(Uri().get + api["send"][by][to], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)

            if data["code"] == 0:
                self._c.Notice(
                    "捏捏发送成功 详细：" + str(BotID().get) + "(" + name + " " + str(subject) + ") <- '捏捏'")
            else:
                self._c.Error("捏捏发送失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}
        return echoTypeMode(data)

    @property
    def friend(self):
        return self._context("Friend", "nudge", "sendNudge", BotID().get)

    def group(self, gid: int):
        return self._context("Group", "nudge", "sendNudge", gid)


class groupPoke:
    def __init__(self, target):
        self._target = target
        self._c = Logger(IsSlice().get)

    def _context(self, name: str, to: str):
        data = {
            "sessionKey": Session().get,
            "target": self._target,
            "group": self._target,
            "messageChain": [
                {
                    "type": "Poke",
                    "name": name
                }
            ]
        }
        data = requests.post(Uri().get + api["send"]["group"][to], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice("戳一戳发送成功 详细：" + str(BotID().get) + "(Group) <- '" + name + "'")
            else:
                self._c.Error("戳一戳发送失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    @property
    def poke(self):
        return self._context("poke", "sendGroupMessage")

    @property
    def FangDaZhao(self):
        return self._context("FangDaZhao", "sendGroupMessage")


class poke:
    def __init__(self, target):
        self._target = target
        self._c = Logger(IsSlice().get)

    def _context(self, name: str, to: str):
        data = {
            "sessionKey": Session().get,
            "target": self._target,
            "messageChain": [
                {
                    "type": "Poke",
                    "name": name
                }
            ]
        }
        data = requests.post(Uri().get + api["send"]["friend"][to], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice("戳一戳发送成功 详细：" + str(BotID().get) + "(Friend) <- '" + name + "'")
            else:
                self._c.Error("戳一戳发送失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    @property
    def poke(self):
        return self._context("poke", "sendFriendMessage")

    @property
    def FangDaZhao(self):
        return self._context("FangDaZhao", "sendFriendMessage")


def _uploadImage(path: str, session, name, url: str):
    path = os.path.abspath(os.path.join(os.path.dirname(
        __file__), "../", f"{path.lower()}"))  # todo 打包时一定注意！！！！
    message = {"sessionKey": session, "type": name}
    onfiles = {'img': ('send.png', open(path, 'rb'), 'image/png', {})}
    data = requests.request(method="POST", url=url + "/uploadImage", data=message, files=onfiles)
    if data.status_code == 200:
        data = json.loads(data.text)
        if "code" not in data:
            return data["url"]
        else:
            return "error"


class Temp:
    def __init__(self, gid):
        self._gid = gid
        self._c = Logger(IsSlice().get)

    def plain(self, context: str):
        data = {
            "sessionKey": Session().get,
            "qq": BotID().get,
            "group": self._gid,
            "messageChain": [
                {"type": "Plain", "text": context},
            ]
        }
        data = requests.post(Uri().get + api["send"]["temp"]["sendTempMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice("文本发送成功 详细：" + str(BotID().get) + "(Temp " + str(self._gid) + ") <- '" + str(
                    context) + "'")
            else:
                self._c.Error("文本发送失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}
        return echoTypeMode(data)

    def image(self, path: str):
        rec = re.compile(r'[a-zA-z]+://[^\s]*')
        if re.search(rec, path):
            data = {
                "sessionKey": Session().get,
                "qq": BotID().get,
                "group": self._gid,
                "messageChain": [
                    {"type": "Image", "url": path},
                ]
            }
        else:
            data = {
                "sessionKey": Session().get,
                "qq": BotID().get,
                "group": self._gid,
                "messageChain": [
                    {
                        "type": "Image",
                        "url": _uploadImage(path, Session().get, "group", Uri().get)
                    }
                ]
            }
        data = requests.post(Uri().get + api["send"]["temp"]["sendTempMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice("图片发送成功 详细：" + str(BotID().get) + "(Temp " + str(self._gid) + ") <- '" + str(
                    path) + "'")
            else:
                self._c.Error("图片发送失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}
        return echoTypeMode(data)

    def face(self, faceId: int, name: str = ""):
        data = {
            "sessionKey": Session().get,
            "qq": BotID().get,
            "group": self._gid,
            "messageChain": [
                {
                    "type": "Face",
                    "faceId": faceId,
                    "name": name
                }
            ]
        }
        data = requests.post(Uri().get + api["send"]["temp"]["sendTempMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice(
                    "表情发送成功 详细：" + str(BotID().get) + "(Group " + str(self._gid) + ") <- '" + str(
                        faceId) + "'")
            else:
                self._c.Error("表情发送失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}
        return echoTypeMode(data)


class AtType:  # at后添加字符串
    def __init__(self, target, gid, display):
        self._gid = gid
        self._c = Logger(IsSlice().get)
        self.target = target
        self.display = display

    def plain(self, context):  # at后追加文本
        data = {
            "sessionKey": Session().get,
            "target": BotID().get,
            "messageChain": [
                {
                    "type": "At",
                    "target": self.target,
                    "display": self.display
                },
                {"type": "Plain", "text": " " + context},
            ]
        }
        data = requests.post(Uri().get + api["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice(
                    "AT + 文本发送成功 详细：" + str(BotID().get) + "(Group " + str(BotID().get) + ") <- '" + str(
                        context) + "'")
            else:
                self._c.Error("AT + 文本发送失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def image(self, path):  # at后追加图片
        rec = re.compile(r'[a-zA-z]+://[^\s]*')
        if re.search(rec, path):
            data = {
                "sessionKey": Session().get,
                "qq": BotID().get,
                "group": self._gid,
                "messageChain": [
                    {
                        "type": "At",
                        "target": self.target,
                        "display": self.display
                    },
                    {"type": "Image", "url": path},
                ]
            }
        else:
            data = {
                "sessionKey": Session().get,
                "qq": BotID().get,
                "group": self._gid,
                "messageChain": [
                    {
                        "type": "At",
                        "target": self.target,
                        "display": self.display
                    },
                    {
                        "type": "Image",
                        "url": _uploadImage(path, Session().get, "group", Uri().get)
                    }
                ]
            }
        data = requests.post(Uri().get + api["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice(
                    "AT + 图片发送成功 详细：" + str(BotID().get) + "(Temp " + str(self._gid) + ") <- '" + str(
                        path) + "'")
            else:
                self._c.Error("AT + 图片发送失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}
        return echoTypeMode(data)
