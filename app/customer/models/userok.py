# coding=utf-8

import logging
import datetime
# from app.customer.models.user import User
from mongoengine import *
from base.settings import CHATPAMONGO


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class OkUser(Document):
    user_id = IntField(verbose_name="用户id")
    is_target = IntField(verbose_name="是不是目标用户") #1目标用户
    created_time = DateTimeField(verbose_name=u"添加时间")
    charge =  IntField(verbose_name="总充值")


    @classmethod
    def create(cls,userid,charge):
        try:
            _obj = cls()
            _obj.user_id = userid
            _obj.charge = charge
            _obj.is_target = 0
            _obj.created_time = datetime.datetime.now()
            _obj.save()
            return _obj
        except Exception, e:
            logging.error("create okuser error:{0}".format(e))
        return ''

