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
    join_ip = StringField(verbose_name=u"加入者ip")

    dial_back_status = IntField(verbose_name=u"回拨状态")  # 1:可回拨  2:已回拨  3:取消回拨
    dial_back_time = DateTimeField(verbose_name=u"回拨时间")
    is_dial_back = IntField(verbose_name=u"是否是回拨房间(回拨之后房间)")  # 0:否  1:是

    is_show = IntField(verbose_name=u"通话记录是否展示")  # 0:否  1:是

    @classmethod
    def create_room_reocord(cls, user_id, join_id, price, room_type, join_ip, dial_back_status=None, dial_back_time=None, is_dial_back=0):

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

        record.join_ip = join_ip

        record.dial_back_status = dial_back_status
        record.dial_back_time = dial_back_time
        record.is_dial_back = is_dial_back
        record.is_show = 1
        record.save()
        return record

    def finish_room(self, end_type):
        if self.room_status == 2:
            return
        end_time = datetime.datetime.now()
        self.update(set__room_status=2, set__end_type=end_type, set__end_time=end_time)
        room_user = User.objects.get(id=self.user_id)
        join_user = User.objects.get(id=self.join_id)
        if room_user.last_room_id == str(self.id):
            room_user.update(set__audio_status=2)
        if join_user.last_room_id == str(self.id):
            join_user.update(set__audio_status=2)

        if room_user.is_video_auth == 1:
            UserRedis.add_user_recommed_id_v3_one(self.user_id)

        # 判断回呼
        if end_type in [1, 3, 6]:
            if self.is_answer == 2 and self.room_type == 1:
                user_id = self.user_id
                join_id = self.join_id
                records = RoomRecord.objects.filter(user_id=user_id, join_id=join_id, dial_back_status=1)
                if records:
                    for record in records:
                        record.update(set__dial_back_status=3)

                self.update(set__dial_back_status=1)

    @classmethod
    def get_records(cls, user_id, page, page_count):
        records = cls.objects.filter(user_id=user_id, is_show=1, room_type=1).order_by("-create_time")[(page - 1) * page_count:page * page_count]
        return records

    @classmethod
    def get_timestamp(cls, date_time):
        temp_time = date_time.strftime("%Y-%m-%d %H:%M:%S")
        timeArray = time.strptime(temp_time, "%Y-%m-%d %H:%M:%S")
        timestamp = time.mktime(timeArray)
        return int(timestamp)

    @classmethod
    def get_type(cls, record):
        dial_type = 1
        if record.dial_back_status == 1:
            dial_type = 3
        if record.end_type == 5:
            dial_type = 2
        if record.end_type == 1:
            dial_type = 3
        return dial_type

    @classmethod
    def get_time_len_str(cls, start_time, end_time):
        seconds = (end_time - start_time).total_seconds()/60
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        time_str = ("%02d:%02d:%02d" % (h, m, s))
        return time_str

    @classmethod
    def clear_user_call_record(cls, user_id, record_id):
        last_record = cls.objects.filter(id=record_id).first()
        records = cls.objects.filter(user_id=user_id, create_time__lte=last_record.create_time)
        if records:
            for record in records:
                record.update(set__is_show=0)
