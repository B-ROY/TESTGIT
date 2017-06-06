# coding=utf-8
from django.db import models
import logging
from app.customer.models.user import User
import datetime
from mongoengine import *
from base.settings import CHATPAMONGO


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)

# 封号状态查询

class BlockUser(Document):

    id = IntField(verbose_name=u"封号记录id", primary_key=True)
    block_user = IntField(verbose_name=u"被封号者")
    block_admin = IntField(verbose_name=u"封号者")
    block_room = GenericReferenceField("LiveRoom", verbose_name=u"被封房间", default=None)
    block_start = DateTimeField(verbose_name=u"封号开始时间", default=None)
    block_end = DateTimeField(verbose_name=u"封号结束时间", default=None)
    status = IntField(verbose_name=u"状态", default=0)
    reason = StringField(verbose_name=u"原因", max_length=280, default=None)


    class Meta:
        app_label = "customer"
        verbose_name = u"用户被封号"
        verbose_name_plural = verbose_name

    @classmethod
    def add_block_user(cls, block_user, block_admin, block_room=None, block_start=None, block_end=None, status=0, reason=None):
        try:
            _obj = cls()
            _obj.id = cls.objects.all().count() + 1
            _obj.block_user = block_user
            _obj.block_admin = block_admin
            _obj.block_room = block_room
            _obj.block_start = block_start
            _obj.block_end = block_end
            _obj.status = status
            _obj.reason = reason

            _obj.save()
            return _obj
        except Exception, e:
            logging.error("add block user error:{0}".format(e))
        return None

    @classmethod
    def update_block_user(cls, block_user, block_room=None, block_start=None, block_end=None, reason=None):
        try:
            _obj = cls.objects.filter(block_user=block_user).order_by("-block_start").first()
            if block_room:
                _obj.block_room = block_room
            if block_start:
                _obj.block_start = block_start
            if block_end:
                _obj.block_end = block_end
            if reason:
                _obj.reason = reason

            _obj.save()
            return _obj
        except Exception, e:
            logging.error("update block user error:{0}".format(e))
        return None

    # set status = 1
    @classmethod
    def status_active(self):
        self.status = 1
        self.save()

    # set status = 0
    @classmethod
    def status_inactive(self):
        self.status = 0
        self.save()


    @classmethod
    def search_block_user_status(cls, user):
        return cls.objects.filter(block_user=user).order_by("-block_start").first()

    def cancel_block(self):
        self.block_end = datetime.datetime.now()
        self.status = 0
        user = User.objects.get(id=self.block_user)
        user.is_block = 0
        user.save()
        self.save()




