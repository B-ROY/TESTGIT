#coding=utf-8
import json
from app.util.messageque.http_request import RequestApi
import logging
from django.conf import settings


class MessageSender:
    Host = settings.Message_Tornado_host

    @classmethod
    def send_bottle_message(cls, from_id, desc):
        body = {}
        body["from_id"] = from_id
        body["desc"] = desc
        path = "/tecent/bottle"
        data = RequestApi.post_body_request_http(path=path, body=json.dumps(body), headers={}, host=cls.Host)
        result = json.loads(data)
        print result.get("status_code")
        if result.get("status_code")==200:
            return 200
        elif result.get("status_code") ==400:
            logging.error("send bottle message to mq error")
            return 400


    @classmethod
    def send_bottle_message_v3(cls, from_id, desc, gender):
        body = {}
        body["from_id"] = from_id
        body["desc"] = desc
        body["gender"] = gender
        path = "/tecent/bottle_v3"
        data = RequestApi.post_body_request_http(path=path, body=json.dumps(body), headers={}, host=cls.Host)
        result = json.loads(data)
        print result.get("status_code")
        if result.get("status_code") == 200:
            return 200
        elif result.get("status_code") == 400:
            logging.error("send bottle message to mq error")
            return 400


    @classmethod
    def send_block_user_message(cls, user_id, desc):
        body = {}
        body["block_id"] = user_id
        body["desc"] = desc
        path = "/tecent/bottle"
        data = RequestApi.post_body_request_http(path=path, body=json.dumps(body), headers={}, host=cls.Host)
        result = json.loads(data)
        print result.get("status_code")
        print 1234566
        if result.get("status_code") == 200:
            return 200
        elif result.get("status_code") == 400:
            logging.error("send blocker_user message to mq error")
            return 400

    @classmethod
    def send_charge_bottle_message(cls, from_id):
        body = {}
        body["from_id"] = from_id
        desc = u"我已经成为土豪,快来撩我吧～"
        body["desc"] = desc
        path = "/tecent/charge_bottle"
        data = RequestApi.post_body_request_http(path=path, body=json.dumps(body), headers={}, host=cls.Host)
        result = json.loads(data)
        print result.get("status_code")
        if result.get("status_code") == 200:
            return 200
        elif result.get("status_code") == 400:
            logging.error("send charge bottle message to mq error")
            return 400


    @classmethod
    def send_system_message(cls, to_user_id, desc):
        body = {}
        body["to_user_id"] = to_user_id
        body["desc"] = desc
        path = "/tecent/system_message"
        data = RequestApi.post_body_request_http(path=path, body=json.dumps(body), headers={}, host=cls.Host)
        result = json.loads(data)
        print result.get("status_code")
        if result.get("status_code") == 200:
            return 200
        elif result.get("status_code") == 400:
            logging.error("send system message to mq error")
            return



    @classmethod
    def send_big_gift_info_message(cls, sender_id, sender_name, receiver_id, receiver_name, gift_id, gift_name,
                                   gift_count):
        body = {
            "sender_id": sender_id,
            "sender_name": sender_name,
            "receiver_id": receiver_id,
            "receiver_name": receiver_name,
            "gift_id": gift_id,
            "gift_count": gift_count,
            "gift_name": gift_name
        }
        path = "/tecent/information/big_gift"
        data = RequestApi.post_body_request_http(path=path, body=json.dumps(body), headers={}, host=cls.Host)
        print data
        print cls.Host
        result = json.loads(data)
        print result.get("status_code")
        if result.get("status_code") == 200:
            return 200
        elif result.get("status_code") == 400:
            logging.error("send big gift message to mq error")
            return 400

    @classmethod
    def send_charge_info_message(cls, user_id, user_name, money):
        body = {
            "user_id": user_id,
            "user_name": user_name,
            "money": money
        }
        path = "/tecent/information/charge"
        data = RequestApi.post_body_request_http(path=path, body=json.dumps(body), headers={}, host=cls.Host)
        print data
        print cls.Host
        result = json.loads(data)
        print result.get("status_code")
        if result.get("status_code") == 200:
            return 200
        elif result.get("status_code") == 400:
            logging.error("send charge info message to mq error")
            return 400

    @classmethod
    def send_video_auth_info_message(cls, user_id, user_name):
        body = {
            "user_id": user_id,
            "user_name": user_name,
        }
        path = "/tecent/information/video_auth"
        data = RequestApi.post_body_request_http(path=path, body=json.dumps(body), headers={}, host=cls.Host)
        print data
        print cls.Host
        result = json.loads(data)
        print result.get("status_code")
        if result.get("status_code") == 200:
            return 200
        elif result.get("status_code") == 400:
            logging.error("send video auth info message to mq error")
            return 400

    @classmethod
    def send_activity_info_message(cls, user_id, user_name, desc):
        body = {
            "user_id": user_id,
            "user_name": user_name,
            "desc": desc
        }
        path = "/tecent/information/activity"
        data = RequestApi.post_body_request_http(path=path, body=json.dumps(body), headers={}, host=cls.Host)
        print data
        print cls.Host
        result = json.loads(data)
        print result.get("status_code")
        if result.get("status_code") == 200:
            return 200
        elif result.get("status_code") == 400:
            logging.error("send activity info message to mq error")
            return 400

    @classmethod
    def send_withdraw_info_message(cls, user_id, user_name, money):
        body = {
            "user_id": user_id,
            "user_name": user_name,
            "money": money,
        }
        path = "/tecent/information/withdraw"
        data = RequestApi.post_body_request_http(path=path, body=json.dumps(body), headers={}, host=cls.Host)
        print data
        result = json.loads(data)
        print result.get("status_code")
        if result.get("status_code") == 200:
            return 200
        elif result.get("status_code") == 400:
            logging.error("send withdraw info message to mq error")
            return 400


    @classmethod
    def send_porn_check(cls, file_id, pic_url, room_id, user_id, join_id, room_user_id):
        body = {
            "file_id": file_id,
            "pic_url": pic_url,
            "room_id": room_id,
            "user_id": user_id,
            "join_id": join_id,
            "room_user_id": room_user_id
        }
        path = "/audit/porn_check"
        data = RequestApi.post_body_request_http(path=path, body=json.dumps(body), headers={}, host=cls.Host)
        print data
        result = json.loads(data)
        print result.get("status_code")
        if result.get("status_code") == 200:
            return 200
        elif result.get("status_code") == 400:
            logging.error("send porn_check message to mq error")
            return 400

    @classmethod
    def send_picture_detect(cls, pic_url="", user_id=0, pic_channel=0, source=0, obj_id=None):
        if source == 1:
            body = {
                "pic_url": pic_url,
                "user_id": user_id,
                "pic_channel": pic_channel,
                "source": source
            }
        elif source == 2:
            # 2: 社区动态 图片
            body = {
                "obj_id": obj_id,
                "source": source
            }
        elif source == 3:
            #  3:个人相册
            body = {
                "pic_urls": pic_url,  # 多个用逗号分隔
                "source": source,
                "user_id": user_id
            }
        elif source == 4:
            #  4:聊天图片鉴定
            body = {
                "pic_url": pic_url,
                "source": source,
                "obj_id": obj_id
            }
        else:
            return 400

        path = "/audit/pic_check"
        data = RequestApi.post_body_request_http(path=path, body=json.dumps(body), headers={}, host=cls.Host)
        print data
        result = json.loads(data)
        print result.get("status_code")
        if result.get("status_code") == 200:
            return 200
        elif result.get("status_code") == 400:
            logging.error("send pic_check message to mq error")
            return 400

    @classmethod
    def send_text_check(cls, text, user_id, text_channel, ip):
        body = {
            "text": text,
            "user_id": user_id,
            "text_channel": text_channel,
            "ip": ip
        }
        path = "/audit/text_check"
        data = RequestApi.post_body_request_http(path=path, body=json.dumps(body), headers={}, host=cls.Host)
        print data
        result = json.loads(data)
        print result.get("status_code")
        if result.get("status_code") == 200:
            return 200
        elif result.get("status_code") == 400:
            logging.error("send text_check message to mq error")
            return 400

    @classmethod
    def send_about_me_message(cls, user_id):
        body = {}
        body["user_id"] = user_id
        path = "/tecent/about_me"
        data = RequestApi.post_body_request_http(path=path, body=json.dumps(body), headers={}, host=cls.Host)
        result = json.loads(data)
        print result.get("status_code")
        if result.get("status_code") == 200:
            return 200
        elif result.get("status_code") == 400:
            logging.error("send about me message to mq error")
            return 400


    @classmethod
    def send_return_tool(cls, from_id, to_id, type):
        body = {}
        body["from_id"] = from_id
        body["to_id"] = to_id
        body["close_type"] = type
        path = "/tecent/return_tool"
        data = RequestApi.post_body_request_http(path=path, body=json.dumps(body), headers={}, host=cls.Host)
        result = json.loads(data)
        if result.get("status_code") == 200:
            return 200
        elif result.get("status_code") == 400:
            logging.error("send_return_tool to mq error")
            return 400
