#coding=utf-8
from mongoengine import *
import logging
import datetime
from app.customer.models.user import *
from django.db import models
from base.settings import CHATPAMONGO


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class FeedbackInfo(Document):

    STATUS = [
        (0, u'未读'),
        (1, u'已读'),
        (2, u'已解决'),
        (3, u'暂缓解决'),
    ]

    user_id = IntField(verbose_name=u'用户id', required=True)
    created_at = DateTimeField(verbose_name=u'创建时间', default=None)
    user_agent = StringField(verbose_name=u'ua', max_length=256, default='')
    desc = StringField(verbose_name=u'问题描述', max_length=65535, default='')
    phone_number=StringField(verbose_name=u'电话号码',max_length=16, default='')
    qq_number=StringField(verbose_name=u'qq号码', max_length=32, default='')
    status = IntField(verbose_name=u"处理状态", default=0)  # 0：未处理 1：已处理 2:忽略
    update_time = DateTimeField(verbose_name=u"处理时间")
    operator = StringField(verbose_name=u"操作人")
    operaterecord = StringField(verbose_name=u"操作记录")
    is_answer = IntField(verbose_name=u'是否回复', default=0)  # 0:没回复 1：回复

    class Meta:
        app_label = "customer"
        verbose_name = u"反馈"
        verbose_name_plural = verbose_name

    @classmethod
    def create_feedback(cls, user_id, created_at, ua='', desc='', phone_number='',qq_number=''):
        try:
            feedback = FeedbackInfo(
                user_id=user_id,
                created_at=created_at,
                status=0,
                user_agent=ua,
                desc=desc,
                phone_number=phone_number,
                qq_number=qq_number,
            )
            feedback.save()
        except Exception,e:
            logging.error("create feedback error:{0}".format(e))
            return False
        return str(feedback.id)

    @classmethod
    def check_feedback(cls, user_id, created_at):
        feedbacks = FeedbackInfo.objects.filter(user_id=user_id).order_by('-created_at')
        if not feedbacks:
            return False
        else:
            last_time = feedbacks.first().created_at
            if created_at.strftime('%Y-%m-%d') == last_time.strftime('%Y-%m-%d'):
                return True
            else:
                return False
