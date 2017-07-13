# coding=utf-8

import time
import datetime
import logging
import random


"""
http://www.bootcss.com/p/bootstrap-switch/
https://github.com/bootstrap-tagsinput/bootstrap-tagsinput
"""
from mongoengine import *
from base.settings import CHATPAMONGO


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


switcher_info = {}

class Switcher(Document):

    SWITCH_PlATFORM = [
        (u'IOS', u'IOS'),
        (u'ANDROID', u'ANDROID'),
        (u'H5', u'H5'),
        (u'WEB', u'WEB'),
        (u'ALL', u'ALL'),
    ]

    DELETE_STATUS = [
        (0, u'正常'),
        (1, u'删除'),
    ]

    name = StringField(verbose_name=u'名称', max_length=100, default=0)
    description = StringField(max_length=255, verbose_name=u'描述')
    platform = StringField(verbose_name=u'平台,逗号分隔', max_length=255, default=0)
    created_time = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())
    status = StringField(max_length=255, verbose_name=u'值')
    delete_status = IntField(verbose_name=u'删除状态', choices=DELETE_STATUS, default=0)

    def __unicode__(self):
        return self.description

    class Meta:
        app_label = "customer"
        verbose_name = u"开关"
        verbose_name_plural = verbose_name

    @classmethod
    def create(cls, name, description, platform, status=''):
        try:
            obj = cls()
            obj.name = name
            obj.description = description
            obj.platform = platform.upper()
            obj.status = status
            obj.created_time = datetime.datetime.now()
            obj.save()
            return obj
        except Exception, e:
            logging.error("create Switcher error:{0}".format(e))

    @classmethod
    def update(cls, obj_id, name, description, platform, status=''):
        try:
            obj = cls.objects.get(id=obj_id)
            obj.name = name
            obj.description = description
            obj.platform = platform.upper()
            obj.status = status
            obj.save()
            return obj
        except Exception, e:
            logging.error("create Switcher error:{0}".format(e))

    @classmethod
    def get_all(cls):
        return cls.objects.filter(delete_status=0)

    @classmethod
    def get_on_switches(cls, platform):
        platform = platform.upper()
        results = []
        switchers = cls.get_all()
        for switch in switchers:
            if platform.upper() in switch.platform:
                results.append(switch)
        return results


