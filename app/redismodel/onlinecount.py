# coding=utf-8

from mongoengine import *


class OnlineCount(Document):

    charge_count = IntField(verbose_name=u"充值人数")
    online_count = IntField(verbose_name=u"在线人数")
    update_time = DateTimeField(verbose_name=u"更新时间")
