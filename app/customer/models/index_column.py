# coding=utf-8

from django.db import models
import logging
import datetime
# from app.customer.models.user import User
from wi_model_util.imodel import *
from mongoengine import *
from base.settings import CHATPAMONGO


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)

# 首页栏目
class IndexColumn(Document):

    name = StringField(max_length=32, verbose_name=u'名称')
    column_type = IntField(verbose_name=u"栏目类型")
    delete_status = IntField(verbose_name=u"是否删除")  # 1:未删除   2:删除

    def normal_info(self):
        return {
            "name": self.name,
            "column_type": self.column_type
        }

