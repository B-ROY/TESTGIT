#coding=utf-8

import logging

from django.db import models
from app.customer.models.user import *
from app.customer.models.account import TradeDiamondRecord
from mongoengine import *
from base.settings import CHATPAMONGO


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class StartupImage(Document):

    STATUS = [
        (0, u'未使用'),
        (1, u'使用'),
    ]
    DELETE_STATUS = [
        (0, u'正常'),
        (1, u'删除'),
    ]
    STATUS_INVALID = 0
    STATUS_VALID = 1

    status = IntField(verbose_name=u'状态', choices=STATUS)
    delete_status = IntField(verbose_name=u'删除状态', choices=DELETE_STATUS, default=0)
    image = StringField(max_length=256, verbose_name=u'开机启动图')
    url = StringField(max_length=256, verbose_name=u'启动图url')

    @classmethod
    def create(cls, url, image, status=0):
        try:
            _obj = cls()
            _obj.url = url
            # _obj.image = image
            _obj.image = User.convert_http_to_https(image)
            _obj.status = status
            _obj.save()
            return _obj
        except Exception, e:
            logging.error("create StartupAdv error:{0}".format(e))
        return ''

    @classmethod
    def update(cls, obj_id, url, image, status=0):
        try:
            _obj = cls.objects.get(id=obj_id)
            # _obj.image = image
            _obj.image = User.convert_http_to_https(image)
            _obj.url = url
            _obj.status = status
            _obj.save()
            return _obj
        except Exception, e:
            logging.error("update StartupAdv error:{0}".format(e))
        return ''

    class Meta:
        app_label = "customer"
        verbose_name = u"启动图"
        verbose_name_plural = verbose_name


    @property
    def key(self):
        if self.id <= 10000:
            return "%05d" % self.id
        else:
            return self.id







