# coding=utf-8
from django.db import models
from mongoengine import *
import logging
import datetime
from base.settings import CHATPAMONGO

connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)

class ChannelInfo(Document):

    STATUS = [
        (0, u"使用中"),
        (1, u"已删除"),
    ]

    channel_num = StringField(verbose_name=u"渠道号", max_length=64)
    channel_name = StringField(verbose_name=u"渠道名称", max_length=64)
    status = IntField(verbose_name=u"状态", choices=STATUS)

    class Meta:
        app_label = "customer"
        verbose_name = u"渠道信息"
        verbose_name_plural = verbose_name

    @classmethod
    def create_channel(cls, channel_num, channel_name, status=0):
        try:
            channel = ChannelInfo(
                channel_num=channel_num,
                channel_name=channel_name,
                status=status
            )
            channel.save()
            return True
        except Exception, e:
            logging.error("create channel error:{0}".format(e))
            return False

    @classmethod
    def delete_channel(cls, channel_id):
        try:
            channel = ChannelInfo.objects.get(id=channel_id)
            channel.status = 1
            channel.save()
            return True
        except Exception, e:
            logging.error("delete channel error:{0}".format(e))
            return False

    @classmethod
    def get_channel_list(cls):
        channels = ChannelInfo.objects.filter(status=0)
        return channels
