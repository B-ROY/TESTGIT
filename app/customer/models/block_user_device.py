# coding=utf-8
from django.db import models
import logging
from mongoengine import *
from base.settings import CHATPAMONGO


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)

# 封号状态查询

class BlockUserDev(Document):

    id = IntField(verbose_name=u"封号记录id", primary_key=True)
    block_user = IntField(verbose_name=u"被封号者")
    block_admin = IntField(verbose_name=u"封号者")
    block_start = DateTimeField(verbose_name=u"封号开始时间", default=None)
    block_end = DateTimeField(verbose_name=u"封号结束时间", default=None)
    created_time =  DateTimeField(verbose_name=u"创建时间", default=None)
    update_time =  DateTimeField(verbose_name=u"修改时间", default=None)
    status = IntField(verbose_name=u"状态", default=None)#3解封 1封一周 2 永久封
    reason = StringField(verbose_name=u"原因", max_length=280, default=None)
    devno = StringField(verbose_name=u"设备号", max_length=280, default=None)
    block_type = IntField(verbose_name=u"封号类型")#1封设备 2封id


    class Meta:
        app_label = "customer"
        verbose_name = u"用户设备封号"
        verbose_name_plural = verbose_name


    @classmethod
    def add_block_user(cls, block_user, block_admin, block_start=None, block_end=None, status=None, reason=None,devno=None,created_time=None,update_time=None,block_type=None):
        # count = BlockUser.objects.filter(block_user=block_user).count()
        # if count == 0:
        try:
            _obj = cls()
            _obj.id = cls.objects.all().count() + 1
            _obj.block_user = block_user
            _obj.block_admin = block_admin
            _obj.block_start = block_start
            _obj.block_end = block_end
            _obj.status = status
            _obj.reason = reason
            _obj.created_time = created_time
            _obj.update_time = update_time
            _obj.block_type = block_type
            _obj.save()
            return _obj
        except Exception, e:
            logging.error("add block user dev error:{0}".format(e))
            # return None

