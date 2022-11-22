import json

from rich.console import Console
import requests as po

from .expand.echo import echoTypeMode
from .expand.getMessage import GetMessage
from .expand.getList import GetList
from .expand.getProFile import GetProFile
from .expand.utils import getApi

api = getApi("models")


class getTypeMode:
    def __init__(self, session: str, uri: str):
        self._url = uri
        self._session = session
        self._c = Console()

    def _get(self, message: str):
        data = po.get(self._url + str(api["get"]["info"]))
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
    def info(self):
        return self._get("插件信息")

    @property
    def message(self):
        return GetMessage(self._url, self._session)

    @property
    def list(self):
        return GetList(self._url, self._session)

    @property
    def proFile(self):
        return GetProFile(self._url, self._session)

    def groupConfig(self, target: int):
        data = {
            "sessionKey": self._session,
            "target": target
        }
        data = po.get(self._url + api["get"]["groupConfig"], params=data)
        if data.status_code == 200:
            data = json.loads(data.text)
            if "code" not in data:
                self._c.log("[Notice]：获取成功",
                            "详细：获取群设置(get) <- " + str(target),
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：获取失败", style="#ff8f8f")
        return echoTypeMode(data)
