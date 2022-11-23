import json

from rich.console import Console
import requests as po

from .expand.utils import getApi
from .expand.echo import echoTypeMode

from .expand.getMessage import GetMessage
from .expand.getList import GetList
from .expand.getProFile import GetProFile
from .expand.setGroupConfig import SetGroupConfig

api = getApi("models")


class setTypeMode:
    def __init__(self, session: str, uri: str):
        self._url = uri
        self._session = session
        self._c = Console()

    def essence(self, target: int):
        data = {
            "sessionKey": self._session,
            "target": target,
        }
        data = po.post(self._url + api["set"]["essence"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：设置成功",
                            "详细：群精华消息(set) <- " + str(target),
                            style="#a4ff8f")
            else:
                self._c.log("[Error]：设置失败", style="#ff8f8f")
        return echoTypeMode(data)

    @property
    def message(self):
        return GetMessage(self._url, self._session)

    @property
    def list(self):
        return GetList(self._url, self._session)

    @property
    def proFile(self):
        return GetProFile(self._url, self._session)

    def group(self, target: int):
        # 修改群相关设置
        return SetGroupConfig(self._url, self._session, target)
