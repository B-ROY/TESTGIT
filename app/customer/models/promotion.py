# coding=utf-8
from django.db import models
import logging
from app.customer.models.user import *
import datetime
from mongoengine import *
from base.settings import CHATPAMONGO


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class Promotion(Document):

    STATUS = [
        (0, u"未参与"),
        (1, u"已参与"),
    ]

    TYPE = [
        (0, u"1元充值活动"),
        (1, u"赠送引力币活动"),
        (2, u"10元首充活动"),
    ]

    promotion_user = IntField(verbose_name=u"参与活动用户id", default=0)
    promotion_time = DateTimeField(verbose_name=u"参与活动时间", default=None)
    promotion_status = IntField(verbose_name=u"参与活动状态", default=0, choices=STATUS)
    promotion_type = IntField(verbose_name=u"活动类型", default=0, choices=TYPE)
    promotion_desc = StringField(verbose_name=u"描述", max_length=256, default=None)

    class Meta:
        app_label = "customer"
        verbose_name = u"促销活动"
        verbose_name_plural = verbose_name

    @classmethod
    def add_promotion_user(cls, promotion_user, promotion_time=None, promotion_status=1, promotion_type=0, promotion_desc=None):
        try:
            _obj = cls()
            _obj.promotion_user = promotion_user
            _obj.promotion_time = promotion_time
            _obj.promotion_status = promotion_status
            _obj.promotion_type = promotion_type
            _obj.promotion_desc = promotion_desc
            _obj.save()
            return _obj
        except Exception, e:
            logging.error("add promotion user error:{0}".format(e))
        return None

    @classmethod
    def check_status(cls, promotion_user, promotion_type):
        try:
            user = cls.objects.get(promotion_user=promotion_user, promotion_type=promotion_type)
            if not user.promotion_status:
                return False
            else:
                return True
        except Promotion.DoesNotExist:
            return False