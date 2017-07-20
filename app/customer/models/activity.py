# coding=utf-8

import datetime
import logging

from base.settings import CHATPAMONGO
from django.conf import settings
from mongoengine import *


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class Activity(Document):
    STATUS = [
        (0, u'关闭'),
        (1, u'开启'),
    ]

    name = StringField(max_length=32, verbose_name=u'活动名称')
    status_type = IntField(verbose_name=u'状态', choices=STATUS)
    img_url = StringField(max_length=256, verbose_name=u'活动图url')
    activity_url = StringField(max_length=256, verbose_name=u'活动链接地址')
    create_time = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())
    is_valid = IntField(verbose_name=u'是否有效', default=1)  # 1有效 0 无效
    join_in_tool_activity = IntField(verbose_name=u'我的道具中是否显示平台活动', default=1)  # 1不显示 2 显示

    def normal_info(self):
        return {
            "name": self.name,
            "img_url": self.img_url,
            "activity_url": self.activity_url
        }
