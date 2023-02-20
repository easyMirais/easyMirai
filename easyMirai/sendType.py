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

from rich.console import Console
import requests

from easyMirai.echo.echoTypeMode import echoTypeMode
from easyMirai.data.getData import getApi

api = getApi("expand")


class sendTypeMode:
    def __init__(self, session: str, uri: str, isSlice: bool):
        self._session = session
        self._uri = uri
        self._isSlice = isSlice
        self._c = Console()

    def friend(self, target: int):
        return friendTypeMode(session=self._session, target=target, url=self._uri, isSlice=self._isSlice)

    def group(self, target: int):
        return groupTypeMode(session=self._session, target=target, url=self._uri, isSlice=self._isSlice)

    def temp(self, group: int):
        return tempTypeMode(session=self._session, group=group, url=self._uri, isSlice=self._isSlice)

    def nudge(self, target: int):
        return nudge(session=self._session, target=target, url=self._uri, isSlice=self._isSlice)

    def recall(self, target: int):
        print(target)
        data = {
            "sessionKey": self._session,
            "target": target
        }
        print(json.dumps(data))
        data = requests.post(self._uri + str(api["send"]["recall"]), data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：撤回成功",
                                "详细：" + str(target) + "(get) <- '撤回'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：撤回失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：撤回失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)


class friendTypeMode:
    # 好友发送消息类型
    def __init__(self, session, url: str, target: int, isSlice: bool):
        self._session = session
        self._uri = url
        self._target = target
        self._c = Console()
        self._isSlice = isSlice

    def plain(self, value: str) -> echoTypeMode:
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "messageChain": [
                {"type": "Plain", "text": value},
            ]
        }
        data = requests.post(self._uri + api["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：文本发送成功", "详细：" + str(self._target) + "(Friend) <- '" + str(value) + "'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：文本发送失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：文本发送失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}
        return echoTypeMode(data)

    def image(self, value: str) -> echoTypeMode:
        uriCompile = re.compile(r'[a-zA-z]+://[^\s]*')
        if re.search(uriCompile, value):
            # 如果是一段网址则直接发送
            data = {
                "sessionKey": self._session,
                "target": self._target,
                "messageChain": [
                    {"type": "Image", "url": value},
                ]
            }
        else:
            # 如果不是网址则上传后发送
            data = {
                "sessionKey": self._session,
                "target": self._target,
                "messageChain": [
                    {
                        "type": "Image",
                        "url": _uploadImage(value, self._session, "friend", self._uri)
                    }
                ]
            }
        data = requests.post(self._uri + api["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：图片发送成功", "详细：" + str(self._target) + "(Friend) <- '" + str(value) + "'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：图片发送失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：图片发送失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def face(self, value: int, name: str = "") -> echoTypeMode:

        data = {
            "sessionKey": self._session,
            "target": self._target,
            "messageChain": [
                {
                    "type": "Face",
                    "faceId": value,
                    "name": name
                }
            ]
        }

        data = requests.post(self._uri + api["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：表情发送成功", "详细：" + str(self._target) + "(Friend) <- '" + str(value) + "'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：表情发送失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：表情发送失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def voice(self):
        pass

    @property
    def poke(self):
        return poke(uri=self._uri, session=self._session, target=self._target, isSlice=self._isSlice)

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
        data = requests.post(self._uri + api["send"]["friend"]["sendFriendMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：骰子发送成功", "详细：" + str(self._target) + "(Friend) <- '" + str(value) + "'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：骰子发送失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：骰子发送失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}
        return echoTypeMode(data)



class groupTypeMode:
    def __init__(self, session: str, url: str, target: int, isSlice: bool):
        self._uri = url
        self._session = session
        self._target = target
        self._isSlice = isSlice
        self._c = Console()

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

        data = requests.post(self._uri + api["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：At发送成功", "详细：" + str(self._target) + "(Group) <- 'at " + str(target) + "'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：At发送失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：At发送失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

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
        data = requests.post(self._uri + api["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：AtAll发送成功",
                                "详细：" + str(self._target) + "(Group) <- 'at " + str(self._target) + "'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：AtAll发送失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：AtAll发送失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def plain(self, context: str):
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "messageChain": [
                {"type": "Plain", "text": context},
            ]
        }
        data = requests.post(self._uri + api["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：文本发送成功",
                                "详细：" + str(self._target) + "(Group " + str(self._target) + ") <- '" + str(
                                    context) + "'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：文本发送失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：文本发送失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def image(self, value: str):
        uriCompile = re.compile(r'[a-zA-z]+://[^\s]*')
        if re.search(uriCompile, value):
            data = {
                "sessionKey": self._session,
                "target": self._target,
                "messageChain": [
                    {"type": "Image", "url": value},
                ]
            }
        else:
            data = {
                "sessionKey": self._session,
                "target": self._target,
                "messageChain": [
                    {
                        "type": "Image",
                        "url": _uploadImage(value, self._session, "group", self._uri)
                    }
                ]
            }

        data = requests.post(self._uri + api["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：图片发送成功",
                                "详细：" + str(self._target) + "(Group " + str(self._target) + ") <- '" + str(value) + "'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：图片发送失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：图片发送失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

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
        data = requests.post(self._uri + api["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：表情发送成功",
                                "详细：" + str(self._target) + "(Group " + str(self._target) + ") <- '" + str(
                                    faceId) + "'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：表情发送失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：表情发送失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def voice(self, voiceId: str = "", url: str = "", length: int = 1024):
        pass  # todo 编写voice 等待实验

    def poke(self, group: int):
        return groupPoke(uri=self._uri, session=self._session, target=self._target, isSlice=self._isSlice, group=group)

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
        data = requests.post(self._uri + api["send"]["group"]["sendGroupMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：骰子发送成功",
                                "详细：" + str(self._target) + "(Group " + str(self._target) + ") <- '" + str(value) + "'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：骰子发送失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：骰子发送失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def app(self, content: str):
        pass

    def other(self, data: dict):
        pass


class tempTypeMode:
    def __init__(self, session: str, url: str, group: int, isSlice: bool):
        self._url = url
        self._session = session
        self._c = Console()
        self._gid = group
        self._isSlice = isSlice

    # 发送群临时消息类型
    def to(self, target: int):
        return Temp(self._url, self._session, target, self._gid, self._isSlice)


class nudge:
    def __init__(self, session, url: str, target: int, isSlice: bool):
        self._url = url
        self._session = session
        self._target = target
        self._c = Console()
        self._isSlice = isSlice

    def _context(self, name: str, by: str, to: str, subject: int):
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "subject": subject,
            "kind": name
        }
        data = requests.post(self._url + api["send"][by][to], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：捏捏发送成功",
                                "详细：" + str(self._target) + "(" + name + " " + str(subject) + ") <- '捏捏'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：捏捏发送失败", style="#ff8f8f")
            else:
                self._c.log("[Error]：捏捏发送失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}
        return echoTypeMode(data)

    @property
    def friend(self):
        return self._context("Friend", "nudge", "sendNudge", self._target)

    def group(self, gid: int):
        return self._context("Group", "nudge", "sendNudge", gid)


class groupPoke:
    def __init__(self, uri: str, session: str, target: int, isSlice: bool, group: int):
        self._url = uri
        self._session = session
        self._target = target
        self._isSlice = isSlice
        self._group = group
        self._c = Console()

    def _context(self, name: str, to: str):
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "group": self._group,
            "messageChain": [
                {
                    "type": "Poke",
                    "name": name
                }
            ]
        }
        data = requests.post(self._url + api["send"]["group"][to], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：戳一戳发送成功", "详细：" + str(self._target) + "(Group) <- '" + name + "'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：戳一戳发送失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：戳一戳发送失败", style="#ff8f8f")
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
    def __init__(self, uri: str, session: str, target: int, isSlice: bool):
        self._url = uri
        self._session = session
        self._target = target
        self._isSlice = isSlice
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
        data = requests.post(self._url + api["send"]["friend"][to], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：戳一戳发送成功", "详细：" + str(self._target) + "(Friend) <- '" + name + "'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：戳一戳发送失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：戳一戳发送失败", style="#ff8f8f")
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
    def __init__(self, url, session, target, gid, isSlice: bool):
        self._url = url
        self._session = session
        self._target = target
        self._gid = gid
        self._isSlice = isSlice
        self._c = Console()

    def plain(self, context: str):
        data = {
            "sessionKey": self._session,
            "qq": self._target,
            "group": self._gid,
            "messageChain": [
                {"type": "Plain", "text": context},
            ]
        }
        data = requests.post(self._url + api["send"]["temp"]["sendTempMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：文本发送成功",
                                "详细：" + str(self._target) + "(Temp " + str(self._gid) + ") <- '" + str(context) + "'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：文本发送失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：文本发送失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}
        return echoTypeMode(data)

    def image(self, path: str):
        rec = re.compile(r'[a-zA-z]+://[^\s]*')
        if re.search(rec, path):
            data = {
                "sessionKey": self._session,
                "qq": self._target,
                "group": self._gid,
                "messageChain": [
                    {"type": "Image", "url": path},
                ]
            }
        else:
            data = {
                "sessionKey": self._session,
                "qq": self._target,
                "group": self._gid,
                "messageChain": [
                    {
                        "type": "Image",
                        "url": _uploadImage(path, self._session, "group", self._url)
                    }
                ]
            }
        data = requests.post(self._url + api["send"]["temp"]["sendTempMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：图片发送成功",
                                "详细：" + str(self._target) + "(Temp " + str(self._gid) + ") <- '" + str(path) + "'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：图片发送失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：图片发送失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}
        return echoTypeMode(data)

    def face(self, faceId: int, name: str = ""):
        data = {
            "sessionKey": self._session,
            "qq": self._target,
            "group": self._gid,
            "messageChain": [
                {
                    "type": "Face",
                    "faceId": faceId,
                    "name": name
                }
            ]
        }
        data = requests.post(self._url + api["send"]["temp"]["sendTempMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：表情发送成功",
                                "详细：" + str(self._target) + "(Group " + str(self._gid) + ") <- '" + str(faceId) + "'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：表情发送失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：表情发送失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}
        return echoTypeMode(data)
