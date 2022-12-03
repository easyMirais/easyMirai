#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : SFNCO-Studio
# @Time     : 2022/11/24 20:18
# @File     : actionType.py
# @Project  : Deep in easyMirai
# @Uri      : https://sfnco.com.cn/
import json

from rich.console import Console
import requests

from easyMirai.echo.echoTypeMode import echoTypeMode
from easyMirai.data.getData import getApi

api = getApi("models")


class actionTypeMode:
    # 操作模式
    def __init__(self, session: str, uri: str, isSlice: bool):
        self._session = session
        self._isSlice = isSlice
        self._uri = uri

    def __repr__(self):
        return "请选择群操作模式"

    def group(self, target: int):
        return ActionGroup(uri=self._uri, session=self._session, target=target, isSlice=self._isSlice)

    @property
    def friend(self):
        return ActionFriend(uri=self._uri, session=self._session, isSlice=self._isSlice)


class ActionGroup:
    def __init__(self, uri: str, session: str, target: int, isSlice: bool):
        self._url = uri
        self._session = session
        self._target = target
        self._isSlice = isSlice
        self._c = Console()

    def mute(self, target: int):
        return ActionGroupMute(self._url, self._session, self._target, target, self._isSlice)

    def unmute(self, target: int):
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "memberId": target,
        }
        data = requests.post(self._url + api["action"]["unmute"], data=json.dumps(data))
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
        data = requests.post(self._url + api["action"]["muteAll"], data=json.dumps(data))
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
        data = requests.post(self._url + api["action"]["unmuteAll"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：解除全体禁言成功",
                                "详细：" + str(self._target) + "(Group) <- 'unMuteAll'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：解除全体禁言失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：解除全体禁言失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def kick(self, target: int):
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "memberId": target,
            "msg": "您已被移出群聊"
        }
        data = requests.post(self._url + api["action"]["kick"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：移除群成员成功",
                                "详细：" + str(self._target) + "(Group) <- '" + str(target) + "'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：移除群成员失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：移除群成员失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    @property
    def quit(self):
        data = {
            "sessionKey": self._session,
            "target": self._target,
        }
        data = requests.post(self._url + api["action"]["quit"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：退出群聊成功",
                                "详细：" + str(self._target) + "(Group) <- 'quit'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：退出群聊失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：退出群聊失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)


class ActionGroupMute:
    def __init__(self, url: str, session: str, target: int, memberId: int, isSlice: bool):
        self._url = url
        self._session = session
        self._target = target
        self._memberId = memberId
        self._isSlice = isSlice
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
        data = requests.post(self._url + api["action"]["mute"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：禁言成功",
                                "详细：" + str(self._target) + "(Group) <- '" + str(time) + " s " + str(
                                    self._memberId) + "'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：禁言失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：禁言失败", style="#ff8f8f")
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
    def __init__(self, uri: str, session: str, isSlice: bool):
        self._uri = uri
        self._session = session
        self._isSlice = isSlice
        self._c = Console()

    def deleteFriend(self, target: int):
        data = {
            "sessionKey": self._session,
            "target": target,
        }
        data = requests.post(self._uri + api["action"]["deleteFriend"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：移除好友成功",
                                "详细：" + str(target) + "(Friend) <- 'deleteFriend'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：移除好友失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：移除好友失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)
