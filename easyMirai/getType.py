#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : SFNCO-Studio
# @Time     : 2022/11/24 19:00
# @File     : getType.py
# @Project  : Deep in easyMirai
# @Uri      : https://sfnco.com.cn/
import json

import requests
from rich.console import Console

from easyMirai.echo.echoTypeMode import echoTypeMode
from easyMirai.data.getData import getApi

api = getApi("models")


class getTypeMode:
    def __init__(self, session: str, uri: str, isSlice: bool):
        self._uri = uri
        self._session = session
        self._isSlice = isSlice
        self._c = Console()

    def _get(self, message: str):
        data = requests.get(self._uri + str(api["get"]["info"]))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：获取成功",
                                "详细：" + message + "(get) <- '获取'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：获取失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：获取失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}
        return echoTypeMode(data)

    @property
    def info(self):
        return self._get("插件信息")

    @property
    def message(self):
        return GetMessage(uri=self._uri, session=self._session, isSlice=self._isSlice)

    @property
    def list(self):
        return GetList(uri=self._uri, session=self._session, isSlice=self._isSlice)

    @property
    def proFile(self):
        return GetProFile(uri=self._uri, session=self._session, isSlice=self._isSlice)

    def groupConfig(self, target: int):
        data = {
            "sessionKey": self._session,
            "target": target
        }
        data = requests.get(self._uri + api["get"]["groupConfig"], params=data)
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if "code" not in data:
                    self._c.log("[Notice]：获取成功",
                                "详细：获取群设置(get) <- " + str(target),
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：获取失败", style="#ff8f8f")
            elif "code" in data:
                self._c.log("[Error]：获取失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)


class GetMessage:
    def __init__(self, uri: str, session: str, isSlice: bool):
        self._url = uri
        self._session = session
        self._isSlice = isSlice
        self._c = Console()

    def _request(self, message, to: str, params: dict):
        data = requests.get(self._url + str(api["get"][to]), params=params)
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：获取成功",
                                "详细：" + message + "(get) <- '获取信息'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：获取失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：获取失败", style="#ff8f8f")
        return echoTypeMode(data)

    @property
    def count(self):
        data = {
            "sessionKey": self._session
        }
        return self._request("count", "count", data)

    def fetch(self, count: int):
        data = {
            "sessionKey": self._session,
            "count": count
        }
        return self._request("fetchMessage", "fetchMessage", data)

    def fetchLatest(self, count: int):
        data = {
            "sessionKey": self._session,
            "count": count
        }
        return self._request("fetchLatestMessage", "fetchLatestMessage", data)

    def peek(self, count: int):
        data = {
            "sessionKey": self._session,
            "count": count
        }
        return self._request("peekMessage", "peekMessage", data)

    def peekLatest(self, count: int):
        data = {
            "sessionKey": self._session,
            "count": count
        }
        return self._request("peekLatestMessage", "peekLatestMessage", data)

    def fromId(self, mid: int):
        data = {
            "sessionKey": self._session,
            "id": mid
        }
        return self._request("messageFromId", "messageFromId", data)


class GetList:
    def __init__(self, uri: str, session: str, isSlice: bool):
        self._url = uri
        self._session = session
        self._isSlice = isSlice
        self._c = Console()

    def _request(self, message, to: str, params: dict):
        data = requests.get(self._url + str(api["get"][to]), params=params)
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：获取成功",
                                "详细：" + message + "(get) <- '获取'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：获取失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：获取失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    @property
    def friend(self):
        data = {
            "sessionKey": self._session
        }
        return self._request("friendList", "friendList", data)

    @property
    def group(self):
        data = {
            "sessionKey": self._session
        }
        return self._request("groupList", "groupList", data)

    def member(self, target: int):
        data = {
            "sessionKey": self._session,
            "target": target
        }
        return self._request("memberList", "memberList", data)


class GetProFile:
    def __init__(self, uri: str, session: str, isSlice: bool):
        self._url = uri
        self._session = session
        self._isSlice = isSlice
        self._c = Console()

    def _request(self, message, to: str, params: dict):
        data = requests.get(self._url + str(api["get"][to]), params=params)
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if "code" in data:
                    self._c.log("[Notice]：获取成功",
                                "详细：" + message + "(get) <- '获取资料页'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：撤回失败", style="#ff8f8f")
            elif "code" in data:
                self._c.log("[Error]：获取失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    @property
    def bot(self):
        data = {
            "sessionKey": self._session
        }
        return self._request("botProfile", "botProfile", data)

    def friend(self, target: int):
        data = {
            "sessionKey": self._session,
            "target": target
        }
        return self._request("friendProfile", "friendProfile", data)

    def member(self, gid: int, target: int):
        data = {
            "sessionKey": self._session,
            "target": gid,
            "memberId": target,
        }
        return self._request("memberProfile", "memberProfile", data)

    def user(self, target: int):
        data = {
            "sessionKey": self._session,
            "target": target,
        }
        return self._request("userProfile", "userProfile", data)
