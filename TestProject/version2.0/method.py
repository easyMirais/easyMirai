import json
import models
from concurrent.futures import ThreadPoolExecutor

try:
    import requests as req

    ire: bool = True
except ImportError as ip:
    ire: bool = False

try:
    from rich.console import Console

    rh: bool = True
except ImportError as ip:
    rh: bool = False

_config = {
    "about": "/about",
    "verify": "/verify",
    "bind": "/bind",
}


class Init:
    def __init__(self, host: str, port: str, botId: str, key: str, count: int = 0, maxWork: int = 8):
        self.host: str = host
        self.port: str = port
        self.botId: str = botId
        self.key: str = key
        self.session: str = ""
        self.count: int = count
        self.c = Console()
        self.url = self.host + ":" + self.port  # 格式化Bot HTTP API地址
        self._testServer()
        self.pool = self._createPool(maxWork)  # 创建线程池
        self._beginSession()

    def _testServer(self):
        # 测试服务器是否正常开启
        try:
            request = req.get(url=self.url + _config["about"], timeout=5)
        except Exception as re:
            request = ""
            self.c.log("[Alert]：地址或端口有误，详细：查询不到Mirai服务器", style="#fb48a0")
            exit()
        if request.status_code == 200:
            data = json.loads(request.text)
            if data["code"] == 0:
                version = data["data"]["version"]
                self.c.log("[Notice]：当前Mirai-HTTP-API版本为 " + version + " ，详细: 已查询到Mirai服务器", style="#a4ff8f")

    def _createPool(self, maxWork: int):
        pool = ThreadPoolExecutor(maxWork)
        self.c.log("[Notice]：成功创建容量为" + str(maxWork) + "的线程池", style="#a4ff8f")
        return pool

    def _beginSession(self):
        data = {
            "verifyKey": self.key
        }
        data = req.post(url=self.url + _config["verify"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self.session = data["session"]
            else:
                self.c.log("[Error]：获取Session失败", style="#ff8f8f")

        data = {
            "sessionKey": self.session,
            "qq": self.botId
        }
        data = req.post(url=self.url + _config["bind"], data=json.dumps(data))
        if data.status_code == 200:
            data = json.loads(data.text)
            if data["code"] == 0:
                self.c.log("[Notice]：绑定Session成功", "详细：session=" + self.session, style="#a4ff8f")
            else:
                self.c.log("[Error]：绑定Session失败", style="#ff8f8f")


class Mirai(Init):
    @property
    def send(self):
        return models.targetMode(session=self.session, uri=str(self.url))
