#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : SFNCO-Studio
# @Time     : 2022/11/24 20:39
# @File     : eventType.py
# @Project  : Deep in easyMirai
# @Uri      : https://sfnco.com.cn/
import json

from rich.console import Console
import requests

from easyMirai.echo.echoTypeMode import echoTypeMode
from easyMirai.data.getData import getApi

api = getApi("model")


class eventTypeMode:
    # 操作模式
    def __init__(self, session, uri, eventId, isSlice: bool):
        self._session = session
        self._url = uri
        self._eventId = eventId  # 事件ID
        self._isSlice = isSlice

    def __repr__(self):
        return "请选择事件处理类型"

    def newFriend(self, target: int, groupId: int = 0):
        return EventNewFriend(self._url, self._session, target, self._eventId, groupId, self._isSlice)

    def newJoinGroup(self, target: int, groupId: int):
        return EventJoinGroup(self._url, self._session, target, self._eventId, groupId, self._isSlice)

    def newBotJoinGroup(self, target: int, groupId: int, fromId: int):
        return EventBotJoinGroup(self._url, self._session, target, self._eventId, groupId, fromId, self._isSlice)


class EventNewFriend:
    def __init__(self, url, session, target, eventId, group, isSlice: bool):
        self._url = url
        self._session = session
        self._target = target
        self._eventId = eventId
        self._groupId = group
        self._isSlice = isSlice
        self._c = Console()

    def _request(self, code: int, eventId, message):
        data = {
            "sessionKey": self._session,
            "eventId": self._eventId,
            "fromId": eventId,
            "groupId": self._groupId,
            "operate": code,
            "message": message
        }
        data = requests.post(self._url + api["event"]["newFriend"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：好友添加事件处理成功",
                                "详细：" + str(self._target) + "(Friend) <- '" + str(code) + "'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：好友添加事件处理失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：好友添加事件处理失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def yes(self, message: str = ""):
        return self._request(1, self._eventId, message)

    def no(self, message: str = ""):
        return self._request(0, self._eventId, message)

    def black(self, message: str = ""):
        return self._request(2, self._eventId, message)


class EventJoinGroup:
    def __init__(self, url, session, target, eventId, groupId, isSlice: bool):
        self._url = url
        self._session = session
        self._target = target
        self._eventId = eventId
        self._groupId = groupId
        self._isSlice = isSlice
        self._c = Console()

    def _request(self, code: int, eventId, message):
        data = {
            "sessionKey": self._session,
            "eventId": self._eventId,
            "fromId": eventId,
            "groupId": self._groupId,
            "operate": code,
            "message": message
        }
        data = requests.post(self._url + api["event"]["newFriend"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：用户入群申请事件处理成功",
                                "详细：" + str(self._target) + "(Friend) <- '" + str(code) + "'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：用户入群申请事件处理失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：用户入群申请事件处理失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def yes(self, message: str = ""):
        return self._request(1, self._eventId, message)

    def no(self, message: str = ""):
        return self._request(0, self._eventId, message)

    def over(self, message: str = ""):
        return self._request(2, self._eventId, message)

    def noBlack(self, message: str = ""):
        return self._request(3, self._eventId, message)

    def overBlack(self, message: str = ""):
        return self._request(4, self._eventId, message)


class EventBotJoinGroup:
    def __init__(self, url, session, target, eventId, groupId, fromId, isSlice: bool):
        self._url = url
        self._session = session
        self._target = target
        self._eventId = eventId
        self._groupId = groupId
        self._fromId = fromId
        self._isSlice = isSlice
        self._c = Console()

    def _request(self, code: int, message):
        data = {
            "sessionKey": self._session,
            "eventId": self._eventId,
            "fromId": self._fromId,
            "groupId": self._groupId,
            "operate": code,
            "message": message
        }
        data = requests.get(self._url + api["event"]["newFriend"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：用户入群申请事件处理成功",
                                "详细：" + str(self._target) + "(Friend) <- '" + str(code) + "'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：用户入群申请事件处理失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：用户入群申请事件处理失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def yes(self, message: str = ""):
        return self._request(1, message)

    def no(self, message: str = ""):
        return self._request(0, message)
