#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : SFNCO-Studio
# @Time     : 2022/11/24 19:23
# @File     : setType.py
# @Project  : Deep in easyMirai
# @Uri      : https://sfnco.com.cn/
import json

from rich.console import Console
import requests

from easyMirai.echo.echoTypeMode import echoTypeMode
from easyMirai.data.getData import getApi

api = getApi("models")


class setTypeMode:
    def __init__(self, session: str, uri: str, isSlice: bool):
        self._session = session
        self._uri = uri
        self._isSlice = isSlice
        self._c = Console()

    def essence(self, target: int):
        data = {
            "sessionKey": self._session,
            "target": target,
        }
        data = requests.post(self._uri + api["set"]["essence"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                if not self._isSlice:
                    if data["code"] == 0:
                        self._c.log("[Notice]：设置成功",
                                    "详细：群精华消息(set) <- " + str(target),
                                    style="#a4ff8f")
                    else:
                        self._c.log("[Error]：设置失败", style="#ff8f8f")
                elif data["code"] != 0:
                    self._c.log("[Error]：设置失败", style="#ff8f8f")
            else:
                data = {"code": data.status_code, "msg": "网络错误"}

            return echoTypeMode(data)

    def group(self, target: int):
        # 修改群相关设置
        return SetGroupConfig(self._uri, self._session, target, isSlice=self._isSlice)


class SetGroupConfig:
    # 修改群设置
    def __init__(self, url, session, target: int, isSlice: bool):
        self._url = url
        self._session = session
        self._target = target
        self._isSlice = isSlice
        self._c = Console()

    def name(self, name: str):
        # 修改群名称
        data = getGroupConfig(self._url, self._session, self._target)
        if "announcement" not in data:
            data["announcement"] = ""
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "config": {
                "name": name,
                "announcement": data["announcement"],
                "confessTalk": data["confessTalk"],
                "allowMemberInvite": data["allowMemberInvite"],
                "autoApprove": data["autoApprove"],
                "anonymousChat": data["anonymousChat"]
            }
        }
        data = requests.post(self._url + api["get"]["groupConfig"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：群配置修改成功",
                                "详细：" + str(self._target) + "(name) <- '" + str(name) + "'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：群配置修改失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：群配置修改失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def announcement(self, content: str):
        # 修改群名称
        data = getGroupConfig(self._url, self._session, self._target)
        if "announcement" not in data:
            data["announcement"] = ""
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "config": {
                "name": data["name"],
                "announcement": content,
                "confessTalk": data["confessTalk"],
                "allowMemberInvite": data["allowMemberInvite"],
                "autoApprove": data["autoApprove"],
                "anonymousChat": data["anonymousChat"]
            }
        }
        data = requests.post(self._url + api["get"]["groupConfig"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：群配置修改成功",
                                "详细：" + str(self._target) + "(announcement) <- '" + str(content) + "'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：群配置修改失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：群配置修改失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def confessTalk(self, mode: bool):
        data = getGroupConfig(self._url, self._session, self._target)
        if "announcement" not in data:
            data["announcement"] = ""
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "config": {
                "name": data["name"],
                "announcement": data["announcement"],
                "confessTalk": mode,
                "allowMemberInvite": data["allowMemberInvite"],
                "autoApprove": data["autoApprove"],
                "anonymousChat": data["anonymousChat"]
            }
        }
        data = requests.post(self._url + api["get"]["groupConfig"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：群配置修改成功",
                                "详细：" + str(self._target) + "(confessTalk) <- '" + str(mode) + "'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：群配置修改失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：群配置修改失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def allowMemberInvite(self, mode: bool):
        data = getGroupConfig(self._url, self._session, self._target)
        if "announcement" not in data:
            data["announcement"] = ""
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "config": {
                "name": data["name"],
                "announcement": data["announcement"],
                "confessTalk": data["confessTalkt"],
                "allowMemberInvite": mode,
                "autoApprove": data["autoApprove"],
                "anonymousChat": data["anonymousChat"]
            }
        }
        data = requests.post(self._url + api["get"]["groupConfig"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：群配置修改成功",
                                "详细：" + str(self._target) + "(confessTalk) <- '" + str(mode) + "'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：群配置修改失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：群配置修改失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def autoApprove(self, mode: bool):
        data = getGroupConfig(self._url, self._session, self._target)
        if "announcement" not in data:
            data["announcement"] = ""
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "config": {
                "name": data["name"],
                "announcement": data["announcement"],
                "confessTalk": data["confessTalkt"],
                "allowMemberInvite": data["allowMemberInvite"],
                "autoApprove": mode,
                "anonymousChat": data["anonymousChat"]
            }
        }
        data = requests.post(self._url + api["get"]["groupConfig"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：群配置修改成功",
                                "详细：" + str(self._target) + "(autoApprove) <- '" + str(mode) + "'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：群配置修改失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：群配置修改失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def anonymousChat(self, mode: bool):
        data = getGroupConfig(self._url, self._session, self._target)
        if "announcement" not in data:
            data["announcement"] = ""
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "config": {
                "name": data["name"],
                "announcement": data["announcement"],
                "confessTalk": data["confessTalkt"],
                "allowMemberInvite": data["allowMemberInvite"],
                "autoApprove": data["autoApprove"],
                "anonymousChat": mode
            }
        }
        data = requests.post(self._url + api["get"]["groupConfig"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if not self._isSlice:
                if data["code"] == 0:
                    self._c.log("[Notice]：群配置修改成功",
                                "详细：" + str(self._target) + "(anonymousChat) <- '" + str(mode) + "'",
                                style="#a4ff8f")
                else:
                    self._c.log("[Error]：群配置修改失败", style="#ff8f8f")
            elif data["code"] != 0:
                self._c.log("[Error]：群配置修改失败", style="#ff8f8f")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)


def getGroupConfig(url, session, target: int):
    # 获取群配置信息
    message = {"sessionKey": session, "target": target}
    data = requests.get(url=url + api["get"]["groupConfig"], params=message)
    if data.status_code == 200:
        data = json.loads(data.text)
        if "code" not in data:
            return data
        else:
            return "error"
