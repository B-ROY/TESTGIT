# coding=utf-8
import hmac
import base64
import uuid
import time
import urllib
import hashlib
import copy
from http_request import RequestApi

class TwitterAPI(object):

    CONSUMER_KEY = "xvz1evFS4wEEPTGEFPHBog"
    Host = "api.twitter.com"
    PATH = "/1.1/users/show.json"
    HTTP_Method = "GET"
    oauth_signature_method = "HMAC-SHA1"

    CONSUMER_SECRET = "X4S4OUtSCEGAPpWHBiZFncNI6"
    OAUTH_TOKEN_SECRET = "W9TGrI4BCFs26pCcsTH57MuyYT8adxomO69lX2dmect38"

    @classmethod
    def get_user_info(cls, user_id, access_token):
        access_token = "757489947993485312-9aENEkcBKfGn2NTF2Lx00lLaILgnO8s"

        dic = {
            "oauth_consumer_key"  : cls.CONSUMER_KEY,
            "oauth_nonce": base64.b64encode(str(uuid.uuid1())),
            "oauth_signature_method": cls.oauth_signature_method,
            "oauth_timestamp ": str(int(time.time())),
            "oauth_token": access_token,
            "oauth_version": "1.0",
        }
        param_map = {}
        oauth_signature = cls.get_signature(dic, param_map),
        param_map["user_id"] = 757489947993485312
        dic["oauth_signature"] = oauth_signature

        data = RequestApi.get(cls.PATH, param_map, dic, host=cls.Host)

        print data

    @classmethod
    def get_signature(cls, dic, param_map):
        dic1 = copy.copy(dic)
        dic1.update(param_map)
        sort_param = sorted(
            [(key, unicode(value).encode('utf-8')) for key, value in dic1.iteritems()],
            key=lambda x: x[0]
        )
        content = '&'.join(['='.join(x) for x in sort_param])
        content = cls.HTTP_Method + "&" + cls.Host + cls.PATH + "&" +content
        print content
        sigining_key = urllib.quote(cls.CONSUMER_SECRET+"&"+cls.OAUTH_TOKEN_SECRET)

        ss = hmac.new(sigining_key, content, hashlib.sha1).hexdigest()

        signature = base64.b64encode(ss)

        return signature