#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : SFNCO-Studio
# @Time     : 2022/11/24 19:00
# @File     : getType.py
# @Project  : Deep in easyMirai
# @Uri      : https://sfnco.com.cn/
import http
import json

import requests

from easyMirai.echo.echoTypeMode import echoTypeMode
from easyMirai.data.getData import getApi

from easyMirai.globalvar import Uri, Session, IsSlice
from easyMirai.logger.logger import Logger

api = getApi("models")


class getTypeMode:
    def __init__(self):
        self._c = Logger(IsSlice().get)

    def _get(self, message: str):
        data = requests.get(Uri().get + str(api["get"]["info"]))
        if data.status_code == http.HTTPStatus.OK:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice("获取成功 详细：" + message + "(get) <- '获取'")
            else:
                self._c.Error("获取失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}
        return echoTypeMode(data)

    @property
    def info(self):
        return self._get("插件信息")

    @property
    def message(self):
        return GetMessage()

    @property
    def list(self):
        return GetList()

    @property
    def proFile(self):
        return GetProFile()

    def groupConfig(self, target: int):
        data = {
            "sessionKey": Session().get,
            "target": target
        }
        data = requests.get(Uri().get + api["get"]["groupConfig"], params=data)
        if data.status_code == http.HTTPStatus.OK:
            data = json.loads(data.text)
            if "code" not in data:
                self._c.Notice("获取成功 详细：获取群设置(get) <- " + str(target))
            else:
                self._c.Error("获取失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)


class GetMessage:
    def __init__(self):
        self._c = Logger(IsSlice().get)

    def _request(self, message, to: str, params: dict):
        data = requests.get(Uri().get + str(api["get"][to]), params=params)
        if data.status_code == http.HTTPStatus.OK:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice("获取成功 详细：" + message + "(get) <- '获取信息'")
            else:
                self._c.Error("获取失败")
        return echoTypeMode(data)

    @property
    def count(self):
        data = {
            "sessionKey": Session().get
        }
        return self._request("count", "count", data)

    def fetch(self, count: int):
        data = {
            "sessionKey": Session().get,
            "count": count
        }
        return self._request("fetchMessage", "fetchMessage", data)

    def fetchLatest(self, count: int):
        data = {
            "sessionKey": Session().get,
            "count": count
        }
        return self._request("fetchLatestMessage", "fetchLatestMessage", data)

    def peek(self, count: int):
        data = {
            "sessionKey": Session().get,
            "count": count
        }
        return self._request("peekMessage", "peekMessage", data)

    def peekLatest(self, count: int):
        data = {
            "sessionKey": Session().get,
            "count": count
        }
        return self._request("peekLatestMessage", "peekLatestMessage", data)

    def fromId(self, mid: int):
        data = {
            "sessionKey": Session().get,
            "id": mid
        }
        return self._request("messageFromId", "messageFromId", data)


class GetList:
    def __init__(self):
        self._c = Logger(IsSlice().get)

    def _request(self, message, to: str, params: dict):
        data = requests.get(Uri().get + str(api["get"][to]), params=params)
        if data.status_code == http.HTTPStatus.OK:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice("获取成功 详细：" + message + "(get) <- '获取'")
            else:
                self._c.Error("获取失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    @property
    def friend(self):
        data = {
            "sessionKey": Session().get
        }
        return self._request("friendList", "friendList", data)

    @property
    def group(self):
        data = {
            "sessionKey": Session().get
        }
        return self._request("groupList", "groupList", data)

    def member(self, target: int):
        data = {
            "sessionKey": Session().get,
            "target": target
        }
        return self._request("memberList", "memberList", data)


class GetProFile:
    def __init__(self):
        self._c = Logger(IsSlice().get)

    def _request(self, message, to: str, params: dict):
        data = requests.get(Uri().get + str(api["get"][to]), params=params)
        if data.status_code == http.HTTPStatus.OK:
            data = json.loads(data.text)
            if "code" in data:
                self._c.Notice("获取成功 详细：" + message + "(get) <- '获取资料页'")
            else:
                self._c.Error("获取失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    @property
    def bot(self):
        data = {
            "sessionKey": Session().get
        }
        return self._request("botProfile", "botProfile", data)

    def friend(self, target: int):
        data = {
            "sessionKey": Session().get,
            "target": target
        }
        return self._request("friendProfile", "friendProfile", data)

    def member(self, gid: int, target: int):
        data = {
            "sessionKey": Session().get,
            "target": gid,
            "memberId": target,
        }
        return self._request("memberProfile", "memberProfile", data)

    def user(self, target: int):
        data = {
            "sessionKey": Session().get,
            "target": target,
        }
        return self._request("userProfile", "userProfile", data)
