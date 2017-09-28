# coding=utf-8

import logging

from django.db import models
from app.customer.models.account import TradeDiamondRecord

from app.customer.models.user import *
from mongoengine import *
from base.settings import CHATPAMONGO


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class TempInviteTicket(Document):
    invite_ticket = IntField(verbose_name=u'邀请收益')
    user_name = StringField(max_length=256, verbose_name=u'用户名')
    create_time = DateTimeField(verbose_name=u"创建时间")
    delete_status = IntField(verbose_name=u"是否删除")  # 0:否  1: 是

    @classmethod
    def create(cls, user_name, invite_ticket):
        try:
            _obj = cls()
            _obj.user_name = user_name
            _obj.invite_ticket = invite_ticket
            _obj.delete_status = 0
            _obj.create_time = datetime.datetime.now()
            _obj.save()
            return _obj
        except Exception, e:
            logging.error("create Gift error:{0}".format(e))
        return ''

