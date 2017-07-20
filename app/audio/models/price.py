#coding=utf-8
from mongoengine import *
import logging
from app.customer.models.user import *
from django.db import models
from base.settings import CHATPAMONGO


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class PriceList(Document):
    price = IntField(verbose_name=u'价格', required=True)
    desc = StringField(verbose_name=u'描述', max_length=64, default='')
    limit_time = IntField(verbose_name=u'最低选择时长')

    class Meta:
        app_label = "audio"
        verbose_name = u"价格"
        verbose_name_plural = verbose_name

    @classmethod
    def create_price(cls, price, desc=None, limit_time=0):
        try:
            price = PriceList(price=price, desc=desc, limit_time=limit_time)
            price.save()

        except Exception,e:
            logging.error("create price error:{0}".format(e))
            return False
        return True

    @classmethod
    def get_price_list(cls):
        price_list = cls.objects.all().order_by("-price")
        return price_list

    @classmethod
    def get_price_desc(cls, price):
        price_desc = cls.objects.get(price=price).desc
        return price_desc


class VideoPriceList(Document):
    price = IntField(verbose_name=u'价格', required=True)
    desc = StringField(verbose_name=u'描述', max_length=64, default='')
    limit_time = IntField(verbose_name=u'最低选择时长')

    class Meta:
        app_label = "video"
        verbose_name = u"视频价格"
        verbose_name_plural = verbose_name

    @classmethod
    def create_price(cls, price, desc=None, limit_time=0):
        try:
            price = VideoPriceList(price=price, desc=desc, limit_time=limit_time)
            price.save()

        except Exception,e:
            logging.error("create price error:{0}".format(e))
            return False
        return True

    @classmethod
    def get_price_list(cls):
        price_list = cls.objects.all().order_by("-price")
        return price_list

    @classmethod
    def get_price_desc(cls, price):
        price_desc = cls.objects.get(price=price).desc
        return price_desc

