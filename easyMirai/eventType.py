#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : SFNCO-Studio
# @Time     : 2022/11/24 20:39
# @File     : eventType.py
# @Project  : Deep in easyMirai
# @Uri      : https://sfnco.com.cn/
import json

import requests

from easyMirai.echo.echoTypeMode import echoTypeMode
from easyMirai.data.getData import getApi

from easyMirai.globalvar import Uri, Session, IsSlice
from easyMirai.logger.logger import Logger

api = getApi("expand")


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
        return EventNewFriend(target, self._eventId, groupId)

    def newJoinGroup(self, target: int, groupId: int):
        return EventJoinGroup(target, self._eventId, groupId)

    def newBotJoinGroup(self, groupId: int, fromId: int):
        return EventBotJoinGroup(self._eventId, groupId, fromId)


class EventNewFriend:
    def __init__(self, target, eventId, group):
        self._target = target
        self._eventId = eventId
        self._groupId = group
        self._c = Logger(IsSlice().get)

    def _request(self, code: int, eventId, message):
        data = {
            "sessionKey": Session().get,
            "eventId": self._eventId,
            "fromId": eventId,
            "groupId": self._groupId,
            "operate": code,
            "message": message
        }
        data = requests.post(Uri().get + api["event"]["newFriend"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice("好友添加事件处理成功 详细：" + str(self._target) + "(Friend) <- '" + str(code) + "'")
            else:
                self._c.Error("好友添加事件处理失败")
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
    def __init__(self, target, eventId, groupId):
        self._target = target
        self._eventId = eventId
        self._groupId = groupId
        self._c = Logger(IsSlice().get)

    def _request(self, code: int, eventId, message):
        data = {
            "sessionKey": Session().get,
            "eventId": self._eventId,
            "fromId": eventId,
            "groupId": self._groupId,
            "operate": code,
            "message": message
        }
        data = requests.post(Uri().get + api["event"]["joinGroup"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice("用户入群申请事件处理成功 详细：" + str(self._target) + "(Group) <- '" + str(code) + "'")
            else:
                self._c.Error("用户入群申请事件处理失败")
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
    def __init__(self, eventId, groupId, fromId):
        self._eventId = eventId
        self._groupId = groupId
        self._fromId = fromId
        self._c = Logger(IsSlice().get)

    def _request(self, code: int, message):
        data = {
            "sessionKey": Session().get,
            "eventId": self._eventId,
            "fromId": self._fromId,
            "groupId": self._groupId,
            "operate": code,
            "message": message
        }
        data = requests.get(Uri().get + api["event"]["newFriend"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice("用户入群申请事件处理成功 详细：" + str(self._target) + "(Friend) <- '" + str(code) + "'")
            else:
                self._c.Error("[Error]：用户入群申请事件处理失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def yes(self, message: str = ""):
        return self._request(1, message)

    def no(self, message: str = ""):
        return self._request(0, message)
