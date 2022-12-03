#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : SFNCO-Studio
# @Time     : 2022/11/24 19:41
# @File     : uploadType.py
# @Project  : Deep in easyMirai
# @Uri      : https://sfnco.com.cn/


import json
import os

from rich.console import Console
import requests

from easyMirai.echo.echoTypeMode import echoTypeMode
from easyMirai.data.getData import getApi

api = getApi("expand")


class uploadTypeMode:
    # 上传模式
    def __init__(self, session: str, uri: str, isSlice: bool):
        self._session = session
        self._url = uri
        self._isSlice = isSlice

    def __repr__(self):
        return "请选择上传模式"

    def image(self, path: str):
        return UploadImage(self._url, self._session, path, self._isSlice)


class UploadImage:
    def __init__(self, uri: str, session: str, path: str, isSlice: bool):
        self._uri = uri
        self._session = session
        self._path = path
        self._isSlice = isSlice
        self._c = Console()

    def _context(self, name: str, subject: str):
        message = {"sessionKey": self._session, "type": name}
        subject = os.path.abspath(os.path.join(os.path.dirname(
            __file__), "../", f"{subject.lower()}"))  # todo 打包时一定注意！！！！
        onfiles = {'img': ('send.png', open(subject, 'rb'), 'image/png', {})}
        data = requests.request(method="POST",
                                url=self._uri + "/uploadImage", data=message, files=onfiles)
        if data.status_code == 200:
            data = json.loads(data.text)
            if "code" not in data:
                if not self._isSlice:
                    if "code" not in data:
                        self._c.log("[Notice]：图片上传成功",
                                    "详细：Cloud(" + name + " " + str(subject) + ") <- '" + self._path + "'",
                                    style="#a4ff8f")
                    else:
                        self._c.log("[Error]：图片上传失败", style="#ff8f8f")
                elif data["code"] != 0:
                    self._c.log("[Error]：图片上传失败", style="#ff8f8f")
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
