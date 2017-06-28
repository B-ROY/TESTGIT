# coding=utf-8

from mongoengine import *


class ChannelAuditInfo(Document):

    channel_id = StringField(verbose_name=u"渠道号", unique=True)
    version = StringField(verbose_name=u"当前版本号")
    audit_switch = IntField(verbose_name=u"审核开关是否开启, 0:关闭，1：开启")
    is_delete = IntField(verbose_name=u"是否删除")#1:删除 0：非删除

    @classmethod
    def add_audit_info(cls, channel, version, audit_swith=0):
        obj_ = cls()
        obj_.channel = channel
        obj_.version = version
        obj_.audit_switch = audit_swith
        obj_.save()

    @classmethod
    def update_audit_info(cls, channel_id, version, audit_switch):
        channel = cls.objects.filter(channel_id=channel_id)
        channel.update(set__version=version, set__audit_swith=audit_switch)

    @classmethod
    def delete_audit_info(cls, channel_id):
        cls.objects.filter(chanel_id=channel_id).update(set__is_delete=1)

    @classmethod
    def get_audit_info(cls, channel):
        return cls.objects.filter(channel_id=channel)

