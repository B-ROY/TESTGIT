# coding=utf-8
from django.db import models
import logging
from app.customer.models.user import User
from wi_model_util.imodel import *
from django.db.models import Q
import time
import datetime
from mongoengine import *
from base.settings import CHATPAMONGO


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class HoldManage(Document):
    liveowner_id = IntField(verbose_name=u'主播ID', unique=False)
    viewer_id = IntField(verbose_name=u'用户ID')
    hold_start_time = StringField(verbose_name=u"禁言开始时间", max_length=255, default='')
    hold_end_time = StringField(verbose_name=u"禁言结束时间", max_length=255, default='')
    is_block = IntField(verbose_name='是否拉黑', default=0)
    is_hold = IntField(verbose_name='是否禁言', default=0)
    is_admin = IntField(verbose_name='是否设置管理', default=0)

    class Meta:
        app_label = "customer"
        verbose_name = u"主播管理禁言与拉黑"
        verbose_name_plural = verbose_name

    @classmethod
    def get_liveowner_hold_info(cls, uid):
        holdmanages = {}
        hm_hold = HoldManage.objects.filter(liveowner_id=uid, is_hold=1).all()
        if hm_hold:
            holds = []
            for v in hm_hold:
                kv = {}
                kv["uid"] = v.viewer_id
                kv["hold_time"] = v.hold_end_time
                holds.append(kv)

            holdmanages["hold"] = holds

        hm_admin = HoldManage.objects.filter(liveowner_id=uid, is_admin=1).all()
        if hm_admin:
            admins = []
            for v in hm_admin:
                kv = {}
                kv["uid"] = v.viewer_id
                admins.append(kv)
            holdmanages["admin"] = admins

        return holdmanages

    @classmethod
    def set_hold(cls, uid, viewerid):
        try:
            cls.gen(uid, viewerid, ishold=1)
        except Exception, e:
            return False, e.message
        return True, None

    @classmethod
    def set_unhold(cls, uid, viewerid):
        try:
            cls.gen(uid, viewerid, ishold=0)
        except Exception, e:
            return False, e.message
        return True, None

    @classmethod
    def set_admin(cls, uid, viewerid):
        try:
            cls.gen(uid, viewerid, isadmin=1)
        except Exception, e:
            return False, e.message
        return True, None

    @classmethod
    def set_unadmin(cls, uid, viewerid):
        try:
            cls.gen(uid, viewerid, isadmin=0)
        except Exception, e:
            return False, e.message
        return True, None

    @classmethod
    def gen(cls, uid, viewerid, isadmin=0, isblock=0, ishold=0):
        hm = HoldManage.objects.filter(liveowner_id=uid, viewer_id=viewerid).first()
        if not hm:
            hm = HoldManage(
                liveowner_id=uid,
                viewer_id=viewerid,
                is_admin=isadmin,
                is_block=isblock,
                is_hold=ishold,
            )
            is_new = True
        else:
            hm.is_admin = isadmin
            hm.is_block = isblock
            hm.is_hold = ishold
            is_new = False

        if ishold:
            hm.hold_start_time = str(int(time.time()))
            hm.hold_end_time = str(int(hm.hold_start_time) + 7200)
            hm.is_admin = 0
        else:
            hm.hold_end_time = None
            hm.hold_start_time = None

        hm.save()
        return is_new, hm