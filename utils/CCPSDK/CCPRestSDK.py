# -*- coding: UTF-8 -*-
#  Copyright (c) 2014 The CCP project authors. All Rights Reserved.
#
#  Use of this source code is governed by a Beijing Speedtong Information Technology Co.,Ltd license
#  that can be found in the LICENSE file in the root of the web site.
#
#   http://www.yuntongxun.com
#
#  An additional intellectual property rights grant can be found
#  in the file PATENTS.  All contributing project authors may
#  be found in the AUTHORS file in the root of the source tree.

from hashlib import md5
import base64
import datetime
# import urllib
import json
from .xmltojson import xmltojson
from urllib import request


class REST:
    AccountSid = ''
    AccountToken = ''
    AppId = ''
    SubAccountSid = ''
    SubAccountToken = ''
    ServerIP = 'app.cloopen.com'
    ServerPort = 8883
    SoftVersion = '2013-12-26'
    Iflog = False  # 是否打印日志
    Batch = ''  # 时间戳
    BodyType = 'json'  # 包体格式，可填值：json 、xml

    # 初始化
    # @param serverIP       必选参数    服务器地址
    # @param serverPort     必选参数    服务器端口
    # @param softVersion    必选参数    REST版本号
    def __init__(self, accoundSid, accountToken, appId):
        self.AccountSid = accoundSid
        self.AccountToken = accountToken
        self.AppId = appId

    # 设置子帐号
    #
    # @param SubAccountSid  必选参数    子帐号
    # @param SubAccountToken  必选参数    子帐号Token

    def setSubAccount(self, SubAccountSid, SubAccountToken):
        self.SubAccountSid = SubAccountSid
        self.SubAccountToken = SubAccountToken

    def log(self, url, body, data=None):
        print('这是请求的URL：')
        print(url)
        print('这是请求包体:')
        print(body)
        print('这是响应包体:')
        print(data)
        print('********************************')

    def sendRequest(self, body, req):
        req.body = body.encode("utf-8")
        try:
            res = request.urlopen(req)
            data = res.read()
            res.close()
            if self.BodyType == 'json':
                # json格式
                locations = json.loads(data)
            else:
                # xml格式
                xtj = xmltojson()
                locations = xtj.main(data)
            return locations
        except Exception as error:
            if self.Iflog:
                print(error)
            return {'172001': '网络错误'}

    # 创建子账号
    # @param friendlyName   必选参数      子帐号名称
    def CreateSubAccount(self, friendlyName):

        self.accAuth()
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")
        # 生成sig
        signature = self.AccountSid + self.AccountToken + self.Batch
        sig = md5.new(signature).hexdigest().upper()
        # 拼接URL
        url = "https://" + self.ServerIP + ":" + str(
            self.ServerPort) + "/" + self.SoftVersion + "/Accounts/" + self.AccountSid + "/SubAccounts?sig=" + sig
        # 生成auth
        src = self.AccountSid + ":" + self.Batch
        auth = base64.encodebytes(src.encode("utf-8")).strip()
        req = request.Request(url)
        self.setHttpHeader(req)
        req.add_header("Authorization", auth)
        # xml格式
        body = '''<?xml version="1.0" encoding="utf-8"?><SubAccount><appId>%s</appId>\
            <friendlyName>%s</friendlyName>\
            </SubAccount>\
            ''' % (self.AppId, friendlyName)

        if self.BodyType == 'json':
            # json格式
            body = '''{"friendlyName": "%s", "appId": "%s"}''' % (friendlyName, self.AppId)
        # 发送请求
        return self.sendRequest(body, req)

    #  获取子帐号
    # @param startNo  可选参数    开始的序号，默认从0开始
    # @param offset 可选参数     一次查询的最大条数，最小是1条，最大是100条
    def getSubAccounts(self, startNo, offset):

        self.accAuth()
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")
        # 生成sig
        signature = self.AccountSid + self.AccountToken + self.Batch
        sig = md5.new(signature).hexdigest().upper()
        # 拼接URL
        url = "https://" + self.ServerIP + ":" + str(
            self.ServerPort) + "/" + self.SoftVersion + "/Accounts/" + self.AccountSid + "/GetSubAccounts?sig=" + sig
        # 生成auth
        src = self.AccountSid + ":" + self.Batch
        auth = base64.encodebytes(src.encode("utf-8")).strip()
        req = request.Request(url)
        self.setHttpHeader(req)
        req.add_header("Authorization", auth)
        # xml格式
        body = '''<?xml version="1.0" encoding="utf-8"?><SubAccount><appId>%s</appId>\
            <startNo>%s</startNo><offset>%s</offset>\
            </SubAccount>\
            ''' % (self.AppId, startNo, offset)

        if self.BodyType == 'json':
            # json格式
            body = '''{"appId": "%s", "startNo": "%s", "offset": "%s"}''' % (self.AppId, startNo, offset)
        # 发送请求
        return self.sendRequest(body, req)

    # 子帐号信息查询
    # @param friendlyName 必选参数   子帐号名称

    def querySubAccount(self, friendlyName):

        self.accAuth()
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")
        # 生成sig
        signature = self.AccountSid + self.AccountToken + self.Batch
        sig = md5.new(signature).hexdigest().upper()
        # 拼接URL
        url = "https://" + self.ServerIP + ":" + str(
            self.ServerPort) + "/" + self.SoftVersion + "/Accounts/" + self.AccountSid + "/QuerySubAccountByName?sig=" + sig
        # 生成auth
        src = self.AccountSid + ":" + self.Batch
        auth = base64.encodebytes(src.encode("utf-8")).strip()
        req = request.Request(url)
        self.setHttpHeader(req)

        req.add_header("Authorization", auth)

        # 创建包体
        body = '''<?xml version="1.0" encoding="utf-8"?><SubAccount><appId>%s</appId>\
            <friendlyName>%s</friendlyName>\
            </SubAccount>\
            ''' % (self.AppId, friendlyName)
        if self.BodyType == 'json':
            body = '''{"friendlyName": "%s", "appId": "%s"}''' % (friendlyName, self.AppId)
        # 发送请求
        return self.sendRequest(body, req)

    # 发送模板短信
    # @param to  必选参数     短信接收彿手机号码集合,用英文逗号分开
    # @param datas 可选参数    内容数据
    # @param tempId 必选参数    模板Id
    def sendTemplateSMS(self, to, datas, tempId):
        self.accAuth()
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")

        # 生成sig
        signature = self.AccountSid + self.AccountToken + self.Batch
        sig = md5(signature.encode('utf-8')).hexdigest().upper()
        # 拼接URL
        url = "https://" + self.ServerIP + ":" + "%s" % self.ServerPort + "/" + self.SoftVersion + "/Accounts/" + self.AccountSid + "/SMS/TemplateSMS?sig=" + sig
        # 生成auth
        src = self.AccountSid + ":" + self.Batch
        auth = base64.encodebytes(src.encode()).strip()
        req = request.Request(url, method='POST')
        self.setHttpHeader(req)
        req.add_header("Authorization", auth)
        # 创建包体
        b = ''
        for a in datas:
            b += '<data>%s</data>' % (a)

        body = '<?xml version="1.0" encoding="utf-8"?><TemplateSMS><datas>' + b + '</datas><to>%s</to><templateId>%s</templateId><appId>%s</appId>\
            </TemplateSMS>\
            ' % (to, tempId, self.AppId)
        if self.BodyType == 'json':
            # if this model is Json ..then do next code
            # caution 下面的方式会在列表最后一个元素后面加个逗号["xxx","111",],导致解析错误
            # b = '['
            # for a in datas:
            #     b += '"%s",' % (a)
            # b += ']'

            body = '''{"to": "%s", "datas": %s, "templateId": "%s", "appId": "%s"}''' % (
            to, datas, tempId, self.AppId)  # 原来的datas是b,这里 换了
        req.data = body.encode('utf-8')
        data = ''
        try:
            res = request.urlopen(req)  # caution  请求不到数据,参数解析错误,
            data = res.read()
            res.close()

            if self.BodyType == 'json':
                # json格式
                locations = json.loads(data)
            else:
                # xml格式
                xtj = xmltojson()
                locations = xtj.main(data)
            if self.Iflog:
                self.log(url, body, data)
            return locations
        except Exception as error:
            print(error)
            if self.Iflog:
                self.log(url, body, data)
            return {'172001': '网络错误'}

    # 外呼通知
    # @param to 必选参数    被叫号码
    # @param mediaName 可选参数    语音文件名称，格式 wav。与mediaTxt不能同时为空。当不为空时mediaTxt属性失效。
    # @param mediaTxt 可选参数    文本内容
    # @param displayNum 可选参数    显示的主叫号码
    # @param playTimes 可选参数    循环播放次数，1－3次，默认播放1次。
    # @param respUrl 可选参数    外呼通知状态通知回调地址，云通讯平台将向该Url地址发送呼叫结果通知。
    # @param userData 可选参数    用户私有数据
    # @param maxCallTime 可选参数    最大通话时长
    # @param speed 可选参数    发音速度
    # @param volume 可选参数    音量
    # @param pitch 可选参数    音调
    # @param bgsound 可选参数    背景音编号

    def landingCall(self, to, mediaName, mediaTxt, displayNum, playTimes, respUrl, userData, maxCallTime, speed, volume,
                    pitch, bgsound):

        self.accAuth()
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")
        # 生成sig
        signature = self.AccountSid + self.AccountToken + self.Batch
        sig = md5.new(signature).hexdigest().upper()
        # 拼接URL
        url = "https://" + self.ServerIP + ":" + str(
            self.ServerPort) + "/" + self.SoftVersion + "/Accounts/" + self.AccountSid + "/Calls/LandingCalls?sig=" + sig
        # 生成auth
        src = self.AccountSid + ":" + self.Batch
        auth = base64.encodebytes(src.encode("utf-8")).strip()
        req = request.Request(url)
        self.setHttpHeader(req)
        req.add_header("Authorization", auth)

        # 创建包体
        body = '''<?xml version="1.0" encoding="utf-8"?><LandingCall>\
            <to>%s</to><mediaName>%s</mediaName><mediaTxt>%s</mediaTxt><appId>%s</appId><displayNum>%s</displayNum>\
            <playTimes>%s</playTimes><respUrl>%s</respUrl><userData>%s</userData><maxCallTime>%s</maxCallTime><speed>%s</speed>
            <volume>%s</volume><pitch>%s</pitch><bgsound>%s</bgsound></LandingCall>\
            ''' % (
        to, mediaName, mediaTxt, self.AppId, displayNum, playTimes, respUrl, userData, maxCallTime, speed, volume,
        pitch, bgsound)
        if self.BodyType == 'json':
            body = '''{"to": "%s", "mediaName": "%s","mediaTxt": "%s","appId": "%s","displayNum": "%s","playTimes": "%s","respUrl": "%s","userData": "%s","maxCallTime": "%s","speed": "%s","volume": "%s","pitch": "%s","bgsound": "%s"}''' % (
            to, mediaName, mediaTxt, self.AppId, displayNum, playTimes, respUrl, userData, maxCallTime, speed, volume,
            pitch, bgsound)
        # 发送请求
        return self.sendRequest(body, req)

    # 语音验证码
    # @param verifyCode  必选参数   验证码内容，为数字和英文字母，不区分大小写，长度4-8位
    # @param playTimes  可选参数   播放次数，1－3次
    # @param to 必选参数    接收号码
    # @param displayNum 可选参数    显示的主叫号码
    # @param respUrl 可选参数    语音验证码状态通知回调地址，云通讯平台将向该Url地址发送呼叫结果通知
    # @param lang 可选参数    语言类型
    # @param userData 可选参数    第三方私有数据

    def voiceVerify(self, verifyCode, playTimes, to, displayNum, respUrl, lang, userData):

        self.accAuth()
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")
        # 生成sig
        signature = self.AccountSid + self.AccountToken + self.Batch
        sig = md5.new(signature).hexdigest().upper()
        # 拼接URL
        url = "https://" + self.ServerIP + ":" + str(
            self.ServerPort) + "/" + self.SoftVersion + "/Accounts/" + self.AccountSid + "/Calls/VoiceVerify?sig=" + sig
        # 生成auth
        src = self.AccountSid + ":" + self.Batch
        auth = base64.encodebytes(src.encode("utf-8")).strip()
        req = request.Request(url)
        self.setHttpHeader(req)

        req.add_header("Authorization", auth)

        # 创建包体
        body = '''<?xml version="1.0" encoding="utf-8"?><VoiceVerify>\
            <appId>%s</appId><verifyCode>%s</verifyCode><playTimes>%s</playTimes><to>%s</to><respUrl>%s</respUrl>\
            <displayNum>%s</displayNum><lang>%s</lang><userData>%s</userData></VoiceVerify>\
            ''' % (self.AppId, verifyCode, playTimes, to, respUrl, displayNum, lang, userData)
        if self.BodyType == 'json':
            # if this model is Json ..then do next code
            body = '''{"appId": "%s", "verifyCode": "%s","playTimes": "%s","to": "%s","respUrl": "%s","displayNum": "%s","lang": "%s","userData": "%s"}''' % (
            self.AppId, verifyCode, playTimes, to, respUrl, displayNum, lang, userData)
        # 发送请求
        return self.sendRequest(body, req)

    # IVR外呼
    # @param number  必选参数     待呼叫号码，为Dial节点的属性
    # @param userdata 可选参数    用户数据，在<startservice>通知中返回，只允许填写数字字符，为Dial节点的属性
    # @param record   可选参数    是否录音，可填项为true和false，默认值为false不录音，为Dial节点的属性

    def ivrDial(self, number, userdata, record):

        self.accAuth()
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")
        # 生成sig
        signature = self.AccountSid + self.AccountToken + self.Batch
        sig = md5.new(signature).hexdigest().upper()
        # 拼接URL
        url = "https://" + self.ServerIP + ":" + str(
            self.ServerPort) + "/" + self.SoftVersion + "/Accounts/" + self.AccountSid + "/ivr/dial?sig=" + sig
        # 生成auth
        src = self.AccountSid + ":" + self.Batch
        auth = base64.encodebytes(src.encode("utf-8")).strip()
        req = request.Request(url)
        req.add_header("Accept", "application/xml")
        req.add_header("Content-Type", "application/xmlcharset=utf-8")
        req.add_header("Authorization", auth)

        # 创建包体
        body = '''<?xml version="1.0" encoding="utf-8"?>
                <Request>
                    <Appid>%s</Appid>
                    <Dial number="%s"  userdata="%s" record="%s"></Dial>
                </Request>
            ''' % (self.AppId, number, userdata, record)
        # 发送请求
        return self.sendRequest(body, req)

    # 话单下载
    # @param date   必选参数    day 代表前一天的数据（从00:00 – 23:59），目前只支持按天查询
    # @param keywords  可选参数     客户的查询条件，由客户自行定义并提供给云通讯平台。默认不填忽略此参数
    def billRecords(self, date, keywords):

        self.accAuth()
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")
        # 生成sig
        signature = self.AccountSid + self.AccountToken + self.Batch
        sig = md5.new(signature).hexdigest().upper()
        # 拼接URL
        url = "https://" + self.ServerIP + ":" + str(
            self.ServerPort) + "/" + self.SoftVersion + "/Accounts/" + self.AccountSid + "/BillRecords?sig=" + sig
        # 生成auth
        src = self.AccountSid + ":" + self.Batch
        auth = base64.encodebytes(src.encode("utf-8")).strip()
        req = request.Request(url)
        self.setHttpHeader(req)
        req.add_header("Authorization", auth)

        # 创建包体
        body = '''<?xml version="1.0" encoding="utf-8"?><BillRecords>\
            <appId>%s</appId><date>%s</date><keywords>%s</keywords>\
            </BillRecords>\
            ''' % (self.AppId, date, keywords)
        if self.BodyType == 'json':
            # if this model is Json ..then do next code
            body = '''{"appId": "%s", "date": "%s","keywords": "%s"}''' % (self.AppId, date, keywords)
        # 发送请求
        return self.sendRequest(body, req)

    # 主帐号信息查询

    def queryAccountInfo(self):

        self.accAuth()
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")
        # 生成sig
        signature = self.AccountSid + self.AccountToken + self.Batch
        sig = md5.new(signature).hexdigest().upper()
        # 拼接URL
        url = "https://" + self.ServerIP + ":" + (
            self.ServerPort) + "/" + self.SoftVersion + "/Accounts/" + self.AccountSid + "/AccountInfo?sig=" + sig
        # 生成auth
        src = self.AccountSid + ":" + self.Batch
        auth = base64.encodebytes(src.encode("utf-8")).strip()
        req = request.Request(url)
        self.setHttpHeader(req)
        body = ''
        req.add_header("Authorization", auth)
        # 发送请求
        return self.sendRequest(body, req)

    # 短信模板查询
    # @param templateId  必选参数   模板Id，不带此参数查询全部可用模板

    def QuerySMSTemplate(self, templateId):

        self.accAuth()
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")
        # 生成sig
        signature = self.AccountSid + self.AccountToken + self.Batch
        sig = md5.new(signature).hexdigest().upper()
        # 拼接URL
        url = "https://" + self.ServerIP + ":" + str(
            self.ServerPort) + "/" + self.SoftVersion + "/Accounts/" + self.AccountSid + "/SMS/QuerySMSTemplate?sig=" + sig
        # 生成auth
        src = self.AccountSid + ":" + self.Batch
        auth = base64.encodebytes(src.encode("utf-8")).strip()
        req = request.Request(url)
        self.setHttpHeader(req)

        req.add_header("Authorization", auth)

        # 创建包体
        body = '''<?xml version="1.0" encoding="utf-8"?><Request>\
            <appId>%s</appId><templateId>%s</templateId></Request>
            ''' % (self.AppId, templateId)
        if self.BodyType == 'json':
            # if this model is Json ..then do next code
            body = '''{"appId": "%s", "templateId": "%s"}''' % (self.AppId, templateId)
        # 发送请求
        return self.sendRequest(body, req)

    # 呼叫结果查询
    # @param callsid   必选参数    呼叫ID

    def CallResult(self, callSid):

        self.accAuth()
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")
        # 生成sig
        signature = self.AccountSid + self.AccountToken + self.Batch
        sig = md5.new(signature).hexdigest().upper()
        # 拼接URL
        url = "https://" + self.ServerIP + ":" + str(
            self.ServerPort) + "/" + self.SoftVersion + "/Accounts/" + self.AccountSid + "/CallResult?sig=" + sig + "&callsid=" + callSid
        # 生成auth
        src = self.AccountSid + ":" + self.Batch
        auth = base64.encodebytes(src.encode("utf-8")).strip()
        req = request.Request(url)
        self.setHttpHeader(req)
        body = ''
        req.add_header("Authorization", auth)
        # 发送请求
        return self.sendRequest(body, req)

    # 呼叫状态查询
    # @param callid   必选参数    一个由32个字符组成的电话唯一标识符
    # @param action      可选参数     查询结果通知的回调url地址
    def QueryCallState(self, callid, action):

        self.accAuth()
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")
        # 生成sig
        signature = self.AccountSid + self.AccountToken + self.Batch
        sig = md5.new(signature).hexdigest().upper()
        # 拼接URL
        url = "https://" + self.ServerIP + ":" + str(
            self.ServerPort) + "/" + self.SoftVersion + "/Accounts/" + self.AccountSid + "/ivr/call?sig=" + sig + "&callid=" + callid
        # 生成auth
        src = self.AccountSid + ":" + self.Batch
        auth = base64.encodebytes(src.encode("utf-8")).strip()
        req = request.Request(url)
        self.setHttpHeader(req)
        req.add_header("Authorization", auth)

        # 创建包体
        body = '''<?xml version="1.0" encoding="utf-8"?><Request>\
            <Appid>%s</Appid><QueryCallState callid="%s" action="%s"/>\
            </Request>\
            ''' % (self.AppId, callid, action)
        if self.BodyType == 'json':
            # if this model is Json ..then do next code
            body = '''{"Appid":"%s","QueryCallState":{"callid":"%s","action":"%s"}}''' % (self.AppId, callid, action)
        # 发送请求
        return self.sendRequest(body, req)

    # 语音文件上传
    # @param filename   必选参数    文件名
    # @param body      必选参数     二进制串
    def MediaFileUpload(self, filename, body):

        self.accAuth()
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")
        # 生成sig
        signature = self.AccountSid + self.AccountToken + self.Batch
        sig = md5.new(signature).hexdigest().upper()
        # 拼接URL
        url = "https://" + self.ServerIP + ":" + str(
            self.ServerPort) + "/" + self.SoftVersion + "/Accounts/" + self.AccountSid + "/Calls/MediaFileUpload?sig=" + sig + "&appid=" + self.AppId + "&filename=" + filename
        # 生成auth
        src = self.AccountSid + ":" + self.Batch
        auth = base64.encodebytes(src.encode("utf-8")).strip()
        req = request.Request(url)
        req.add_header("Authorization", auth)
        if self.BodyType == 'json':
            req.add_header("Accept", "application/json")
            req.add_header("Content-Type", "application/octet-stream")

        else:
            req.add_header("Accept", "application/xml")
            req.add_header("Content-Type", "application/octet-stream")
        # 发送请求
        return self.sendRequest(body, req)

    # 子帐号鉴权
    def subAuth(self):
        if (self.ServerIP == ""):
            print('172004')
            print('IP为空')

        if (self.ServerPort <= 0):
            print('172005')
            print('端口错误（小于等于0）')

        if (self.SoftVersion == ""):
            print('172013')
            print('版本号为空')

        if (self.SubAccountSid == ""):
            print('172008')
            print('子帐号为空')

        if (self.SubAccountToken == ""):
            print('172009')
            print('子帐号令牌为空')

        if (self.AppId == ""):
            print('172012')
            print('应用ID为空')

    # 主帐号鉴权
    def accAuth(self):
        if (self.ServerIP == ""):
            print('172004')
            print('IP为空')

        if (self.ServerPort <= 0):
            print('172005')
            print('端口错误（小于等于0）')

        if (self.SoftVersion == ""):
            print('172013')
            print('版本号为空')

        if (self.AccountSid == ""):
            print('172006')
            print('主帐号为空')

        if (self.AccountToken == ""):
            print('172007')
            print('主帐号令牌为空')

        if (self.AppId == ""):
            print('172012')
            print('应用ID为空')

    # 设置包头
    def setHttpHeader(self, req):
        if self.BodyType == 'json':
            req.add_header("Accept", "application/json")
            req.add_header("Content-Type", "application/jsoncharset=utf-8")

        else:
            req.add_header("Accept", "application/xml")
            req.add_header("Content-Type", "application/xmlcharset=utf-8")
