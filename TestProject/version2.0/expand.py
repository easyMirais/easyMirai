import re

try:
    from rich.console import Console

    rh: bool = True
except ImportError as ip:
    rh: bool = False

import requests as po

import json

import models

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
    "upload": {
        "uploadImage": "/uploadImage"
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
        return models.echoTypeMode(data)

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
        return models.echoTypeMode(data)

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
        return models.echoTypeMode(data)

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
        return models.echoTypeMode(data)

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
        return models.echoTypeMode(data)


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
        return models.echoTypeMode(data)

    @property
    def friend(self):
        return self._context("friend", self._path)

    @property
    def group(self):
        return self._context("group", self._path)

    @property
    def temp(self):
        return self._context("temp", self._path)


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
