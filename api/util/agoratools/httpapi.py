#coding=utf-8
import hashlib
import hmac
from hashlib import sha1
import sys
import datetime
import time
import ctypes
import requests
import json

appId = "edbfe06e96ec4bb0b4271adffa068031"
appCertificate = "0a69dde1c31249848f2834aff61ae8b8"
AGORA_SERVER_URL = "http://api.sig.agora.io/api1"


class HttpAPI:
    def __init__(self, appId, appCertificate, url=AGORA_SERVER_URL):
        self.appId = appId
        self.appCertificate = appCertificate
        self.callid = 1
        self.url = url

    def call(self, func, **kargs):
        self.callid += 1

        req = {
            '_vendorkey': self.appId,
            '_callid'   : self.callid,
            '_timestamp': datetime.datetime.now().isoformat(),
            '_function' : func,
        }
        req.update(kargs)

        keys = req.keys()
        keys.sort()
        signstr = ''.join(k+str(req[k]) for k in keys)
        signstr = signstr.lower()
        sign = hmac.new(self.appCertificate, signstr, hashlib.sha1).hexdigest()
        req['_sign'] = sign

        resp = requests.post(self.url, data=json.dumps(req))
        return resp.json()

    def sign(self,req):
        keys = req.keys()
        keys.sort()
        s = ''.join(k+str(req[k]) for k in keys)
        s = s.encode('utf-8')
        s = s.lower()
        print s
        sign = hmac.new(self.appCertificate, s, hashlib.sha1).hexdigest()
        return sign