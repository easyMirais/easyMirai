import json
import re

from rich.console import Console
import requests as po

from .echo import echoTypeMode
from .utils import getApi
from .other import uploadImage

api = getApi("expand")


class Temp:
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
        data = po.post(self._url + api["send"]["temp"]["sendTempMessage"], data=json.dumps(data))
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
                        "url": uploadImage(path, self._session, "group", self._url)
                    }
                ]
            }
        data = po.post(self._url + api["send"]["temp"]["sendTempMessage"], data=json.dumps(data))
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
        data = po.post(self._url + api["send"]["temp"]["sendTempMessage"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：表情发送成功",
                            "详细：" + str(self._target) + "(Group " + str(self._gid) + ") <- '" + str(faceId) + "'",
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：表情发送失败", style="#ff8f8f")
        return echoTypeMode(data)
