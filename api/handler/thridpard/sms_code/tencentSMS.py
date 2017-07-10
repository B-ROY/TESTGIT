#-*- coding: UTF-8 -*-
#
# 具体定义和参数说明参考 云之讯REST开发者文档 .docx
#
import base64
import datetime
import urllib2
import md5
import random
#import Foundation
import json
import hmac
import hashlib
import pylibmc
import time
from redis_model.redis_client import *


# 返回签名
def getSig(accountSid,accountToken,timestamp):
    sig = accountSid + accountToken + timestamp
    return md5.new(sig).hexdigest().upper()


#生成授权信息
def getAuth(accountSid,timestamp):
    src = accountSid + ":" + timestamp
    return base64.encodestring(src).strip()


#发起http请求
def urlOpen(req,data=None):
    try:
        res = urllib2.urlopen(req,data)
        data = res.read()
        res.close()
    except urllib2.HTTPError, error:
        data = error.read()
        error.close()
    return data


class TencentSMS:

    __HOST = "https://yun.tim.qq.com/v5/tlssmssvr/sendsms?sdkappid=%s&random=%s"

    __HOST__VOICE = "https://yun.tim.qq.com/v5/tlsvoicesvr/sendvoice?sdkappid=%s&random=%s"

    __app_id = 1400028789
    __app_key = '41d0c4112b17dc11a8311a1ec2fd8437'
    __accountToken = "cb6ad643943e90beaaf564b7ee517965"
    __nation_code = "86"

    def __init__(self):
        if settings.INTERNATIONAL_TYPE != 0:
            self.__nation_code = "86"
        pass

    def get_sig(self, random_str, timestamp, mobiles):
        sig_pre = "appkey=%s&random=%s&time=%s&mobile=%s" % (self.__app_key, random_str, timestamp,mobiles)
        sig = hashlib.sha256(sig_pre).hexdigest()
        return sig

    def getAuth(self, accountSid, timestamp):
        src = accountSid + ":" + timestamp
        return base64.encodestring(src).strip()

    def send_SMS(self, telnumber, templates_id, params):
        random_str = str(random.randint(0,1000000))
        timestamp = int(time.time())
        sig = self.get_sig(random_str, timestamp, telnumber)

        url = self.__HOST % (self.__app_id, random_str)

        body={}

        tel_single={}
        tel_single["nationcode"]=self.__nation_code
        tel_single["mobile"] = telnumber

        body["tel"] = tel_single
        body["type"] = 0
        body["tpl_id"] = templates_id
        body["params"] = params
        body["sig"] = sig
        body["time"] = str(timestamp)
        req = urllib2.Request(url, json.dumps(body))
        res_data = urllib2.urlopen(req).read()

        print res_data
        return res_data

    def send_VOICESMS(self, telnumber, code):

        random_str = str(random.randint(0, 1000000))
        timestamp = int(time.time())
        sig = self.get_sig(random_str, timestamp, telnumber)

        url = self.__HOST__VOICE % (self.__app_id, random_str)

        body = {}

        tel_single = {}
        tel_single["nationcode"] = self.__nation_code
        tel_single["mobile"] = telnumber

        body["tel"] = tel_single
        body["msg"] = str(code)
        body["times"] = 3
        body["sig"] = sig
        body["time"] = str(timestamp)
        req = urllib2.Request(url, json.dumps(body))
        res_data = urllib2.urlopen(req).read()

        print res_data
        return res_data

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
        print "result is " + str(result)
        if len(result) == 2:
            resl = {}
            resl['smsCode'] = result[0]
            print result
            data = json.loads(result[1])
            resl['respCode'] = data['result']
            if resl['respCode'] == 0:
                resl["is_success"] = 1
            else:
                resl["is_success"] = 0
            resl['createDate'] = int(time.time())
            resl['finishDate'] = str(resl['createDate'] + 180)
            resl['openId'] = base64.b64encode(phone)
            resl['user_key'] = self.get_access_token(phone, resl['openId'], resl['createDate'])
            resl['phone'] = phone
            return resl

    def delSmsCodeCache(self, toTelNumber):
        RQueueClient.getInstance().redis.delete(str(toTelNumber))


    def getCacheData(self, toTelNumber):
        regCache = RQueueClient.getInstance().redis.get(toTelNumber)

        print "getCacheData"
        print regCache
        if regCache is None:
            return None
        regCache = json.loads(regCache)
        # curr_time = datetime.datetime.utcnow().strftime("%Y%m%d%H%S%M")
        curr_time = int(time.time())

        # 说明验证码失效
        if (int(regCache['finishDate']) - int(curr_time)) < 0:
            self.delSmsCodeCache(toTelNumber)
            return None
        return regCache

    def sendRegiesterCode(self, toTelNumber, method=0, sms_type=0):# 0为文字 1为语音

        self.__CODE = self.__genCode()
        # TODO 这里是为了苹果测试
        if toTelNumber == "13811768998" or toTelNumber == "13552475673" or toTelNumber == "18600023711":
            self.__CODE = "1234"
        # TODO: for hacker
        if toTelNumber == "15655513846":
            return
        param = [self.__CODE, "1"]
        # templateId="25690"
        if method == 0:
            # templateId="31623"
            templateId = 21648
        elif method == 1 or method == 2:
            # templateId="35411"
            templateId = 21647
        elif method == 3:
            # templateId="35412"
            templateId = 21646
        elif method == 4:
            # templateId="35711"
            templateId = 21645
        reg = []
        reg.append(self.__CODE)
        if sms_type == 0:
            reg.append(self.send_SMS(toTelNumber, templateId, param))
        else:
            reg.append(self.send_VOICESMS(toTelNumber, self.__CODE))
        reult = self.__analyzing(reg, toTelNumber)
        print reult
        RQueueClient.getInstance().redis.set(toTelNumber, json.dumps(reult), ex=180)

        return reult

    def sendForgetPassCode(self, toTelNumber):
        self.__CODE = self.__genCode()
        param = [self.__CODE, "1"]
        # templateId="25690"
        templateId = 21647
        reg = []
        reg.append(self.__CODE)
        reg.append(self.send_SMS(toTelNumber, templateId, param))
        return self.__analyzing(reg)



def main():
    test = TencentSMS()
    resl = test.sendRegiesterCode("18600023711")
    print resl
    if resl['respCode'] != '000000':
        print "ssss"
        return "fail"
    if isinstance(resl, dict):
        for r in resl.iteritems():
            print r
    test1 = TencentSMS()
    data={'openId': u'9485d24ab5a3f51fa392805c14b268bc', 'smsCode': 'FJNG', 'respCode': u'000000', 'user_key': 'eyJBbGciOiJIUzI1NiIsIkFjY2lkIjoiOTQ4NWQyNGFiNWEzZjUxZmEzOTI4MDVjMTRiMjY4YmMiLCJDbnVtYmVyIjoiMTg2MDAwMjM3MTEiLCJFeHBpcmV0aW1lIjoiMjAxNjA3MDIxMTU5NDYifQ==.PGRZcKQtwMpwKHtRjYASUCNqb79tnYUJiirM5YCQw/k=', 'createDate': u'20160702115946', 'phone': '18600023711', 'finishDate': '20160702116126'}
    curr_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        #说明验证码失效
    print "curr_time" + curr_time
    print "time:" + str(int(data['finishDate'])-int(curr_time))

    token = test1.get_access_token("18600023711",resl['openId'], resl['createDate'])
    if resl['user_key'] != token:
        raise Exception("error")
    print "ok"
    print 1
"""
{'createDate': u'20160701210746', 'smsCode': 'NW0D', 'endDate': 20160701210866, 'respCode': u'000000', 'smsId': u'9a5b0d270127ffb8b27a4a9fb0ef4b56'}
"""

	
	
if __name__ == "__main__":
	main()
