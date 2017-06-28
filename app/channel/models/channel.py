# coding=utf-8

from mongoengine import *


class Channel(Document):

    CHANNEL_PLATFORM = [
        (0, "IOS"),
        (1, "Android")
    ]

    channel_id = StringField(verbose_name=u"渠道号", unique=True)
    channel_name = StringField(verbose_name=u"渠道名称")
    channel_desc = StringField(verbose_name=u"渠道描述")
    channel_platform = IntField(verbose_name=u"渠道所属平台", choices=CHANNEL_PLATFORM)


    @classmethod
    def add_channel(cls, channel_id, channel_platform, channel_name="", channel_desc=""):
        obj_= cls()
        obj_.channel_id = channel_id
        obj_.channel_platform = channel_platform
        obj_.channel_name = channel_name
        obj_.channel_desc = channel_desc
        obj_.save()

    @classmethod
    def delete_channel(cls, channel_id):
        channel = cls.objects.filter(channel_id=channel_id)
        channel.delete()

    @classmethod
    def batch_delete_channel(cls, channel_ids):
        cls.objects.filter(chanel_id__in=channel_ids).delete()

    @classmethod
    def update_channel(cls, channel_id, channel_platform, channel_name="", channel_desc=""):
        channel = Channel.objects.filter(channel_id=channel_id)
        channel.update(set__channel_platform=channel_platform, channel_name=channel_name, channel_desc=channel_desc)
