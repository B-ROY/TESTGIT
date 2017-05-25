# coding=utf-8

import logging

from django.db import models
from app.customer.models.account import TradeDiamondRecord

from app.customer.models.user import *
from mongoengine import *
from base.settings import CHATPAMONGO


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class Adv(Document):
    STATUS = [
        (0, u'未使用'),
        (1, u'使用'),
    ]

    DELETE_STATUS = [
        (0, u'正常'),
        (1, u'删除'),
    ]

    ADV_TYPE = [
        (0, u'URL内'),
        (1, u'URL外'),
        (2, u'房间'),
        (3, u'个人详情页'),
        (4, u'充值页'),
    ]

    status = IntField(verbose_name=u'状态', choices=STATUS)
    delete_status = IntField(verbose_name=u'删除状态', choices=DELETE_STATUS, default=0)
    adv_info = StringField(max_length=256, verbose_name=u'跳转信息')
    adv_type = IntField(verbose_name='跳转类型', choices=ADV_TYPE)
    image = StringField(max_length=256, verbose_name=u'广告图片')
    title = StringField(max_length=50, verbose_name=u'广告标题')
    seq = IntField(verbose_name=u'排序', default=0)

    class Meta:
        app_label = "customer"
        verbose_name = u"广告"
        verbose_name_plural = verbose_name

    def normal_info(self):
        return {
            "adv_info": self.adv_info,
            "adv_type": self.adv_type,
            "image": self.image,
            "seq": self.seq,
            "title": self.title,
        }

    @classmethod
    def get_list(cls):
        return Adv.objects.filter(status=1, delete_status=0).order_by("seq")

    @classmethod
    def create(cls, title, adv_info, image, adv_type, status=0):
        try:
            _obj = cls()
            _obj.adv_info = adv_info
            _obj.title = title
            # _obj.image = image
            _obj.image = User.convert_http_to_https(image)
            _obj.adv_type = adv_type
            _obj.status = status
            _obj.save()
            return _obj
        except Exception, e:
            logging.error("create Gift error:{0}".format(e))
        return ''

    @classmethod
    def update(cls, obj_id, title, adv_info, image, adv_type, status=0):
        try:
            _obj = cls.objects.get(id=obj_id)
            _obj.adv_info = adv_info
            # _obj.image = image
            _obj.image = User.convert_http_to_https(image)
            _obj.title = title
            _obj.status = status
            _obj.adv_type = adv_type
            _obj.save()
            return _obj
        except Exception, e:
            logging.error("update Gift error:{0}".format(e))
        return ''











