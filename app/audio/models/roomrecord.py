#coding=utf-8

from mongoengine import *
import logging
import datetime
import time
from base.core.util.dateutils import datetime_to_timestamp
from app.customer.models.user import *
from app.customer.models.account import *
from app.customer.models.online_user import *
from django.db import models
from base.settings import CHATPAMONGO
from app.customer.models import user


class RoomRecord(Document):

    user_id = IntField(verbose_name=u"房主id")
    join_id = IntField(verbose_name=u"加入者id")
    price = IntField(verbose_name=u"房间价格")
    room_type = IntField(verbose_name=u"房间类型")#1.视频房间 0.语音房间
    create_time = DateTimeField(verbose_name=u"房间记录创建时间 以拨打时间计")
    is_answer = IntField(verbose_name=u"是否接通")#1.接通 2.未接通
    start_time = DateTimeField(verbose_name=u"房间正式通话时间， 以主播接通时间计")
    end_time = DateTimeField(verbose_name=u"房间结束通话时间， 挂断时间")
    end_type = IntField(verbose_name=u"房间挂断类型") #1. 用户取消请请求 2. 用户挂断 3.用户异常挂断 4.主播拒绝 5 主播挂断 6 主播异常挂断
    report_time_user = DateTimeField(verbose_name=u"房主的上报时间")
    report_time_join = DateTimeField(verbose_name=u"加入者的上报时间")
    last_pay_time = DateTimeField(verbose_name=u"最后付费时间")
    pay_times = IntField(verbose_name=u"用户付费时间")
    room_status = IntField(verbose_name=u"房间状态")# 由于延迟造成的不同步（譬如 用户拨打电话 挂断的同时 主播接听了），
                                                    # 记录一下房间状态 1.开启 2.已结束
    gift_value = IntField(verbose_name=u"房间赠送礼物价值")

    @classmethod
    def create_room_reocord(cls, user_id, join_id, price, room_type):
        record = cls()
        record.user_id = user_id
        record.join_id = join_id
        record.price = price
        record.room_type = room_type
        record.create_time = datetime.datetime.now()
        record.is_answer = 2
        record.room_status = 1
        record.gift_value = 0
        record.pay_times = 0
        record.save()
        return record


    def room_report(self, uid):
        if self.user_id == uid:
            self.update(set__report_time_user=datetime.datetime.now())
        else:
            self.update(set__report_time_join=datetime.datetime.now())


    def finish_room(self):





        pass

