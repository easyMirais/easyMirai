#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : SFNCO-Studio
# @Time     : 2022/11/24 20:18
# @File     : actionType.py
# @Project  : Deep in easyMirai
# @Uri      : https://sfnco.com.cn/
import json

import requests

from easyMirai.echo.echoTypeMode import echoTypeMode
from easyMirai.data.getData import getApi

from easyMirai.globalvar import Uri, Session, IsSlice
from easyMirai.logger.logger import Logger

api = getApi("models")


class actionTypeMode:
    # 操作模式
    def __repr__(self):
        return "请选择群操作模式"

    def group(self, target: int):
        return ActionGroup(target=target)

    @property
    def friend(self):
        return ActionFriend()


class ActionGroup:
    def __init__(self, target: int):
        self._target = target
        self._c = Logger(IsSlice().get)

    def mute(self, target: int):
        return ActionGroupMute(self._target, target)

    def unmute(self, target: int):
        data = {
            "sessionKey": Session().get,
            "target": self._target,
            "memberId": target,
        }
        data = requests.post(Uri().get + api["action"]["unmute"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)

            if data["code"] == 0:
                self._c.Notice("解除禁言成功 详细：" + str(self._target) + "(Group) <- '" + str(target) + "'")
            else:
                self._c.Error("解除禁言失败")
        return echoTypeMode(data)

    @property
    def muteAll(self):
        data = {
            "sessionKey": Session().get,
            "target": self._target,
        }
        data = requests.post(Uri().get + api["action"]["muteAll"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)

            if data["code"] == 0:
                self._c.Notice("全体禁言成功 详细：" + str(self._target) + "(Group) <- 'muteAll'")
            else:
                self._c.Error("全体禁言失败")
        return echoTypeMode(data)

    @property
    def unMuteAll(self):
        data = {
            "sessionKey": Session().get,
            "target": self._target,
        }
        data = requests.post(Uri().get + api["action"]["unmuteAll"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice("解除全体禁言成功 详细：" + str(self._target) + "(Group) <- 'unMuteAll'")
            else:
                self._c.Error("解除全体禁言失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def kick(self, target: int):
        data = {
            "sessionKey": Session().get,
            "target": self._target,
            "memberId": target,
            "msg": "您已被移出群聊"
        }
        data = requests.post(Uri().get + api["action"]["kick"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice("移除群成员成功 详细：" + str(self._target) + "(Group) <- '" + str(target) + "'")
            else:
                self._c.Error("移除群成员失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    @property
    def quit(self):
        data = {
            "sessionKey": Session().get,
            "target": self._target,
        }
        data = requests.post(Uri().get + api["action"]["quit"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice("退出群聊成功 详细：" + str(self._target) + "(Group) <- 'quit'")
            else:
                self._c.Error("退出群聊失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)


class ActionGroupMute:
    def __init__(self, target: int, memberId: int):
        self._target = target
        self._memberId = memberId
        self._c = Logger(IsSlice().get)

    def _request(self, time: int):
        if time >= 2592000:
            time = 2591999
        data = {
            "sessionKey": Session().get,
            "target": self._target,
            "memberId": self._memberId,
            "time": time
        }
        data = requests.post(Uri().get + api["action"]["mute"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice("禁言成功 详细：" + str(self._target) + "(Group) <- '" + str(time) + " s " + str(self._memberId) + "'")
            else:
                self._c.Error("禁言失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

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


class ActionFriend:
    def __init__(self):
        self._c = Logger(IsSlice().get)

    def deleteFriend(self, target: int):
        data = {
            "sessionKey": Session().get,
            "target": target,
        }
        data = requests.post(Uri().get + api["action"]["deleteFriend"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice("移除好友成功 详细：" + str(target) + "(Friend) <- 'deleteFriend'")
            else:
                self._c.Error("移除好友失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)
