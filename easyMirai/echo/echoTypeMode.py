#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : SFNCO-Studio
# @Time     : 2022/11/24 16:52
# @File     : echoTypeMode.py
# @Project  : Deep in easyMirai
# @Uri      : https://sfnco.com.cn/
import json

"""
将输出格式化方便调用
"""


class echoTypeMode:

    def __init__(self, context: dict):
        self._context = context

    def __repr__(self):
        return "<Request [OK]>"

    @property
    def json(self) -> str:
        """
        将返回值格式化为字符串类型
        @return: str
        """
        data = json.dumps(self._context)
        return data

    @property
    def dictionary(self) -> dict:
        """
        将返回值格式化为字典类型
        @return: dict
        """
        return self._context
