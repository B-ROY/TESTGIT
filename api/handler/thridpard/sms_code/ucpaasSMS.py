# -*- coding: UTF-8 -*-
#
# 具体定义和参数说明参考 云之讯REST开发者文档 .docx
#
import base64
import datetime
import urllib2
import md5
import random
# import Foundation
import json
import hmac
import hashlib
import pylibmc
from django.conf import settings
import time

memcache_settings = settings.memcache_settings


# 返回签名
def getSig(accountSid, accountToken, timestamp):
    sig = accountSid + accountToken + timestamp
    return md5.new(sig).hexdigest().upper()


# 生成授权信息
def getAuth(accountSid, timestamp):
    src = accountSid + ":" + timestamp
    return base64.encodestring(src).strip()


# 发起http请求
def urlOpen(req, data=None):
    try:
        res = urllib2.urlopen(req, data)
        data = res.read()
        print "data is " + data
        res.close()
    except urllib2.HTTPError, error:
        print error
        data = error.read()
        error.close()

    return data


# 生成HTTP报文
def createHttpReq(req, url, accountSid, timestamp, responseMode, body):
    req.add_header("Authorization", getAuth(accountSid, timestamp))
    if responseMode:
        req.add_header("Accept", "application/" + responseMode)
        req.add_header("Content-Type", "application/" + responseMode + ";charset=utf-8")
    if body:
        req.add_header("Content-Length", len(body))
        req.add_data(body)
    return req


class UcpaasSMS:
    __HOST = "https://api.ucpaas.com"
    # PORT = ""
    __SOFTVER = "2014-06-30"
    __JSON = "json"
    __XML = "xml"
    # __accountSid = "531f90c720ded0cc60dd50f44f8e79cd"ta
    __accountSid = "531f90c720ded0cc60dd50f44f8e79cd"
    # __accountToken = "cb6ad643943e90beaaf564b7ee517965"
    __accountToken = "cb6ad643943e90beaaf564b7ee517965"
    # __appId = "75136b111d8e4af49666980e6746cdf4"
    # __appId = "a3589fbbd6cf40d99c6e928ea52e734a" # 爱哇啦
    __appId = "a8fb74d843a546b79dc3d0e1b578bc2b"  # 聊啪
    __CODE = ""

    # smscode_cache = None

    # def __init__(self):

    # 短信验证码（模板短信）
    # accountSid 主账号ID
    # accountToken 主账号Token
    # appId 应用ID
    # toNumber 被叫的号码
    # templateId 模板Id
    # param <可选> 内容数据，用于替换模板中{数字,数字}，多个参数用逗号分隔
    def __templateSMS(self, toNumbers, templateId, param, isUseJson=True):
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        signature = getSig(self.__accountSid, self.__accountToken, timestamp)
        # url = self.HOST + ":" + self.PORT + "/" + self.SOFTVER + "/Accounts/" + accountSid + "/Messages/templateSMS?sig=" + signature
        url = self.__HOST + "/" + self.__SOFTVER + "/Accounts/" + self.__accountSid + "/Messages/templateSMS?sig=" + signature

        if isUseJson == True:
            body = '{"templateSMS":{ "appId":"%s","to":"%s","templateId":"%s","param":"%s"}}' % (
            self.__appId, toNumbers, templateId, param)
            responseMode = self.__JSON
        else:
            body = "<?xml version='1.0' encoding='utf-8'?>\
					<templateSMS>\
						<appId>%s</appId>\
						<to>%s</to>\
						<templateId>%s</templateId>\
						<param>%s</param>\
					</templateSMS>\
					" % (__appId, toNumbers, templateId, param)
            responseMode = self.__XML
        req = urllib2.Request(url)
        return urlOpen(createHttpReq(req, url, self.__accountSid, timestamp, responseMode, body))

    def __voiceSMS(self, toNumbers, sms_code):
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        signature = getSig(self.__accountSid, self.__accountToken, timestamp)
        # url = self.HOST + ":" + self.PORT + "/" + self.SOFTVER + "/Accounts/" + accountSid + "/Messages/templateSMS?sig=" + signature
        url = self.__HOST + "/" + self.__SOFTVER + "/Accounts/" + self.__accountSid + "/Calls/voiceVerify?sig=" + signature


        body = '{"voiceVerify":{ "appId":"%s","to":"%s","captchaCode":"%s","playTimes":"%s","displayNum":"12590"}}' % (
            self.__appId, toNumbers, str(sms_code), "2")
        responseMode = self.__JSON
        req = urllib2.Request(url)
        data = urlOpen(createHttpReq(req, url, self.__accountSid, timestamp, responseMode, body))
        return data
    def __genCode(self):
        codelen = 4
        base = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
        code = ''
        for x in range(codelen):
            ran = random.randint(0, 9)
            code = ''.join((code, base[ran]))
        return code

    def get_access_token(self, phoneNumber, openId, create_time=None):

        if create_time == None:
            # expire_time = (datetime.datetime.utcnow() + datetime.timedelta(days =2)).strftime("%Y%m%d%H%S%M")
            create_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        head = '{"Alg":"HS256","Accid":"%s","Cnumber":"%s","Expiretime":"%s"}' % \
               (openId, phoneNumber, create_time)
        # print("head:",head)
        body = '{"AccToken":"%s","Cnumber":"%s","Cpwd":"%s","Expiretime":"%s"}' % \
               (self.__accountToken, phoneNumber, openId, create_time)
        # print("body:",body)

        body_bytes = hmac.new(self.__accountToken.encode('utf-8'), body.encode('utf-8'), hashlib.sha256)
        # print(body_bytes.digest())
        # base64
        body_bytes = base64.b64encode(body_bytes.digest())
        head = base64.b64encode(head.encode('utf-8'))
        # print(head+b"."+body_bytes)
        return head + b"." + body_bytes

    def __analyzing(self, result, phone):
        if len(result) == 2:
            resl = {}
            resl['smsCode'] = result[0]
            data = json.loads(result[1])['resp']
            resl['respCode'] = data['respCode']
            if resl['respCode'] == '000000':
                resl['is_success'] = 1
            else:
                resl["is_success"] = 0
            resl['createDate'] = int(time.time())
            resl['finishDate'] = str(int(resl['createDate']) + 180)
            # resl['openId'] = (data['templateSMS'])['smsId']
            resl['openId'] = base64.b64encode(phone)
            resl['user_key'] = self.get_access_token(phone, resl['openId'], resl['createDate'])
            resl['phone'] = phone
            return resl

    def delSmsCodeCache(self, toTelNumber):
        smscode_cache = pylibmc.Client(memcache_settings["user_cache"], binary=True,
                                       behaviors={"tcp_nodelay": True, "ketama": True})

        smscode_cache.delete(str(toTelNumber))
        smscode_cache.disconnect_all()

    def getCacheData(self, toTelNumber):
        smscode_cache = pylibmc.Client(memcache_settings["user_cache"], binary=True,
                                       behaviors={"tcp_nodelay": True, "ketama": True})

        regCache = {}
        regCache = smscode_cache.get(toTelNumber)
        print smscode_cache
        print "getCacheData"
        print regCache
        if regCache is None:
            return None
        # curr_time = datetime.datetime.utcnow().strftime("%Y%m%d%H%S%M")
        curr_time = int(time.time())
        # 说明验证码失效
        if (int(regCache['finishDate']) - int(curr_time)) < 0:
            self.delSmsCodeCache(toTelNumber)
            return None
        smscode_cache.disconnect_all()
        return regCache

    def sendRegiesterCode(self, toTelNumber, method=0,sms_type=0):
        smscode_cache = pylibmc.Client(memcache_settings["user_cache"], binary=True,
                                       behaviors={"tcp_nodelay": True, "ketama": True})

        result = self.getCacheData(toTelNumber)
        if result == None:
            self.__CODE = self.__genCode()
            # TODO 这里是为了苹果测试
            if toTelNumber == "13811768998" or toTelNumber == "13552475673" or toTelNumber == "18600023711":
                self.__CODE = "1234"
            # TODO: for hacker
            if toTelNumber == "15655513846":
                return
            param = self.__CODE + ",1"
            # templateId="25690"
            if method == 0:
                # templateId="31623"
                templateId = "36072"
            elif method == 1 or method == 2:
                # templateId="35411"
                templateId = "36073"
            elif method == 3:
                # templateId="35412"
                templateId = "36075"
            elif method == 4:
                # templateId="35711"
                templateId = "36074"
            reg = []
            reg.append(self.__CODE)
            if sms_type == 0:
                reg.append(self.__templateSMS(toTelNumber, templateId, param))
            else:
                respones = self.__voiceSMS(toTelNumber, self.__CODE)
                reg.append(respones)
            reult = self.__analyzing(reg, toTelNumber)
            print reult
            smscode_cache.add(toTelNumber, reult)
            return reult
        smscode_cache.disconnect_all()
        return result

    def sendForgetPassCode(self, toTelNumber):
        self.__CODE = self.__genCode()
        param = self.__CODE + ",1"
        # templateId="25690"
        templateId = "31623"
        reg = []
        reg.append(self.__CODE)
        reg.append(self.__templateSMS(toTelNumber, templateId, param))
        return self.__analyzing(reg)


def main():
    test = UcpaasSMS()
    resl = test.sendRegiesterCode("18600023711")
    print resl
    if resl['respCode'] != '000000':
        print "ssss"
        return "fail"
    if isinstance(resl, dict):
        for r in resl.iteritems():
            print r
    test1 = UcpaasSMS()
    data = {'openId': u'9485d24ab5a3f51fa392805c14b268bc', 'smsCode': 'FJNG', 'respCode': u'000000',
            'user_key': 'eyJBbGciOiJIUzI1NiIsIkFjY2lkIjoiOTQ4NWQyNGFiNWEzZjUxZmEzOTI4MDVjMTRiMjY4YmMiLCJDbnVtYmVyIjoiMTg2MDAwMjM3MTEiLCJFeHBpcmV0aW1lIjoiMjAxNjA3MDIxMTU5NDYifQ==.PGRZcKQtwMpwKHtRjYASUCNqb79tnYUJiirM5YCQw/k=',
            'createDate': u'20160702115946', 'phone': '18600023711', 'finishDate': '20160702116126'}
    curr_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    # 说明验证码失效
    print "curr_time" + curr_time
    print "time:" + str(int(data['finishDate']) - int(curr_time))

    token = test1.get_access_token("18600023711", resl['openId'], resl['createDate'])
    if resl['user_key'] != token:
        raise Exception("error")
    print "ok"
    print 1


"""
{'createDate': u'20160701210746', 'smsCode': 'NW0D', 'endDate': 20160701210866, 'respCode': u'000000', 'smsId': u'9a5b0d270127ffb8b27a4a9fb0ef4b56'}
"""

if __name__ == "__main__":
    main()
