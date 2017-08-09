# coding=utf-8

from django.db import models
import logging
import datetime
from wi_model_util.imodel import *
from mongoengine import *
from base.settings import CHATPAMONGO

connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class PrivateVideo(Document):

    user_id = IntField(verbose_name=u"用户id")
    cover_url = StringField(verbose_name=u"封面照片地址", max_length=256)
    video_url = StringField(verbose_name=u"视频地址", max_length=256)
    price = IntField(verbose_name=u"视频价格")
    create_time = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())
    delete_status = IntField(verbose_name=u"是否删除")  # 1:不删除 2:删除
    is_valid = IntField(verbose_name=u"是否忽略(cms使用)", default=1)  # 1.不忽略 2.忽略

    class Meta:
        app_label = "customer"
        verbose_name = u"私房视频"
        verbose_name_plural = verbose_name
