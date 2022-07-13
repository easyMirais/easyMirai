# -*- coding: utf-8 -*-

"""
一个是开发QBot更加简单的集成模块！
author: HexMikuMax & ExMikuPro
data: 2022/06/29
version: 1.0.39
"""

import json
import time

import requests
from rich.console import Console


class Init:
    # 初始化参数类
    def __init__(self, host: str, port: str, key: str, qid: str, count: str = "1", debug: int = 0, times: int = 1):
        """
        初始化配置
        :param host: Bot Http地址
        :param port: Bot Http端口
        :param key: Bot 认证Key
        :param qid: Bot 已登陆的QQ号
        :param count: 消息单次获取长度(可选)
        :param debug: 控制台调试输出错误等级(可选:0=None，1=Notice,2=Warning,3=Error)
        :param times: 延迟时间秒(可选)
        """
        self.host: str = host
        self.port: str = port
        self.key: str = key
        self.qid: str = qid
        self.count: str = count
        self.session: str = ""
        self.debug: int = debug
        self.times: int = times
        self.version: str = "1.0.39"
        self.c = Console()  # 初始化debug控制台输出模块

    def Debug(self, msg, code: int):
        # 输出控制台
        # code: 0 成功 1 过程性错误 2 请求性错误 5 返回请求原数据
        """
        输出全部运行日志到控制台
        :param msg: 日志信息
        :param code: 错误等级
        :return: None
        """
        if self.debug != 0:
            if code == 0 and self.debug == 1:
                self.c.log("[Notice]：", msg, style="#a4ff8f")
            elif code == 1 and self.debug == 2 and self.debug == 1:
                self.c.log("[Warning]：", msg, style="#f6ff8f")
            elif code == 2 and self.debug == 3 and self.debug == 2 and self.debug == 1:
                self.c.log("[Error]：", msg, style="#ff8f8f")


class setup(Init):
    # Bot初始化类

    def begin(self) -> str:
        # 初始化机器人
        """
        获取并绑定Session到Bot
        :return: Bot: XXXX 初始化成功！
        """
        self.getSession()
        self.bindSession()
        self.Debug("初始化成功！", 0)
        return "Bot:" + self.qid + " 初始化成功！"

    def getSession(self):
        # 获取session状态码
        """
        获取session码
        :return:{'code': 0, 'session': 'XXXX'}
        """
        headers = {
            'Connection': 'close'
        }
        request = requests.post(url=self.host + ":" + self.port + "/verify", data='{"verifyKey": "' + self.key + '"}',
                                headers=headers)
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                self.session = request['session']
                self.Debug(request, 5)
                self.Debug("session获取成功！", 0)
                return request
            else:
                self.Debug("session获取失败！", 1)
                self.Debug(request["msg"], 1)

        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)

    def bindSession(self) -> str:
        # 绑定session到QQ机器人
        """
        绑定Session到QQ机器人
        :return: XXXX
        """
        headers = {
            'Connection': 'close'
        }
        request = requests.post(url=self.host + ":" + self.port + "/bind",
                                data='{"sessionKey": "' + self.session + '","qq": ' + self.qid + '}', headers=headers)
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                self.Debug("session绑定成功！", 0)
                self.Debug(request, 5)
                return self.session
            else:
                self.Debug("session绑定失败！", 1)
                self.Debug(request['msg'], 1)

        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)

    def releaseSession(self):
        # 释放session到QQBot
        """
        释放已经绑定Bot的Session
        :return: {'code': 0, 'msg': 'success'}
        """
        headers = {
            'Connection': 'close'
        }
        request = requests.post(url=self.host + ":" + self.port + "/release",
                                data='{"sessionKey": "' + self.session + '","qq": ' + self.qid + '}', headers=headers)
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                self.Debug("session注销成功！", 0)
                self.Debug(request, 5)
                return request
            else:
                self.Debug("session注销失败！", 1)
                self.Debug(request['msg'], 1)

        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)


class Message(setup):
    # 信息操作处理类
    def getCountMessage(self):
        # 获取消息列长度
        """
        获取消息队列的长度

        需要进行实例化后调用！！！

        :return: {'code': 0, 'msg': '', 'data': XXX}
        """
        params = {
            "sessionKey": self.session
        }
        headers = {
            'Connection': 'close'
        }
        request = requests.get(url=self.host + ":" + self.port + "/countMessage", params=params, headers=headers)
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                self.Debug(request, 5)
                self.Debug("获取消息长度成功！", 0)
                return request
            else:
                self.Debug("获取消息长度失败！", 1)
                self.Debug(request['msg'], 1)
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)

    def getFetchMessage(self) -> dict:
        # 获取队列头部消息后移除
        """
        获取队列头部消息后移除

        需要进行实例化后调用！！！

        :return: 输出文字序列（以实际情况为准）
        """
        params = {
            "sessionKey": self.session,
            "count": self.count
        }
        headers = {
            'Connection': 'close'
        }
        request = requests.get(url=self.host + ":" + self.port + "/fetchMessage", params=params, headers=headers)
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                self.Debug(request, 5)
                self.Debug("获取队列头部信息成功！", 0)
                return request['data']
            else:
                self.Debug("获取队列头部信息失败！", 1)
                self.Debug(request['msg'], 1)

        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)

    def getFetchLatestMessage(self):
        # 获取队列尾部消息后移除
        """
        获取队列尾部消息后移除

        需要进行实例化后调用！！！

        :return: 输出文字序列（以实际情况为准）
        """
        params = {
            "sessionKey": self.session,
            "count": self.count
        }
        headers = {
            'Connection': 'close'
        }
        request = requests.get(url=self.host + ":" + self.port + "/fetchLatestMessage", params=params, headers=headers)
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                self.Debug(request, 5)
                self.Debug("获取队列尾部信息成功！", 0)
                return request['data']
            else:
                self.Debug("获取队列尾部信息失败！", 1)
                self.Debug(request['msg'], 1)

        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)

    def getPeekMessage(self):
        # 获取队列头部消息后不移除
        """
        获取队列头部消息后不移除

        需要进行实例化后调用！！！

        :return: 输出文字序列（以实际情况为准）
        """
        params = {
            "sessionKey": self.session,
            "count": self.count
        }
        headers = {
            'Connection': 'close'
        }
        request = requests.get(url=self.host + ":" + self.port + "/PeekMessage", params=params, headers=headers)
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                self.Debug(request, 5)
                self.Debug("获取队列头部信息成功！", 0)
                return request['data']
            else:
                self.Debug("获取队列头部信息失败！", 1)
                self.Debug(request['msg'], 1)

        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)

    def getPeekLatestMessage(self) -> str:
        # 获取队列尾部消息后不移除
        """
        获取队列尾部消息后不移除

        需要进行实例化后调用！！！

        :return: 输出文字序列（以实际情况为准）
        """
        params = {
            "sessionKey": self.session,
            "count": self.count
        }
        headers = {
            'Connection': 'close'
        }
        request = requests.get(url=self.host + ":" + self.port + "/PeekLatestMessage", params=params, headers=headers)
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                self.Debug(request, 5)
                self.Debug("获取队列尾部信息成功！", 0)
                return request['data']
            else:
                self.Debug("获取队列尾部信息失败！", 1)
                self.Debug(request['msg'], 1)

        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)


class formatMessage(Message):
    # 信息格式化处理类(实际生产项目不建议使用)
    def getFetchMessageFormat(self):
        """
        格式化信息不建议使用
        :return:
        """
        message = self.getFetchMessage()
        return self.Format(message)

    def getFetchLatestMessageFormat(self):
        """
        格式化信息不建议使用
        :return:
        """
        message = self.getFetchLatestMessage()
        return self.Format(message)

    def getPeekMessageFormat(self):
        """
        格式化信息不建议使用
        :return:
        """
        message = self.getPeekMessage()
        return self.Format(message)

    def getPeekLatestMessageFormat(self):
        """
        格式化信息不建议使用
        :return:
        """
        message = self.getPeekLatestMessage()
        return self.Format(message)

    @staticmethod
    def Format(message):
        body = {"From": message[0]['type']}
        if body["From"] == 'GroupMessage':
            body["Sender"] = str(message[0]['sender']['id'])
            body["SenderName"] = str(message[0]['sender']['memberName'])
            body["Group"] = str(message[0]['sender']['group']['id'])
            body["GroupName"] = str(message[0]['sender']['group']['name'])
            body["Ops"] = str(message[0]['sender']['group']['permission'])
            for messageList in message[0]['messageChain']:
                if messageList['type'] == "At":
                    if 'At' in body:
                        body['At'].append(str(messageList['target']))
                    else:
                        body['At'] = list()
                        body['At'].append(str(messageList['target']))
                if messageList['type'] == "Plain":
                    if 'Plain' in body:
                        body['Plain'].append(messageList['text'])
                    else:
                        body['Plain'] = list()
                        body['Plain'].append(messageList['text'])
                if messageList['type'] == "Image":
                    if 'Image' in body:
                        body['Image'].append(messageList['url'])
                    else:
                        body['Image'] = list()
                        body['Image'].append(messageList['url'])
                if messageList['type'] == "Source":
                    if 'Source' in body:
                        body['Source'].append(messageList['id'])
                    else:
                        body['Source'] = list()
                        body['Source'].append(messageList['id'])
                if messageList['type'] == "Face":
                    if 'Face' in body:
                        body['Face'].append(messageList['name'])
                    else:
                        body['Face'] = list()
                        body['Face'].append(messageList['name'])
                    if 'FaceId' in body:
                        body['FaceId'].append(messageList['faceId'])
                    else:
                        body['FaceId'] = list()
                        body['FaceId'].append(messageList['faceId'])

        elif body['From'] == "FriendMessage":
            body['Sender'] = str(message[0]['sender']['id'])
            body['SenderName'] = str(message[0]['sender']['nickname'])
            for messageList in message[0]['messageChain']:
                if messageList['type'] == "Plain":
                    if 'Plain' in body:
                        body['Plain'].append(messageList['text'])
                    else:
                        body['Plain'] = list()
                        body['Plain'].append(messageList['text'])
                if messageList['type'] == "Image":
                    if 'Image' in body:
                        body['Image'].append(messageList['url'])
                    else:
                        body['Image'] = list()
                        body['Image'].append(messageList['url'])
                if messageList['type'] == "Source":
                    if 'Source' in body:
                        body['Source'].append(messageList['id'])
                    else:
                        body['Source'] = list()
                        body['Source'].append(messageList['id'])
        return body


class bot(formatMessage):
    # Bot信息获取类
    def getFriendList(self):
        # 获取Bot好友列表
        """
        获取Bot已经添加的好友列表
        :return:{'code': 0, 'msg': '', 'data': [{'id': XXXX, 'nickname': 'XXXX', 'remark': 'XXXX'}]}
        """
        params = {
            "sessionKey": self.session
        }
        headers = {
            'Connection': 'close'
        }
        request = requests.get(url=self.host + ":" + self.port + "/friendList", params=params, headers=headers)
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                self.Debug(request, 5)
                self.Debug("获取Bot好友列表成功！", 0)
                return request
            else:
                self.Debug("获取Bot好友列表失败！", 1)
                self.Debug(request['msg'], 1)

        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)

    def getMemberList(self, target: str):
        # 获取Bot加入群的群成员列表
        """
        获取Bot加入群的群成员列表
        :param target: 需要查询的群号
        :return:{'code': 0, 'msg': '', 'data': [XXXX]}
        """
        params = {
            "sessionKey": self.session,
            "target": target
        }
        headers = {
            'Connection': 'close'
        }
        request = requests.get(url=self.host + ":" + self.port + "/memberList", params=params, headers=headers)
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                self.Debug(request, 5)
                self.Debug("获取群成员列表成功！", 0)
                return request
            else:
                self.Debug("获取群成员列表失败！", 1)
                self.Debug(request['msg'], 1)

        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)

    def getGroupList(self):
        # 获取Bot加入的群列表
        """
        获取Bot已经加入的群列表
        :return:{'code': 0, 'msg': '', 'data': [{'id': XXXX, 'name': 'XXXX', 'permission': 'XXXX'}]}
        """
        params = {
            "sessionKey": self.session,
        }
        headers = {
            'Connection': 'close'
        }
        request = requests.get(url=self.host + ":" + self.port + "/groupList", params=params, headers=headers)
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                self.Debug(request, 5)
                self.Debug("获取群成员列表成功！", 0)
                return request
            else:
                self.Debug("获取群成员列表失败！", 1)
                self.Debug(request['msg'], 1)

        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)

    def botProfile(self):
        # 获取Bot机器人账号信息
        """
        获取Bot账号信息
        :return:{'nickname': 'XXXX', 'email': 'XXXX', 'age': XXXX, 'level': XXX, 'sign': 'XXXX', 'sex': 'XXXX'}
        """
        headers = {
            'Connection': 'close'
        }
        params = {
            "sessionKey": self.session
        }
        request = requests.get(url=self.host + ":" + self.port + "/botProfile", params=params, headers=headers)
        if request.status_code == 200:
            request = json.loads(request.text)
            self.Debug(request, 5)
            self.Debug("Bot信息获取成功！", 0)
            return request
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)

    def delay(self):
        time.sleep(self.times)


class friend(bot):
    # 好友相关操作类
    def sendFriendMessage(self, msg: dict, tar: str):
        # 发送好友消息
        """
        发送好友普通消息
        :param msg: 消息字典
        :param tar: 消息发送的目标
        :return:{'code': 0, 'msg': 'success', 'messageId': XXXX}
        """
        headers = {
            'Connection': 'close'
        }
        if len(msg) >= 0:
            message = json.dumps(msg)
            message = '{"sessionKey":"' + self.session + '","target":' + tar + ',"messageChain":[' + message + ']}'
            request = requests.post(url=self.host + ":" + self.port + "/sendFriendMessage", data=str(message),
                                    headers=headers)
            if request.status_code == 200:
                request = json.loads(request.text)
                if request['code'] == 0:
                    self.Debug(request, 5)
                    self.Debug("好友消息发送成功！", 0)
                    return request
                else:
                    self.Debug("发送好友信息失败！", 1)
                    self.Debug(request['msg'], 1)

            else:
                self.Debug("连接请求失败！请检查网络配置！", 2)

    def getUserProfile(self, target: str):
        # 获取好友/任意用户信息
        """
        获取好友已经公开的信息
        :param target: 获取对象ID号
        :return: 依据实际情况返回参数
        """
        params = {
            "sessionKey": self.session,
            "target": target,
        }
        headers = {
            'Connection': 'close'
        }
        request = requests.get(url=self.host + ":" + self.port + "/userProfile", headers=headers, params=params)
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                self.Debug(request, 5)
                self.Debug("好友资料成功！", 0)
                return request
            else:
                self.Debug("好友资料失败！", 1)
                self.Debug(request['msg'], 1)

        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)

    def deleteFriend(self, tar):
        # 删除好友
        """
        删除Bot已添加的好友
        :param tar: 好友Qid
        :return:
        """
        headers = {
            'Connection': 'close'
        }
        message = '{"sessionKey":"' + self.session + '","target":"' + tar + '"}'
        request = requests.post(url=self.host + ":" + self.port + "/deleteFriend", data=str(message),
                                headers=headers)
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                self.Debug(request, 5)
                self.Debug("好友删除成功！", 0)
                return request
            else:
                self.Debug("好友删除失败！", 1)
                self.Debug(request['msg'], 1)
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)


class group(friend):
    # 群相关操作类
    def sendGroupMessage(self, msg: dict, tar):
        # 发送群消息
        """
        发送群普通消息
        :param msg: 消息字典
        :param tar: 消息发送的目标
        :return:{'code': 0, 'msg': 'success', 'messageId': XXXX}
        """
        headers = {
            'Connection': 'close'
        }
        if len(msg) >= 0:
            message = json.dumps(msg)
            message = '{"sessionKey":"' + self.session + '","target":' + tar + ',"messageChain":[' + message + ']}'
            request = requests.post(url=self.host + ":" + self.port + "/sendGroupMessage", data=str(message),
                                    headers=headers)
            if request.status_code == 200:
                request = json.loads(request.text)
                if request['code'] == 0:
                    self.Debug(request, 5)
                    self.Debug("群消息发送成功！", 0)
                    return request
                else:
                    self.Debug("发送群信息失败！", 1)
                    self.Debug(request['msg'], 1)

            else:
                self.Debug("连接请求失败！请检查网络配置！", 2)

    def sendTempMessage(self, msg: dict, tar: str, qid: str):
        # 发送群临时消息
        """
        发送群临时消息
        :param msg: 消息字典
        :param tar: 临时信息发送的目标群
        :param qid: 临时信息发送的目标
        :return: {'code': 0, 'msg': 'success', 'messageId': XXXX}
        """
        headers = {
            'Connection': 'close'
        }
        if len(msg) >= 0:
            message = json.dumps(msg)
            message = '{"sessionKey":"' + self.session + '","qq":' + qid + ',"group":' + tar + ',"messageChain":[' + message + ']}'
            request = requests.post(url=self.host + ":" + self.port + "/sendTempMessage", data=str(message),
                                    headers=headers)
            if request.status_code == 200:
                request = json.loads(request.text)
                if request['code'] == 0:
                    self.Debug(request, 5)
                    self.Debug("群临时消息发送成功！", 0)
                    return request
                else:
                    self.Debug("发送群临时信息失败！", 1)
                    self.Debug(request['msg'], 1)

            else:
                self.Debug("连接请求失败！请检查网络配置！", 2)

    def getMemberProfile(self, target: str, memberId: str):
        # 获取群员信息
        """
        获取指定群员消息
        :param target: 目标群
        :param memberId: 目标群成员
        :return:{'nickname': 'XXXX', 'email': 'XXXX', 'age': XXXX, 'level': XXXX, 'sign': 'XXXX', 'sex': 'XXXX'}
        """
        params = {
            "sessionKey": self.session,
            "target": target,
            "memberId": memberId
        }
        headers = {
            'Connection': 'close'
        }
        request = requests.get(url=self.host + ":" + self.port + "/memberProfile", headers=headers, params=params)
        if request.status_code == 200:
            request = json.loads(request.text)
            self.Debug(request, 5)
            self.Debug("群成员资料成功！", 0)
            return request
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)

    def muteMember(self, target: str, memberId: str, times: str):
        # 禁言群成员
        """
        禁言制定群成员（需要相关群权限）
        :param target: 目标群
        :param memberId: 目标群成员
        :param times: 禁言时间（以秒为单位，最高30天）
        :return:{'code': 0, 'msg': 'success'}
        """
        headers = {
            'Connection': 'close'
        }
        me = memberId
        tar = target
        data = '{"sessionKey":"' + self.session + '","target":' + tar + ',"memberId":' + me + ',"time":' + times + '}'
        request = requests.post(url=self.host + ":" + self.port + "/mute", headers=headers, data=data)
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                self.Debug(request, 5)
                self.Debug("群成员禁言成功！", 0)
                return request
            else:
                self.Debug("群成员禁言失败！", 1)
                self.Debug(request['msg'], 1)

        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)

    def unMuteMember(self, target: str, memberId: str):
        # 解除群成员禁言
        """
        解除目标群员禁言（需要相关群权限）
        :param target: 目标群
        :param memberId: 目标群成员
        :return:{'code': 0, 'msg': 'success'}
        """
        headers = {
            'Connection': 'close'
        }
        me = memberId
        tar = target
        data = '{"sessionKey":"' + self.session + '","target":' + tar + ',"memberId":' + me + '}'
        request = requests.post(url=self.host + ":" + self.port + "/unmute", headers=headers, data=data)
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                self.Debug(request, 5)
                self.Debug("群成员禁言解除成功！", 0)
                return request
            else:
                self.Debug("群成员禁言解除失败！", 1)
                self.Debug(request['msg'], 1)

        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)

    def kick(self, target: str, memberId: str, msg: str):
        # 移除群成员
        """
        移除目标群员（需要相关群权限）
        :param msg: 移出群的提示信息
        :param target: 目标群
        :param memberId: 目标群成员
        :return:{'code': 0, 'msg': 'success'}
        """
        headers = {
            'Connection': 'close'
        }
        me = memberId
        tar = target
        msg = msg.encode("utf-8").decode("latin1")
        data = '{"sessionKey":"' + self.session + '","target":' + tar + ',"memberId":' + me + ',"msg":' + msg + '}'
        request = requests.post(url=self.host + ":" + self.port + "/kick", headers=headers, data=data)
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                self.Debug(request, 5)
                self.Debug("群成员移除成功！", 0)
                return request
            else:
                self.Debug("群成员移除失败！", 1)
                self.Debug(request['msg'], 1)

        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)

    def quitGroup(self, target: str):
        # 退出指定群聊
        """
        Bot退出指定群聊
        :param target: 目标群聊
        :return: {'code': 0, 'msg': 'success'}
        """
        headers = {
            'Connection': 'close'
        }
        tar = target
        data = '{"sessionKey":"' + self.session + '","target":' + tar + '}'
        request = requests.post(url=self.host + ":" + self.port + "/quit", headers=headers, data=data)
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                self.Debug(request, 5)
                self.Debug("退出群聊成功！", 0)
                return request
            else:
                self.Debug("退出群聊失败！", 1)
                self.Debug(request['msg'], 1)

        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)

    def muteAll(self, target: str):
        # 禁言指定群聊全体成员
        """
        禁言指定群聊全体成员
        :param target: 目标群聊
        :return: {'code': 0, 'msg': 'success'}
        """
        headers = {
            'Connection': 'close'
        }
        tar = target
        data = '{"sessionKey":"' + self.session + '","target":' + tar + '}'
        request = requests.post(url=self.host + ":" + self.port + "/muteAll", headers=headers, data=data)
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                self.Debug(request, 5)
                self.Debug("禁言全体群聊成员成功！", 0)
                return request
            else:
                self.Debug("禁言全体群聊成员失败！", 1)
                self.Debug(request['msg'], 1)

        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)

    def unMuteAll(self, target: str):
        # 解除指定群聊全体成员禁言
        """
        解除禁言指定群聊全体成员
        :param target: 目标群聊
        :return: {'code': 0, 'msg': 'success'}
        """
        headers = {
            'Connection': 'close'
        }
        tar = target
        data = '{"sessionKey":"' + self.session + '","target":' + tar + '}'
        request = requests.post(url=self.host + ":" + self.port + "/unmuteAll", headers=headers, data=data)
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                self.Debug(request, 5)
                self.Debug("解除禁言全体群聊成员成功！", 0)
                return request
            else:
                self.Debug("解除禁言全体群聊成员失败！", 1)
                self.Debug(request['msg'], 1)

        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)

    def setEssence(self, target: str):
        # 设置群精华消息
        """
        设置群精华消息
        :param target: 目标消息ID
        :return:{'code': 0, 'msg': 'success'}
        """
        headers = {
            'Connection': 'close'
        }
        data = '{"sessionKey":"' + self.session + '","target":' + target + '}'
        request = requests.post(url=self.host + ":" + self.port + "/setEssence", headers=headers, data=data)
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                self.Debug(request, 5)
                self.Debug("设置群聊精华消息成功！", 0)
                return request
            else:
                self.Debug("设置群聊精华消息失败！", 1)
                self.Debug(request['msg'], 1)

        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)

    def getGroupConfig(self, target: str):
        # 获取群设置
        """
        获取群聊设置
        :param target: 目标群聊
        :return:{'name': 'XXXX', 'confessTalk': XXXX, 'allowMemberInvite': XXXX, 'autoApprove': XXXX, 'anonymousChat': XXXX}
        """
        headers = {
            'Connection': 'close'
        }
        params = {
            "sessionKey": self.session,
            "target": target
        }
        request = requests.get(url=self.host + ":" + self.port + "/groupConfig", headers=headers, params=params)
        print(request.text)
        if request.status_code == 200:
            request = json.loads(request.text)
            if 'code' not in request:
                self.Debug(request, 5)
                self.Debug("获取群聊配置成功！", 0)
                return request
            else:
                self.Debug("获取群聊设置失败！", 1)
                self.Debug(request['msg'], 1)

        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)

    def editGroupConfig(self, target: str, name: str = "", announcement: str = "", confessTalk: bool = None,
                        allowMemberInvit: bool = None, autoApprove: bool = None, anonymousChat: bool = None):
        # 修改群设置(需要相关管理权限)
        """
        修改群聊设置
        :param target: 目标群聊
        :param name: 群名称(可选)
        :param announcement:群公告(可选)
        :param confessTalk:是否开启坦白说(可选)
        :param allowMemberInvit:是否允许群员邀请(可选)
        :param autoApprove:是否开启自动审批入群(可选)
        :param anonymousChat:是否允许匿名聊天(可选)
        :return:{"code":0,"msg":"success}
        """
        headers = {
            'Connection': 'close'
        }
        config: dict = {}
        print(len(name))
        if len(name) > 0:
            config["name"] = name
        if len(announcement) > 0:
            config["announcement"] = announcement
        if confessTalk is not None:
            config["confessTalk"] = confessTalk
        if allowMemberInvit is not None:
            config["allowMemberInvit"] = allowMemberInvit
        if autoApprove is not None:
            config["autoApprove"] = autoApprove
        if anonymousChat is not None:
            config["anonymousChat"] = anonymousChat
        data = '{"sessionKey":"' + self.session + '","target":' + target + ',"config":' + str(config) + '}'
        request = requests.post(url=self.host + ":" + self.port + "/groupConfig", headers=headers,
                                data=data.encode("utf-8"))
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                self.Debug(request, 5)
                self.Debug("修改群聊设置成功！", 0)
                return request
            else:
                self.Debug("设置群聊设置失败！", 1)
                self.Debug(request['msg'], 1)
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)

    def getMemberInfo(self, target: str, memberId: str):
        # 获取群员设置
        """
        获取群员设置
        :param target: 目标群聊
        :param memberId: 目标群员
        :return: 根据实际情况决定
        """
        headers = {
            'Connection': 'close'
        }
        params = {
            "sessionKey": self.session,
            "target": target,
            "memberId": memberId,
        }
        request = requests.get(url=self.host + ":" + self.port + "/memberInfo", headers=headers, params=params)
        print(request.text)
        if request.status_code == 200:
            request = json.loads(request.text)
            if 'code' not in request:
                self.Debug(request, 5)
                self.Debug("获取群员配置成功！", 0)
                return request
            else:
                self.Debug("获取群员设置失败！", 1)
                self.Debug(request['msg'], 1)

        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)

    def editMemberInfo(self, target: str, memberId: str, name: str, specialTitle: str):
        # 修改群成员设置
        """
        修改群成员设置
        :param target: 目标群聊
        :param memberId: 目标成员
        :param name: 目标成员新的名称(可选)
        :param specialTitle: 目标成员新的群头衔(可选)
        :return: {"code":0,"msg":"success"}
        """
        headers = {
            'Connection': 'close'
        }
        config: dict = {}
        print(len(name))
        if len(name) > 0:
            config["name"] = name
        if len(specialTitle) > 0:
            config["specialTitle"] = specialTitle
        data = '{"sessionKey": "' + self.session + '","target": "' + target + '","memberId": "' + memberId + '","info": {' + str(
            config) + '}}'
        request = requests.post(url=self.host + ":" + self.port + "/groupConfig", headers=headers,
                                data=data.encode("utf-8"))
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                self.Debug(request, 5)
                self.Debug("修改群聊设置成功！", 0)
                return request
            else:
                self.Debug("设置群聊设置失败！", 1)
                self.Debug(request['msg'], 1)
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)

    def editAdmin(self, target: str, memberId: str, assign: bool):
        # 修改群管理员设置(群主权限)
        """
        修改群管理员设置(群主权限)
        :param target: 目标群聊
        :param memberId: 目标群成员
        :param assign: 是否设为管理员
        :return: {"code":0,"msg":"success"}
        """
        headers = {
            'Connection': 'close'
        }

        data = '{"sessionKey": "' + self.session + '","target": "' + target + '","memberId": "' + memberId + '","assign": "' + str(
            assign) + '"}'
        request = requests.post(url=self.host + ":" + self.port + "/memberAdmin", headers=headers,
                                data=data.encode("utf-8"))
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                self.Debug(request, 5)
                self.Debug("修改群管理员设置成功！", 0)
                return request
            else:
                self.Debug("设置群管理员设置失败！", 1)
                self.Debug(request['msg'], 1)
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)
        pass


class other(group):
    # 其他操作类
    def sendNudge(self, sub: str, tar: str, ki: str):
        # 发送戳一戳消息
        """
        发送戳一戳消息
        :param sub:戳一戳的目标, QQ号,可以为BotQQ号
        :param tar:戳一戳接受的目标可以为群号/好友QQ号
        :param ki:发送的对象类型(Friend, Group, Stranger)
        :return: {'code': 0, 'msg': 'success'}
        """
        headers = {
            'Connection': 'close'
        }
        message = '{"sessionKey": "' + self.session + '", "target": "' + tar + '", "subject": "' + sub + '", "kind": "' + ki + '"}'
        request = requests.post(url=self.host + ":" + self.port + "/sendNudge", data=str(message),
                                headers=headers)
        print(request.text)
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                self.Debug(request, 5)
                self.Debug("戳一戳消息发送成功！", 0)
                return request
            else:
                self.Debug("发送戳一戳信息失败！", 1)
                self.Debug(request['msg'], 1)
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)

    def reCall(self, tar: str):
        # 撤回消息
        """
        撤回消息
        :param tar: 消息ID，即发送消息后返回的messageId
        :return: {'code': 0, 'msg': 'success'}
        """
        headers = {
            'Connection': 'close'
        }
        message = '{"sessionKey": "' + self.session + '", "target": "' + tar + '"}'
        request = requests.post(url=self.host + ":" + self.port + "/recall", data=str(message),
                                headers=headers)
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                self.Debug(request, 5)
                self.Debug("消息撤回成功！", 0)
                return request
            else:
                self.Debug("信息撤回失败！", 1)
                self.Debug(request['msg'], 1)
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)


class file(other):
    # 文件操作类
    def uploadImage(self, types: str, files: str):
        # 上传图片文件
        """
        上传图片文件
        :param types: 上传后发送的目标
        :param files: 文件地址（实例化Mirai的地址）
        :return:
        """
        headers = {
            'Connection': 'close'
        }
        message = {"sessionKey": self.session, "type": types}
        onfiles = {'img': ('send.png', open(files, 'rb'), 'image/png', {})}
        request = requests.request(method="POST",
                                   url=self.host + ":" + self.port + "/uploadImage", data=message,
                                   headers=headers, files=onfiles)
        if request.status_code == 200:
            request = json.loads(request.text)
            self.Debug(request, 5)
            if 'code' in request:
                self.Debug("图片上传失败！", 0)
                return request["msg"]
            else:
                self.Debug("图片上传成功！", 0)
                return request
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)

    def uploadVoice(self, files: str):
        # 上传音频文件(暂无法使用ing)
        """
        上传音频文件（当前仅支持上传群语音文件）
        :param files:
        :return:
        """
        message = {"sessionKey": self.session, "type": "group"}
        # onFiles = {'voice': (files.split('/')[len(str(files).split('/')) - 1], open(files, 'rb'),f"voice/{files.split('.')[len(str(files).split('.')) - 1]}", {})}
        onFiles = {'voice': ('send.silk', open(files, "rb"))}
        print(onFiles)
        request = requests.request(method="POST",
                                   url=self.host + ":" + self.port + "/uploadVoice", data=message, files=onFiles)
        if request.status_code == 200:
            request = json.loads(request.text)
            self.Debug(request, 5)
            if 'code' in request:
                self.Debug("语音上传失败！", 0)
                return request["msg"]
            else:
                self.Debug("语音上传成功！", 0)
            return request
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)

    def uploadFile(self, target: str, files: str, path: str = ""):
        # 上传文件类(目前仅支持上传群文件)
        headers = {
            'Connection': 'close'
        }
        message = {"sessionKey": self.session, "type": "group", "target": target, "path": path}
        onfiles = {'file': (open(files, 'rb'))}
        request = requests.request(method="POST",
                                   url=self.host + ":" + self.port + "/file/upload", data=message,
                                   headers=headers, files=onfiles)
        print(request.text)
        if request.status_code == 200:
            request = json.loads(request.text)
            self.Debug(request, 5)
            if 'code' in request:
                self.Debug("文件上传失败！", 0)
                return request["msg"]
            else:
                self.Debug("文件上传成功！", 0)
                return request
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)


class Mirai(file):
    # 框架相关操作类
    def version(self) -> dict:
        # 获取插件版本号
        """
        获取mirai-http-api插件版本号
        :return: {'version': 'XX.XX.XX'}
        """
        headers = {
            'Connection': 'close'
        }
        request = requests.get(url=self.host + ":" + self.port + "/about", headers=headers)
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                self.Debug(request, 5)
                self.Debug("插件版本号获取成功！", 0)
                return request["data"]
            else:
                self.Debug("插件版本号获取失败！", 1)
                self.Debug(request['msg'], 1)
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)
