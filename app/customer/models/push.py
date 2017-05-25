# coding=utf-8
from django.db import models
import re
import os
import logging
import urllib, urllib2, json, logging
import datetime
from django.conf import settings
from redis_model.queue import Client
import time

from app.customer.models.user import User
from mongoengine import *
from base.settings import CHATPAMONGO


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class PushMessage(Document):

    MESSAGE_TYPE = [
        (0, u'默认全部发送'),
        (1, u'发送给男性用户'),
        (2, u'发送给女性用户'),
    ]

    MESSAGE_STATUS = [
        (0, u'未发送'),
        (1, u'已发送'),
        (2, u'每日定时发送'),
    ]

    USE_STATUS = [
        (0, u'使用中'),
        (1, u'未使用'),
    ]

    desc = StringField(verbose_name=u"推送描述", max_length=4096)
    message_time = DateTimeField(verbose_name=u"单次推送时间", default=datetime.datetime.now())
    message_type = IntField(verbose_name=u"消息类型", choices=MESSAGE_TYPE)
    message_status = IntField(verbose_name=u"状态", choices=MESSAGE_STATUS)
    use_status = IntField(verbose_name=u"使用情况", choices=USE_STATUS)
    daily_time = StringField(verbose_name=u"发送每日推送小时", max_length=64, default="")

    class Meta:
        app_label = "customer"
        verbose_name = u"推送消息"
        verbose_name_plural = verbose_name

    @classmethod
    def create_message(cls, desc, message_time, message_type=0, message_status=0, use_status=0, daily_time=""):
        try:
            message = PushMessage(
                desc=desc,
                message_time=message_time,
                message_type=message_type,
                message_status=message_status,
                use_status=use_status,
                daily_time=daily_time,
            )
            message.save()
            return True
        except Exception,e:
            logging.error("create push message error:{0}".format(e))
            return False

    # 发送每日推送消息
    @classmethod
    def push_daily_message(cls):
        try:
            now_hour = str(datetime.datetime.now().hour)
            messages = PushMessage.objects.filter(use_status=0, message_status=2, daily_time=now_hour)
            for message in messages:
                PushService.send_daily_message(message_desc=message.desc, message_type=message.message_type)
            return True
        except Exception,e:
            logging.error("push daily message error:{0}".format(e))
            return False

    # 发送单次推送消息
    @classmethod
    def push_single_message(cls, message_id):
        try:
            message = PushMessage.objects.get(id=message_id)
            if message.message_status == 0:
                PushService.send_message(message_desc=message.desc, message_type=message.message_type)
                message.message_status = 1
                message.save()
                return True
            else:
                return False
        except Exception,e:
            logging.error("push message error:{0}".format(e))
            return False


class PushService(object):
    queue_client = Client()

    @classmethod
    def send_audio(cls, user_id, host_id, audio_room_id):
        data = {"user_id":user_id, "host_id":host_id, "audio_room_id":audio_room_id}
        cls.queue_client.dispatch("do_push.audio",data)

    @classmethod
    def send_message(cls, message_desc, message_type):
        data = {"message_desc": message_desc, "message_type": message_type}
        cls.queue_client.dispatch("do_push.message", data)

    @classmethod
    def send_daily_message(cls, message_desc, message_type):
        data = {"message_desc": message_desc, "message_type": message_type}
        cls.queue_client.dispatch("do_push.daily_message", data)