#coding=utf-8
import urllib
import os,sys
import time

from app.audio.im.http_request import RequestApi
from api.util.tencenttools.signature import gen_signature
from django.conf import settings
import json

class QCloudIM(object):


    def __init__(self):
        pass


    @classmethod
    def message_in_push(self, pushID, to_recv, random_int, desc):
        """
        发送单聊文本消息
        """

        app_id = "1400022298"
        sig = gen_signature(app_id, "admin")
        print sig

        uri = "/v4/openim/sendmsg?usersig=%s&identifier=admin&sdkappid=%s&random=%s&contenttype=json"%(sig, app_id ,random_int)
        print uri
        message = {
            "messageTypeKey": 500,
            "content": desc,
        }

        content = json.dumps(message)

        body = {
            "SyncOtherMachine": 2,
            "From_Account": pushID,
            "To_Account": to_recv,
            "MsgRandom": random_int,
            "MsgBody": [
                {
                    "MsgType": "TIMCustomElem",
                    "MsgContent": {
                        "Data": content,
                        "Desc": "world",
                    }
                }
            ]
        }

        body = json.dumps(body)
        print body
        data = RequestApi.post_body_request(uri, body, headers={}, host='console.tim.qq.com')
        result = json.loads(data)
        print result

        if result.get("ActionStatus") == "OK":
            return True
        else:
            return False

