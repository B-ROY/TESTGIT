#coding=utf-8
from mongoengine import *
import logging
import datetime
import time
from base.core.util.dateutils import datetime_to_timestamp
from app.customer.models.user import *
from app.customer.models.account import *
from django.db import models
import re


class TestDB(Document):

    id = IntField(verbose_name=u'id', primary_key=True)
    name = StringField(verbose_name=u'名字', max_length=256, default="")
    date = DateTimeField(verbose_name=u'日期')

    class Meta:
        app_label = "audio"
        verbose_name = u"测试"
        verbose_name_plural = verbose_name

    @classmethod
    def create_test(cls, name):
        user_id = TestDB.objects.all().count() + 1
        try:
            test = TestDB(
                id=user_id,
                name=name,
                )
            test.save()
            return test.id

        except Exception,e:
            logging.error("create test error:{0}".format(e))
            return False


class TestDB2(Document):
    id = IntField(primary_key=True)
    name = StringField(max_length=256, default="")
    date = DateTimeField(default=datetime.datetime.now())
    refer_id = ReferenceField("TestDB", default=None)
    new_refer = ReferenceField("TestDB", default=None)

    class Meta:
        app_label = "audio"
        verbose_name = u"测试2"
        verbose_name_plural = verbose_name



def checkLuckNumber(number):
    #任意位置为ABCABC
    p = re.compile(r'^(?=\d*(\d)(\d)(\d)\1\2\3)\d{7}$')
    result = p.search(number)
    #任意位置为AABBCC
    p = re.compile(r'^(?=\d*(\d)\1(\d)\2(\d)\3)\d{7}$')
    result = result or p.search(number)
    #任意位置为AABB
    p = re.compile(r'^(?=\d*(\d)\1(\d)\2)\d{7}$')
    result = result or p.search(number)
    #末尾6位为AABBCC
    p = re.compile(r'^(?=\d*(\d)\1(\d)\2(\d)\3$)\d{7}$')
    result = result or p.search(number)
    #末尾4位为AABB
    p = re.compile(r'^(?=\d*(\d)\1(\d)\2$)\d{7}$')
    result = result or p.search(number)
    #末尾6位为ABCABC
    p = re.compile(r'^(?=\d*(\d)(\d)(\d)\1\2\3$)\d{7}$')
    result = result or p.search(number)
    #末尾4位为ABCD
    p = re.compile(r'^(?=\d*(0(?=1|$)|1(?=2)|2(?=3)|3(?=4|$)|4(?=5|$)|5(?=6|$)|6(?=7|$)|7(?=8|$)|8(?=9|$)|9(?=0|$)){4}$)\d{7}$')
    result = result or p.search(number)
    #末尾5位为ABCDE
    p = re.compile(r'^(?=\d*(0(?=1|$)|1(?=2)|2(?=3)|3(?=4|$)|4(?=5|$)|5(?=6|$)|6(?=7|$)|7(?=8|$)|8(?=9|$)|9(?=0|$)){5}$)\d{7}$')
    result = result or p.search(number)
    #末尾6位为ABCDE
    p = re.compile(r'^(?=\d*(0(?=1|$)|1(?=2)|2(?=3)|3(?=4|$)|4(?=5|$)|5(?=6|$)|6(?=7|$)|7(?=8|$)|8(?=9|$)|9(?=0|$)){6}$)\d{7}$')
    result = result or p.search(number)
    #末尾7位为ABCDE
    p = re.compile(r'^(?=\d*(0(?=1|$)|1(?=2)|2(?=3)|3(?=4|$)|4(?=5|$)|5(?=6|$)|6(?=7|$)|7(?=8|$)|8(?=9|$)|9(?=0|$)){7}$)\d{7}$')
    result = result or p.search(number)
    
    if not result:
        return False, number
    return True, number



