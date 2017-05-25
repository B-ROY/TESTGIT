# coding=utf-8
from django.db import models
from mongoengine import *
from base.settings import CHATPAMONGO
import datetime

connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,password=CHATPAMONGO.password)

class Anchor(Document):

    sid = IntField(verbose_name=u"用户短id")
    identity = IntField(verbose_name=u"用户长id")
    nickname = StringField(verbose_name=u"用户昵称", max_length=32)
    created_at = DateTimeField(verbose_name=u"添加时间", default=datetime.datetime.now())

    class Meta:
        app_label = "customer"
        verbose_name = u"热门主播"
        verbose_name_plural = verbose_name
