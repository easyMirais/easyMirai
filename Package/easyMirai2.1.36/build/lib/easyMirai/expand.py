import re
from rich.console import Console

import requests as po

import json


_config = {
    "send": {
        "friend": {
            "sendFriendMessage": "/sendFriendMessage"
        },
        "group": {
            "sendGroupMessage": "/sendGroupMessage"
        },
        "temp": {
            "sendTempMessage": "/sendTempMessage"
        },
        "nudge": {
            "sendNudge": "/sendNudge"
        }
    },
    "action": {
        "mute": "/mute",
        "unmute": "/unmute",
        "muteAll": "/muteAll",
        "unmuteAll": "/unmuteAll",
        "kick": "/kick",
        "quit": "/quit",
        "deleteFriend": "/deleteFriend",
    },
    "event": {
        "newFriend": "/resp/newFriendRequestEvent",
    },
    "upload": {
        "uploadImage": "/uploadImage",
    },
    "get": {
        "count": "/countMessage",
        "fetchMessage": "/fetchMessage",
        "fetchLatestMessage": "/fetchLatestMessage",
        "peekMessage": "/peekMessage",
        "peekLatestMessage": "/peekLatestMessage",
        "messageFromId": "/messageFromId",
        "friendList": "/friendList",
        "groupList": "/groupList",
        "memberList": "/memberList",
        "friendProfile": "/friendProfile",
        "botProfile": "/botProfile",
        "memberProfile": "/memberProfile",
        "userProfile": "/userProfile",
        "groupConfig": "/groupConfig",
    }
}


class expandPoke:
    def __init__(self, url, session, target):
        self._url = url
        self._session = session
        self._target = target
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
        data = po.post(self._url + _config["send"]["friend"][to], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：戳一戳发送成功", "详细：" + str(self._target) + "(Friend) <- '" + name + "'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：戳一戳发送失败", style="#ff8f8f")
        return echoTypeMode(data)

    @property
    def poke(self):
        return self._context("poke", "sendFriendMessage")

    @property
    def FangDaZhao(self):
        return self._context("FangDaZhao", "sendFriendMessage")


class expandNudge:
    def __init__(self, url, session, target):
        self._url = url
        self._session = session
        self._target = target
        self._c = Console()

    def _context(self, name: str, by: str, to: str, subject: int):
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "subject": subject,
            "kind": name
        }
        data = po.post(self._url + _config["send"][by][to], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：捏捏发送成功",
                            "详细：" + str(self._target) + "(" + name + " " + str(subject) + ") <- '捏捏'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：捏捏发送失败", style="#ff8f8f")
        return echoTypeMode(data)

    @property
    def friend(self):
        return self._context("Friend", "nudge", "sendNudge", self._target)

    def group(self, gid: int):
        return self._context("Group", "nudge", "sendNudge", gid)


class expandTemp:
    def __init__(self, url, session, target, gid):
        self._url = url
        self._session = session
        self._target = target
        self._gid = gid
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
        print(data)
        data = po.post(self._url + _config["send"]["temp"]["sendTempMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：文本发送成功",
                            "详细：" + str(self._target) + "(Temp " + str(self._gid) + ") <- '" + str(context) + "'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：文本发送失败", style="#ff8f8f")
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
        data = po.post(self._url + _config["send"]["temp"]["sendTempMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
        if data["code"] == 0:
            self._c.log("[Notice]：图片发送成功",
                        "详细：" + str(self._target) + "(Temp " + str(self._gid) + ") <- '" + str(path) + "'",
                        style="#a4ff8f")
        else:
            self._c.log("[Error]：图片发送失败", style="#ff8f8f")
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
        data = po.post(self._url + _config["send"]["temp"]["sendTempMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：表情发送成功",
                            "详细：" + str(self._target) + "(Group " + str(self._gid) + ") <- '" + str(faceId) + "'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：表情发送失败", style="#ff8f8f")
        return echoTypeMode(data)


class expandGetMessage:
    def __init__(self, url, session):
        self._url = url
        self._session = session
        self._c = Console()

    def _request(self, message, to: str, params: dict):
        data = po.get(self._url + str(_config["get"][to]), params=params)
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：获取成功",
                            "详细：" + message + "(get) <- '获取信息'",
                            style="#a4ff8f")
            else:
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


class expandGetList:
    def __init__(self, url, session):
        self._url = url
        self._session = session
        self._c = Console()

    def _request(self, message, to: str, params: dict):
        data = po.get(self._url + str(_config["get"][to]), params=params)
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：获取成功",
                            "详细：" + message + "(get) <- '获取'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：获取失败", style="#ff8f8f")
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


class expandGetProFile:
    def __init__(self, url, session):
        self._url = url
        self._session = session
        self._c = Console()

    def _request(self, message, to: str, params: dict):
        data = po.get(self._url + str(_config["get"][to]), params=params)
        if data.status_code == 200:
            data = json.loads(data.text)
            if "code" not in data:
                self._c.log("[Notice]：获取成功",
                            "详细：" + message + "(get) <- '获取资料页'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：获取失败", style="#ff8f8f")
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


class expandSetGroupConfig:
    # 修改群设置
    def __init__(self, url, session, target: int):
        self._url = url
        self._session = session
        self._target = target
        self._c = Console()

    def name(self, name: str):
        # 修改群名称
        data = _getGroupConfig(self._url, self._session, self._target)
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
        data = po.post(self._url + _config["get"]["groupConfig"], data=json.dumps(data))
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
        data = _getGroupConfig(self._url, self._session, self._target)
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
        data = po.post(self._url + _config["get"]["groupConfig"], data=json.dumps(data))
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
        data = _getGroupConfig(self._url, self._session, self._target)
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
        data = po.post(self._url + _config["get"]["groupConfig"], data=json.dumps(data))
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
        data = _getGroupConfig(self._url, self._session, self._target)
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
        data = po.post(self._url + _config["get"]["groupConfig"], data=json.dumps(data))
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
        data = _getGroupConfig(self._url, self._session, self._target)
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
        data = po.post(self._url + _config["get"]["groupConfig"], data=json.dumps(data))
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
        data = _getGroupConfig(self._url, self._session, self._target)
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
        data = po.post(self._url + _config["get"]["groupConfig"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：群配置修改成功",
                            "详细：" + str(self._target) + "(anonymousChat) <- '" + str(mode) + "'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：群配置修改失败", style="#ff8f8f")
        return echoTypeMode(data)


class expandEventNewFriend:
    def __init__(self, url, session, target, eventId, groupId):
        self._url = url
        self._session = session
        self._target = target
        self._eventId = eventId
        self._groupId = groupId
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
        data = po.post(self._url + _config["event"]["newFriend"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：好友添加事件处理成功",
                            "详细：" + str(self._target) + "(Friend) <- '" + str(code) + "'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：好友添加事件处理失败", style="#ff8f8f")
        return echoTypeMode(data)

    def yes(self, message: str = ""):
        return self._request(1, self._eventId, message)

    def no(self, message: str = ""):
        return self._request(0, self._eventId, message)

    def black(self, message: str = ""):
        return self._request(2, self._eventId, message)


class expandEventJoinGroup:
    def __init__(self, url, session, target, eventId, groupId):
        self._url = url
        self._session = session
        self._target = target
        self._eventId = eventId
        self._groupId = groupId
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
        data = po.post(self._url + _config["event"]["newFriend"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：用户入群申请事件处理成功",
                            "详细：" + str(self._target) + "(Friend) <- '" + str(code) + "'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：用户入群申请事件处理失败", style="#ff8f8f")
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


class expandEventBotJoinGroup:
    def __init__(self, url, session, target, eventId, groupId, fromId):
        self._url = url
        self._session = session
        self._target = target
        self._eventId = eventId
        self._groupId = groupId
        self._fromId = fromId
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
        data = po.get(self._url + _config["event"]["newFriend"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：用户入群申请事件处理成功",
                            "详细：" + str(self._target) + "(Friend) <- '" + str(code) + "'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：用户入群申请事件处理失败", style="#ff8f8f")
        return echoTypeMode(data)

    def yes(self, message: str = ""):
        return self._request(1, message)

    def no(self, message: str = ""):
        return self._request(0, message)


class expandUploadImage:
    def __init__(self, url, session, path):
        self._url = url
        self._session = session
        self._path = path
        self._c = Console()

    def _context(self, name: str, subject: int):
        message = {"sessionKey": self._session, "type": name}
        onfiles = {'img': ('send.png', open(subject, 'rb'), 'image/png', {})}
        data = po.request(method="POST",
                          url=self._url + "/uploadImage", data=message, files=onfiles)
        if data.status_code == 200:
            data = json.loads(data.text)
            if "code" not in data:
                self._c.log("[Notice]：图片上传成功",
                            "详细：Cloud(" + name + " " + str(subject) + ") <- '" + self._path + "'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：图片上传失败", style="#ff8f8f")
        return echoTypeMode(data)

    @property
    def friend(self):
        return self._context("friend", self._path)

    @property
    def group(self):
        return self._context("group", self._path)

    @property
    def temp(self):
        return self._context("temp", self._path)


class expandActionGroup:
    def __init__(self, url, session, gid):
        self._url = url
        self._session = session
        self._target = gid
        self._c = Console()

    def mute(self, target: int):
        return expandActionGroupMute(self._url, self._session, self._target, target)

    def unmute(self, target: int):
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "memberId": target,
        }
        data = po.post(self._url + _config["action"]["unmute"], data=json.dumps(data))
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
        data = po.post(self._url + _config["action"]["muteAll"], data=json.dumps(data))
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
        data = po.post(self._url + _config["action"]["unmuteAll"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)

            if data["code"] == 0:
                self._c.log("[Notice]：全体禁言成功",
                            "详细：" + str(self._target) + "(Group) <- 'unMuteAll'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：全体禁言失败", style="#ff8f8f")
        return echoTypeMode(data)

    def kick(self, target: int):
        data = {
            "sessionKey": self._session,
            "target": self._target,
            "memberId": target,
            "msg": "您已被移出群聊"
        }
        data = po.post(self._url + _config["action"]["kick"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：移除群成员成功",
                            "详细：" + str(self._target) + "(Group) <- '" + str(target) + "'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：移除群成员失败", style="#ff8f8f")
        return echoTypeMode(data)

    @property
    def quit(self):
        data = {
            "sessionKey": self._session,
            "target": self._target,
        }
        data = po.post(self._url + _config["action"]["quit"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：退出群聊成功",
                            "详细：" + str(self._target) + "(Group) <- 'quit'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：退出群聊失败", style="#ff8f8f")
        return echoTypeMode(data)


class expandActionFriend:
    def __init__(self, url, session):
        self._url = url
        self._session = session
        self._c = Console()

    def deleteFriend(self, target: int):
        data = {
            "sessionKey": self._session,
            "target": target,
        }
        data = po.post(self._url + _config["action"]["deleteFriend"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：移除好友成功",
                            "详细：" + str(target) + "(Friend) <- 'deleteFriend'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：移除好友失败", style="#ff8f8f")
        return echoTypeMode(data)


class expandActionGroupMute:
    def __init__(self, url, session, target, memberId):
        self._url = url
        self._session = session
        self._target = target
        self._memberId = memberId
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
        data = po.post(self._url + _config["action"]["mute"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：禁言成功",
                            "详细：" + str(self._target) + "(Group) <- '" + str(time) + " s " + str(self._memberId) + "'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：禁言失败", style="#ff8f8f")
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


def _uploadImage(path: str, session, name, url: str):
    message = {"sessionKey": session, "type": name}
    onfiles = {'img': ('send.png', open(path, 'rb'), 'image/png', {})}
    data = po.request(method="POST", url=url + "/uploadImage", data=message, files=onfiles)
    if data.status_code == 200:
        data = json.loads(data.text)
        if "code" not in data:
            return data["url"]
        else:
            return "error"


def _getGroupConfig(url, session, target: int):
    # 获取群配置信息
    message = {"sessionKey": session, "target": target}
    data = po.get(url=url + _config["get"]["groupConfig"], params=message)
    if data.status_code == 200:
        data = json.loads(data.text)
        if "code" not in data:
            return data
        else:
            return "error"
