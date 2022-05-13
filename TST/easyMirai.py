import sys
import time
import requests
import json


class Init:
    # 初始化所有参数类
    def __init__(self, host: str, port: str, key: str, qid: str, count: str = 1, debug: bool = False, times: int = 1):
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


class Setup(Init):
    # 初始化类

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

    def Release(self):
        # 释放session
        pass
        self.Debug("正在注销Session", 1)


class Message(Setup):
    """
    getCountMessage:获取信息列长度，即信息总条数

    getFetchMessage:获取队列头部消息后移除即按时间顺序获取消息

    getFetchLatestMessage:获取队列尾部消息后移除即获取最新消息

    getPeekMessage:获取队列头部消息后不移除即按时间顺序获取消息

    getPeekLatestMessage:获取队列尾部消息后不移除即获取最新消息

    sendFriendMessage:发送好友消息

    sendGroupMessage:发送群消息
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

    def getFetchMessage(self) -> str:
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


class formatMessage(Message):
    # 格式化信息类
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


class Mirai(formatMessage):
    def version(self) -> str:
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
                return request
            else:
                self.Debug("插件版本号获取失败！", 1)
                self.Debug(request['msg'], 1)
        else:
            self.Debug("连接请求失败！请检查网络配置！", 2)

    def botProfile(self):
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