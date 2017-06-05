#coding=utf-8

import hashlib
import time
import random
import urllib
import urllib2
import json

"""
生成网易云易盾接口请求签名
"""
class YIDUNApi:

    __SECRETE_ID__ = ""
    __SECRET_KEY__ = ""
    __BUSINESS_ID__ = ""
    __PIC_CHECK_URL__ = ""
    __TEXT_CHECK_URL__ = "https://api.aq.163.com/v3/text/check"
    __VERSION__ = "v3"


    @classmethod
    def gen_signature(cls, params=None):
        params_str = ""
        for k in sorted(params.keys()):
            params_str += str(k) + str(params[k])

        params_str += cls.__SECRET_KEY__
        return hashlib.md5(params_str).hexdigest()

    @classmethod
    def picture_check(cls):
        pass

    @classmethod
    def text_check(cls, params):
        params["secretId"] = cls.__SECRETE_ID__
        params["businessId"] = cls.__BUSINESS_ID__
        params["version"] = cls.__VERSION__
        params["timestamp"] = int(time.time() * 1000)
        params["nonce"] = int(random.random() * 100000000)
        params["signature"] = cls.gen_signature(params)

        try:
            params = urllib.urlencode(params)
            request = urllib2.Request(cls.__TEXT_CHECK_URL__, params)
            content = urllib2.urlopen(request, timeout=1).read()
            return json.loads(content)
        except Exception, ex:
            print "调用API接口失败:", str(ex)

        pass

    @classmethod
    def pic_check(cls, params):
        params["secretId"] = cls.__SECRETE_ID__
        params["businessId"] = cls.__BUSINESS_ID__
        params["version"] = cls.__VERSION__
        params["timestamp"] = int(time.time() * 1000)
        params["nonce"] = int(random.random() * 100000000)
        params["signature"] = cls.gen_signature(params)

        # print json.dumps(params)
        try:
            params = urllib.urlencode(params)
            request = urllib2.Request(cls.__PIC_CHECK_URL__, params)
            content = urllib2.urlopen(request, timeout=10).read()
            # print content
            # content = "{\"code\":200,\"msg\":\"ok\",\"timestamp\":1453793733515,\"nonce\":1524585,\"signature\":\"630afd9e389e68418bb10bc6d6522330\",\"result\":[{\"image\":\"http://img1.cache.netease.com/xxx1.jpg\",\"labels\":[]},{\"image\":\"http://img1.cache.netease.com/xxx2.jpg\",\"labels\":[{\"label\":100,\"level\":2,\"rate\":0.99},{\"label\":200,\"level\":1,\"rate\":0.5}]},{\"image\":\"http://img1.cache.netease.com/xxx3.jpg\",\"labels\":[{\"label\":200,\"level\":1,\"rate\":0.5}]}]}";
            return json.loads(content)
        except Exception, ex:
            print "调用API接口失败:", str(ex)