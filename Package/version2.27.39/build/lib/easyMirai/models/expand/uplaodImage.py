import json

from rich.console import Console
import requests as po

from .echo import echoTypeMode
from .utils import getApi

api = getApi("expand")


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
