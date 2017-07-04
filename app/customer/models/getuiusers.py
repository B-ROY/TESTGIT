# coding=utf-8

import datetime
import logging

from base.settings import CHATPAMONGO
from django.conf import settings
from mongoengine import *


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class GeTuiUsers(Document):
    user_id = IntField(verbose_name=u'用户id')
    dev_no = StringField(max_length=64,verbose_name=u'设备id')
    platfrom = StringField(max_length=10,verbose_name=u'平台') #1ios 2andriod
    os_version = StringField(max_length=20,verbose_name=u'操作系统版本号')
    cid = StringField(max_length=64,verbose_name=u'个推clientid')
    province = StringField(max_length=20, verbose_name=u'省份')
    city = StringField(max_length=64, verbose_name=u'城市')
    districts = StringField(max_length=64, verbose_name=u'区')
    address = StringField(max_length=128, verbose_name=u'地址')
    create_time = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())


