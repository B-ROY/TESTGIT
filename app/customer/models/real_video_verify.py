# coding=utf-8

from django.db import models
import logging
import datetime
from wi_model_util.imodel import *
from mongoengine import *
from base.settings import CHATPAMONGO

connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class RealVideoVerify(Document):

    VERIFY_STATUS = [
        (0, u"审核中"),
        (1, u"通过"),
        (2, u"未通过"),
    ]

    user_id = IntField(verbose_name=u"用户id")
    cover_url = StringField(verbose_name=u"封面照片地址", max_length=256)
    video_url = StringField(verbose_name=u"视频地址", max_length=256)
    feedback_reason = StringField(verbose_name=u"审核反馈", max_length=256)
    create_time = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())
    update_time = DateTimeField(verbose_name=u"更新时间")
    status = IntField(verbose_name=u"审核状态", choices=VERIFY_STATUS)
    is_valid = IntField(verbose_name=u"是否移除", default=1)  # 1.不移除 2.移除

    class Meta:
        app_label = "customer"
        verbose_name = u"视频认证"
        verbose_name_plural = verbose_name

    @classmethod
    def check_user_verify(cls, user_id):
        verify = RealVideoVerify.objects(user_id=user_id, status__ne=2).order_by("-create_time").first()
        if verify:
            return verify.status
        else:
            return 3