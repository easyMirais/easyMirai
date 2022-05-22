# -*- coding: utf-8 -*-

"""
author: HexMikuMax & ExMikuPro
data: 2022/05/22
version: Beta 1.1
"""

import json
import sys
import time

import requests


class Init:
    # 初始化参数类
    def __init__(self, host: str, port: str, key: str, qid: str, count: str = "1", debug: bool = False, times: int = 1):
        self.host = host
        self.port = port
        self.key = key
        self.qid = qid
        self.count = count
        self.session = ""
        self.debug: bool = debug
        self.times: int = times

    def Debug(self, msg, code: int):
        # 输出控制台
        # code: 0 成功 1 过程性错误 2 请求性错误 5 返回请求原数据
        if self.debug:
            print(msg, code)


class setup(Init):
    # Bot初始化类

    def begin(self) -> str:
        # 初始化机器人
        self.getSession()
        self.bindSession()
        self.Debug("初始化成功！", 0)
        return "Bot:" + self.qid + " 初始化成功！"

    def getSession(self) -> str:
        # 获取session状态码
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
                sys.exit()
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)
            sys.exit()

    def bindSession(self) -> str:
        # 绑定session到QQ机器人
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
                sys.exit()
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)
            sys.exit()

    def releaseSession(self):
        # 释放session到QQBot
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
                return self.session
            else:
                self.Debug("session注销失败！", 1)
                self.Debug(request['msg'], 1)
                sys.exit()
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)
            sys.exit()


class Message(setup):
    # 信息操作处理类
    """
    getCountMessage:获取信息列长度，即信息总条数

    getFetchMessage:获取队列头部消息后移除即按时间顺序获取消息

    getFetchLatestMessage:获取队列尾部消息后移除即获取最新消息

    getPeekMessage:获取队列头部消息后不移除即按时间顺序获取消息

    getPeekLatestMessage:获取队列尾部消息后不移除即获取最新消息

    """

    def getCountMessage(self):
        # 获取消息列长度
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
            sys.exit()

    def getFetchMessage(self) -> dict:
        # 获取队列头部消息后移除
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
                sys.exit()
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)
            sys.exit()

    def getFetchLatestMessage(self):
        # 获取队列尾部消息后移除
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
                sys.exit()
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)
            sys.exit()

    def getPeekMessage(self):
        # 获取队列头部消息后不移除
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
                sys.exit()
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)
            sys.exit()

    def getPeekLatestMessage(self) -> str:
        # 获取队列尾部消息后不移除
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
                sys.exit()
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)
            sys.exit()


class formatMessage(Message):
    # 信息格式化处理类(实际生产项目不建议使用)
    def getFetchMessageFormat(self):
        message = self.getFetchMessage()
        return self.Format(message)

    def getFetchLatestMessageFormat(self):
        message = self.getFetchLatestMessage()
        return self.Format(message)

    def getPeekMessageFormat(self):
        message = self.getPeekMessage()
        return self.Format(message)

    def getPeekLatestMessageFormat(self):
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
                sys.exit()
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)
            sys.exit()

    def getMemberList(self, target: str):
        # 获取Bot加入群的群成员列表
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
                sys.exit()
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)
            sys.exit()

    def getGroupList(self):
        # 获取Bot加入的群列表
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
                sys.exit()
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)
            sys.exit()

    def botProfile(self):
        # 获取Bot机器人账号信息
        headers = {
            'Connection': 'close'
        }
        request = requests.get(url=self.host + ":" + self.port + "/botProfile", headers=headers)
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                self.Debug(request, 5)
                self.Debug("Bot信息获取成功！", 0)
                return request
            else:
                self.Debug("Bot信息获取失败！", 1)
                self.Debug(request['msg'], 1)
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)

    def delay(self):
        time.sleep(self.times)


class friend(bot):
    # 好友相关操作类
    def sendFriendMessage(self, msg: dict, tar) -> str:
        # 发送好友消息
        headers = {
            'Connection': 'close'
        }
        if len(msg) >= 0:
            massage = json.dumps(msg)
            massage = '{"sessionKey":"' + self.session + '","target":' + tar + ',"messageChain":[' + massage + ']}'
            request = requests.post(url=self.host + ":" + self.port + "/sendFriendMessage", data=str(massage),
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
                    sys.exit()
            else:
                self.Debug("连接请求失败！请检查网络配置！", 2)
                sys.exit()

    def getUserProfile(self, target: str):
        # 获取好友/任意用户信息
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
                sys.exit()
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)
            sys.exit()

    def deleteFriend(self, tar):
        # 删除好友
        headers = {
            'Connection': 'close'
        }
        massage = '{"sessionKey":"' + self.session + '","target":' + tar + '}"'
        request = requests.post(url=self.host + ":" + self.port + "/deleteFriend", data=str(massage),
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
            sys.exit()
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)
            sys.exit()


class group(friend):
    # 群相关操作类
    def sendGroupMessage(self, msg: dict, tar):
        # 发送群消息
        headers = {
            'Connection': 'close'
        }
        if len(msg) >= 0:
            massage = json.dumps(msg)
            massage = '{"sessionKey":"' + self.session + '","target":' + tar + ',"messageChain":[' + massage + ']}'
            request = requests.post(url=self.host + ":" + self.port + "/sendGroupMessage", data=str(massage),
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
                    sys.exit()
            else:
                self.Debug("连接请求失败！请检查网络配置！", 2)
                sys.exit()

    def sendTempMessage(self, msg: dict, tar):
        # 发送群临时消息
        headers = {
            'Connection': 'close'
        }
        if len(msg) >= 0:
            massage = json.dumps(msg)
            massage = '{"sessionKey":"' + self.session + '","target":' + tar + ',"messageChain":[' + massage + ']}'
            request = requests.post(url=self.host + ":" + self.port + "/sendTempMessage", data=str(massage),
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
                    sys.exit()
            else:
                self.Debug("连接请求失败！请检查网络配置！", 2)
                sys.exit()

    def getMemberProfile(self, target: str, memberId: str):
        # 获取群员信息
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
            if request['code'] == 0:
                self.Debug(request, 5)
                self.Debug("群成员资料成功！", 0)
                return request
            else:
                self.Debug("群成员资料失败！", 1)
                self.Debug(request['msg'], 1)
                sys.exit()
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)
            sys.exit()

    def muteMember(self, target: str, memberId: str, times: str):
        # 禁言群成员
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
                sys.exit()
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)
            sys.exit()

    def unMuteMember(self, target: str, memberId: str):
        # 解除群成员禁言
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
                sys.exit()
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)
            sys.exit()

    def kick(self, target: str, memberId: str, msg: str):
        # 移除群成员
        headers = {
            'Connection': 'close'
        }
        me = memberId
        tar = target
        data = '{"sessionKey":"' + self.session + '","target":' + tar + ',"memberId":' + me + ',"msg":' + msg + '}'
        request = requests.post(url=self.host + ":" + self.port + "/kick", headers=headers, data=data)
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                self.Debug(request, 5)
                self.Debug("群成员资料成功！", 0)
                return request
            else:
                self.Debug("群成员资料失败！", 1)
                self.Debug(request['msg'], 1)
                sys.exit()
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)
            sys.exit()

    def quitGroup(self, target: str):
        # 退出指定群聊
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
                sys.exit()
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)
            sys.exit()

    def muteAll(self, target: str):
        # 禁言指定群聊全体成员
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
                self.Debug("退出群聊成功！", 0)
                return request
            else:
                self.Debug("退出群聊失败！", 1)
                self.Debug(request['msg'], 1)
                sys.exit()
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)
            sys.exit()

    def unMuteAll(self, target: str):
        # 解除指定群聊全体成员禁言
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
                self.Debug("退出群聊成功！", 0)
                return request
            else:
                self.Debug("退出群聊失败！", 1)
                self.Debug(request['msg'], 1)
                sys.exit()
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)
            sys.exit()


class other(group):
    # 其他操作类
    def sendNudge(self, sub: str, tar: str, ki: str):
        # 发送戳一戳消息
        headers = {
            'Connection': 'close'
        }
        massage = '{"sessionKey":"' + self.session + '","target":' + tar + ',"subject":' + sub + ',"kind":' + ki + '}"'
        request = requests.post(url=self.host + ":" + self.port + "/sendNudge", data=str(massage),
                                headers=headers)
        if request.status_code == 200:
            request = json.loads(request.text)
            if request['code'] == 0:
                self.Debug(request, 5)
                self.Debug("戳一戳消息发送成功！", 0)
                return request
            else:
                self.Debug("发送戳一戳信息失败！", 1)
                self.Debug(request['msg'], 1)
            sys.exit()
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)
            sys.exit()

    def reCall(self, tar):
        # 撤回消息
        headers = {
            'Connection': 'close'
        }
        massage = '{"sessionKey":"' + self.session + '","target":' + tar + '}"'
        request = requests.post(url=self.host + ":" + self.port + "/reCall", data=str(massage),
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
            sys.exit()
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)
            sys.exit()


class file(other):
    # 文件操作类
    def uploadImage(self, types: str, files: str):
        # 上传图片文件
        headers = {
            'Connection': 'close'
        }
        massage = {"sessionKey": self.session, "type": types}
        onFiles = {'img': ('send.png', open(files, 'rb'), 'image/png', {})}
        request = requests.request(method="POST",
                                   url=self.host + ":" + self.port + "/uploadImage", data=massage,
                                   headers=headers, files=onFiles)
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
            sys.exit()

    def uploadVoice(self, files: str):
        # 上传音频文件(暂无法使用ing)
        massage = {"sessionKey": self.session, "type": "group"}
        onFiles = {'voice': (files.split('/')[len(str(files).split('/')) - 1], open(files, 'rb'),
                             f"voice/{files.split('.')[len(str(files).split('.')) - 1]}", {})}
        request = requests.request(method="POST",
                                   url=self.host + ":" + self.port + "/uploadVoice", data=massage
                                   , files=onFiles)
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
            sys.exit()


class Mirai(file):
    # 框架相关操作类
    def version(self) -> dict:
        # 获取插件版本号
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
