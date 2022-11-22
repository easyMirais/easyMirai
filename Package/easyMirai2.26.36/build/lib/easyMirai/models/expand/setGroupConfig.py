import json

from rich.console import Console
import requests as po

from .echo import echoTypeMode
from .other import getGroupConfig
from .utils import getApi

api = getApi("expand")


class SetGroupConfig:
    # 修改群设置
    def __init__(self, url, session, target: int):
        self._url = url
        self._session = session
        self._target = target
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
        data = po.post(self._url + api["get"]["groupConfig"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：群配置修改成功",
                            "详细：" + str(self._target) + "(name) <- '" + str(name) + "'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：群配置修改失败", style="#ff8f8f")
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
        data = po.post(self._url + api["get"]["groupConfig"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：群配置修改成功",
                            "详细：" + str(self._target) + "(announcement) <- '" + str(content) + "'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：群配置修改失败", style="#ff8f8f")
        return echoTypeMode(data)

    # todo 完成群配置设置函数 还差4个选项
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
        data = po.post(self._url + api["get"]["groupConfig"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：群配置修改成功",
                            "详细：" + str(self._target) + "(confessTalk) <- '" + str(mode) + "'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：群配置修改失败", style="#ff8f8f")
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
        data = po.post(self._url + api["get"]["groupConfig"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：群配置修改成功",
                            "详细：" + str(self._target) + "(allowMemberInvite) <- '" + str(mode) + "'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：群配置修改失败", style="#ff8f8f")
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
        data = po.post(self._url + api["get"]["groupConfig"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：群配置修改成功",
                            "详细：" + str(self._target) + "(autoApprove) <- '" + str(mode) + "'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：群配置修改失败", style="#ff8f8f")
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
        data = po.post(self._url + api["get"]["groupConfig"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：群配置修改成功",
                            "详细：" + str(self._target) + "(anonymousChat) <- '" + str(mode) + "'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：群配置修改失败", style="#ff8f8f")
        return echoTypeMode(data)
