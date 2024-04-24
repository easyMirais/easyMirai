#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : SFNCO-Studio
# @Time     : 2022/11/24 19:23
# @File     : setType.py
# @Project  : Deep in easyMirai
# @Uri      : https://sfnco.com.cn/
import json

import requests

from easyMirai.echo.echoTypeMode import echoTypeMode
from easyMirai.data.getData import getApi

from easyMirai.globalvar import Uri, BotID, Key, Session, IsSlice
from easyMirai.logger.logger import Logger

api = getApi("models")


class setTypeMode:
    def __init__(self):
        self._c = Logger(IsSlice().get)

    def essence(self, target: int):
        data = {
            "sessionKey": Session().get,
            "target": target,
        }
        data = requests.post(Uri().get + api["set"]["essence"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice("设置成功 详细：群精华消息(set) <- " + str(target))
            else:
                self._c.Error("设置失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

            return echoTypeMode(data)

    def group(self, target: int):
        # 修改群相关设置
        return SetGroupConfig(target)


class SetGroupConfig:
    # 修改群设置
    def __init__(self, target: int):
        self._target = target
        self._c = Logger(IsSlice().get)

    def name(self, name: str):
        # 修改群名称
        data = getGroupConfig(Uri().get, Session().get, self._target)
        if "announcement" not in data:
            data["announcement"] = ""
        data = {
            "sessionKey": Session().get,
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
        data = requests.post(Uri().get + api["get"]["groupConfig"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice("群配置修改成功 详细：" + str(self._target) + "(name) <- '" + str(name) + "'")
            else:
                self._c.Error("群配置修改失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def announcement(self, content: str):
        # 修改群名称
        data = getGroupConfig(Uri().get, Session().get, self._target)
        if "announcement" not in data:
            data["announcement"] = ""
        data = {
            "sessionKey": Session().get,
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
        data = requests.post(Uri().get + api["get"]["groupConfig"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice("群配置修改成功 详细：" + str(self._target) + "(announcement) <- '" + str(content) + "'")
            else:
                self._c.Error("群配置修改失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def confessTalk(self, mode: bool):
        data = getGroupConfig(Uri().get, Session().get, self._target)
        if "announcement" not in data:
            data["announcement"] = ""
        data = {
            "sessionKey": Session().get,
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
        data = requests.post(Uri().get + api["get"]["groupConfig"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice("群配置修改成功 详细：" + str(self._target) + "(confessTalk) <- '" + str(mode) + "'")
            else:
                self._c.Error("群配置修改失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def allowMemberInvite(self, mode: bool):
        data = getGroupConfig(Uri().get, Session().get, self._target)
        print(data)
        if "announcement" not in data:
            data["announcement"] = ""
        data = {
            "sessionKey": Session().get,
            "target": self._target,
            "config": {
                "name": data["name"],
                "announcement": data["announcement"],
                "confessTalk": data["confessTalk"],
                "allowMemberInvite": mode,
                "autoApprove": data["autoApprove"],
                "anonymousChat": data["anonymousChat"]
            }
        }
        data = requests.post(Uri().get + api["get"]["groupConfig"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice("群配置修改成功 详细：" + str(self._target) + "(confessTalk) <- '" + str(mode) + "'")
            else:
                self._c.Error("群配置修改失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def autoApprove(self, mode: bool):
        data = getGroupConfig(Uri().get, Session().get, self._target)
        if "announcement" not in data:
            data["announcement"] = ""
        data = {
            "sessionKey": Session().get,
            "target": self._target,
            "config": {
                "name": data["name"],
                "announcement": data["announcement"],
                "confessTalk": data["confessTalk"],
                "allowMemberInvite": data["allowMemberInvite"],
                "autoApprove": mode,
                "anonymousChat": data["anonymousChat"]
            }
        }
        data = requests.post(Uri().get + api["get"]["groupConfig"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice("群配置修改成功 详细：" + str(self._target) + "(autoApprove) <- '" + str(mode) + "'")
            else:
                self._c.Error("群配置修改失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)

    def anonymousChat(self, mode: bool):
        data = getGroupConfig(Uri().get, Session().get, self._target)
        if "announcement" not in data:
            data["announcement"] = ""
        data = {
            "sessionKey": Session().get,
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
        data = requests.post(Uri().get + api["get"]["groupConfig"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice("群配置修改成功 详细：" + str(self._target) + "(anonymousChat) <- '" + str(mode) + "'")
            else:
                self._c.Error("群配置修改失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}

        return echoTypeMode(data)


def getGroupConfig(url, session, target: int):
    # 获取群配置信息
    message = {"sessionKey": session, "target": target}
    data = requests.get(url=Uri().get + api["get"]["groupConfig"], params=message)
    if data.status_code == 200:
        data = json.loads(data.text)
        if "code" not in data:
            return data
        else:
            return "error"
