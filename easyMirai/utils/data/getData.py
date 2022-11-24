#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : SFNCO-Studio
# @Time     : 2022/11/24 17:08
# @File     : getData.py
# @Project  : Deep in easyMirai
# @Uri      : https://sfnco.com.cn/
import json
import os


def getApi(fileName: str) -> dict:
    path = os.path.abspath(os.path.join(os.path.dirname(
        __file__), f"{fileName.lower()}.json"))
    if os.path.exists(path):
        with open(path, encoding="utf8") as f:
            return json.loads(f.read())
