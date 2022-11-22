import json
from .models import (
    sendTypeMode,
    getTypeMode,
    setTypeMode,
    uploadTypeMode,
    actionTypeMode,
    eventTypeMode
)
from concurrent.futures import ThreadPoolExecutor
import atexit

import requests as req
from rich.console import Console

_config = {
    "about": "/about",
    "verify": "/verify",
    "bind": "/bind",
    "release": "/release",
    "data": {
        "url": "",
        "session": "",
        "botId": ""
    }
}


class Init:
    def __init__(self, host: str, port: str, botId: str, key: str, maxWork: int = 8):
        self._host: str = host
        self._port: str = port
        self._botId: str = botId
        self._key: str = key
        self._session: str = ""
        self._c = Console()
        self._url = self._host + ":" + self._port  # 格式化Bot HTTP API地址
        self._testServer()
        self._pool = self._createPool(maxWork)  # 创建线程池
        self._beginSession()
        _config["data"]["url"] = self._url
        _config["data"]["botId"] = self._botId
        _config["data"]["session"] = self._session

    def _testServer(self):
        # 测试服务器是否正常开启
        try:
            request = req.get(url=self._url + _config["about"], timeout=5)
        except Exception as re:
            request = re
            self._c.log("[Alert]：地址或端口有误，详细：未查询到Mirai HTTP服务器", style="#fb48a0")
            exit(404)
        if request.status_code == 200:
            data = json.loads(request.text)
            if data["code"] == 0:
                version = data["data"]["version"]
                self._c.log("[Notice]：当前Mirai-HTTP-API版本为 " + version + " ，详细: 已查询到Mirai HTTP服务器", style="#a4ff8f")

    def _createPool(self, maxWork: int):
        pool = ThreadPoolExecutor(maxWork)
        self._c.log("[Notice]：成功创建容量为 " + str(maxWork) + " 的线程池", style="#a4ff8f")
        return pool

    def _beginSession(self):
        data = {
            "verifyKey": self._key
        }
        data = req.post(url=self._url + _config["verify"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._session = data["session"]
            else:
                self._c.log("[Error]：获取Session失败", style="#ff8f8f")

        data = {
            "sessionKey": self._session,
            "qq": self._botId
        }
        data = req.post(url=self._url + _config["bind"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.log("[Notice]：绑定Session成功", "详细：session=" + self._session, style="#a4ff8f")
            else:
                self._c.log("[Error]：绑定Session失败", style="#ff8f8f")


class Mirai(Init):

    def __repr__(self):
        return "请选择一个操作模式"

    # 开放接口
    @property
    def send(self):
        return sendTypeMode(session=self._session, uri=str(self._url))

    @property
    def get(self):
        return getTypeMode(session=self._session, uri=str(self._url))

    @property
    def set(self):
        return setTypeMode(session=self._session, uri=str(self._url))

    @property
    def upload(self):
        return uploadTypeMode(session=self._session, uri=str(self._url))

    @property
    def action(self):
        return actionTypeMode(session=self._session, uri=str(self._url))

    def event(self, eventId: int):
        return eventTypeMode(session=self._session, uri=str(self._url), eventId=eventId)

    # todo 添加File操作类


@atexit.register
def _stop():
    _c = Console()
    data = {
        "sessionKey": _config["data"]["session"],
        "qq": _config["data"]["botId"]
    }
    try:
        data = req.post(url=_config["data"]["url"] + _config["release"], data=json.dumps(data))
    except Exception as re:
        requests = re
        _c.log("[Alert]：地址或端口有误，详细：未查询到Mirai HTTP服务器，无法注销Session", style="#fb48a0")
        exit(404)
    if data.status_code == 200:
        data = json.loads(data.text)
        if data["code"] == 0:
            _c.log("[Notice]：释放Session成功", "详细：session=" + _config["data"]["session"], style="#a4ff8f")
        else:
            _c.log("[Error]：释放Session失败", style="#ff8f8f")
