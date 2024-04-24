#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : SFNCO-Studio
# @Time     : 2022/11/24 19:41
# @File     : uploadType.py
# @Project  : Deep in easyMirai
# @Uri      : https://sfnco.com.cn/


import json
import os

import requests

from easyMirai.echo.echoTypeMode import echoTypeMode
from easyMirai.data.getData import getApi

from easyMirai.globalvar import Uri, Session, IsSlice
from easyMirai.logger import Logger

api = getApi("expand")


class uploadTypeMode:
    # 上传模式
    def __repr__(self):
        return "请选择上传模式"

    def image(self, path: str):
        return UploadImage(path)


class UploadImage:
    def __init__(self, path: str):
        self._path = path
        self._c = Logger(IsSlice().get)

    def _context(self, name: str, subject: str):
        message = {"sessionKey": Session().get, "type": name}
        subject = os.path.abspath(os.path.join(os.path.dirname(__file__), "../", f"{subject.lower()}"))
        onFiles = {'img': ('send.png', open(subject, 'rb'), 'image/png', {})}
        data = requests.request(method="POST", url=Uri().get + "/uploadImage", data=message, files=onFiles)
        if data.status_code == 200:
            data = json.loads(data.text)
            if "code" not in data:
                self._c.Notice("图片上传成功 详细：Cloud(" + name + " " + str(subject) + ") <- '" + self._path + "'")
            else:
                self._c.Error("图片上传失败")
        else:
            data = {"code": data.status_code, "msg": "网络错误"}
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
