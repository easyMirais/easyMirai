import http
import json

import atexit

import requests as req

from easyMirai.sendType import sendTypeMode
from easyMirai.getType import getTypeMode
from easyMirai.setType import setTypeMode
from easyMirai.uploadType import uploadTypeMode
from easyMirai.actionType import actionTypeMode
from easyMirai.eventType import eventTypeMode

from easyMirai.globalvar import Uri, BotID, Key, Session, IsSlice
from easyMirai.logger.logger import Logger

from easyMirai.__version__ import __version__

_config = {
    "about": "/about",
    "verify": "/verify",
    "bind": "/bind",
    "release": "/release",
}


class Init:
    def __init__(self, host: str, port: int, botId: str, key: str, isSlice: bool = False):
        Uri().set(host + ":" + str(port))
        BotID().set(botId)
        Key().set(key)
        IsSlice().set(isSlice)

        self._c = Logger(IsSlice().get)
        self.__version__ = __version__
        self._c.Notice("当前easyMirai版本为 " + self.__version__)
        self._c.Notice("项目文档&使用教程：https://github.com/easyMirais/easyMirai/wiki")
        self._beginSession()
        self._testServer()
        self._isSlice = isSlice

    def _testServer(self):
        # 测试服务器是否正常开启
        try:
            request = req.get(url=Uri().get + _config["about"], timeout=5)
        except Exception:
            self._c.Alert("地址或端口有误，详细：未查询到Mirai HTTP服务器")
            exit()
        if request.status_code == http.HTTPStatus.OK:
            data = json.loads(request.text)
            if data["code"] == 0:
                version = data["data"]["version"]
                self._c.Notice("当前Mirai-HTTP-API版本为 " + version + " ，详细: 已查询到Mirai HTTP服务器")
        else:
            self._c.Alert("地址或端口有误，详细：未查询到Mirai HTTP服务器")
            exit()

    def _beginSession(self):
        data = {
            "verifyKey": Key().get
        }
        data = req.post(url=Uri().get + _config["verify"], data=json.dumps(data))
        if data.status_code == http.HTTPStatus.OK:
            data = json.loads(data.text)
            if data["code"] == 0:
                Session().set(data["session"])
            else:
                self._c.Error("获取Session失败")

        data = {
            "sessionKey": Session().get,
            "qq": BotID().get
        }

        data = req.post(url=Uri().get + _config["bind"], data=json.dumps(data))
        if data.status_code == http.HTTPStatus.OK:
            data = json.loads(data.text)
            if data["code"] == 0:
                self._c.Notice("绑定Session成功 详细：session=" + Session().get)
            else:
                self._c.Error("绑定Session失败:" + data["msg"])


class Mirai(Init):
    @property
    def send(self):
        return sendTypeMode()

    @property
    def get(self):
        return getTypeMode()

    @property
    def set(self):
        return setTypeMode()

    @property
    def upload(self):
        return uploadTypeMode()

    @property
    def action(self):
        return actionTypeMode()

    def event(self, eventId: int):
        return eventTypeMode(session=Session().get, uri=Uri().get, eventId=eventId, isSlice=IsSlice().get)


@atexit.register
def _stop():
    _c = Logger(IsSlice().get)
    data = {
        "sessionKey": Session().get,
        "qq": BotID().get
    }
    try:
        data = req.post(url=Uri().get + _config["release"], data=json.dumps(data))
    except Exception as re:
        _requests = re
        exit(404)
    if data.status_code == 200:
        data = json.loads(data.text)
        if data["code"] == 0:
            _c.Notice("释放Session成功 详细：session=" + Session().get)
