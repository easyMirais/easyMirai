import json

import requests as po

from .utils import getApi

api = getApi("expand")


def getGroupConfig(url, session, target: int):
    # 获取群配置信息
    message = {"sessionKey": session, "target": target}
    data = po.get(url=url + api["get"]["groupConfig"], params=message)
    if data.status_code == 200:
        data = json.loads(data.text)
        if "code" not in data:
            return data
        else:
            return "error"


def uploadImage(path: str, session, name, url: str):
    message = {"sessionKey": session, "type": name}
    onfiles = {'img': ('send.png', open(path, 'rb'), 'image/png', {})}
    data = po.request(method="POST", url=url + "/uploadImage", data=message, files=onfiles)
    if data.status_code == 200:
        data = json.loads(data.text)
        if "code" not in data:
            return data["url"]
        else:
            return "error"
