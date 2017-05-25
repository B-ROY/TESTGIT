#coding=utf-8
from mongoengine import *
import logging
import datetime
import time
from base.core.util.dateutils import datetime_to_timestamp
from app.customer.models.user import *
from django.db import models
from base.settings import CHATPAMONGO

connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username, password=CHATPAMONGO.password)


class ChildUserInfo(Document):

    user_id = IntField(verbose_name=u'用户id', required=True)
    room_id = StringField(verbose_name=u'房间id', max_length=256, default=None)
    total_time = IntField(verbose_name=u'总时长(秒)', default=0)
    total_income = IntField(verbose_name=u'总收入', default=0)
    total_rate = IntField(verbose_name=u'总评分', default=0)
    total_amount = IntField(verbose_name=u'总订单数', default=0)
    update_time = DateTimeField(verbose_name=u'更新时间', default=None)
    listen_url = StringField(verbose_name=u'试听url', max_length=256, default="")
    now_price = IntField(verbose_name=u'当前价格', required=True)
    private_id = StringField(verbose_name=u'私密照片集', default="")

    class Meta:
        app_label = "audio"
        verbose_name = u"语音"
        verbose_name_plural = verbose_name

    def normal_info(self):
        data = {}
        data['id'] = str(self.id)
        data['user_id'] = self.user_id
        data['room_id'] = self.room_id
        data['total_time'] = self.total_time
        data['total_income'] = self.total_income
        data['total_rate'] = self.total_rate
        data['total_amount'] = self.total_amount
        data['update_time'] = datetime_to_timestamp(self.update_time)
        data['listen_url'] = self.listen_url
        data['now_price'] = self.now_price
        return data


class ChildAudioRecord(Document):

    STATUS = [
        (0, u'未挂单'),
        (1, u'挂单中'),
        (2, u'正在通话'),
        (3, u'有用户打入'),
        (4, u'离线'),
    ]

    user_id = IntField(verbose_name=u'用户id', required=True)
    join_id = IntField(verbose_name=u'加入者id', default=None)
    open_time = DateTimeField(verbose_name=u'挂单开始时间', default=None)
    start_time = DateTimeField(verbose_name=u'通话开始时间', default=None)
    end_time = DateTimeField(verbose_name=u'结束时间', default=None)
    report_user = DateTimeField(verbose_name=u'用户上报时间', default=None)
    report_join = DateTimeField(verbose_name=u'加入者上报时间', default=None)
    status = IntField(verbose_name=u'当前状态', default=0, choices=STATUS)
    now_price = IntField(verbose_name=u'当前价格', default=0)
    spend = IntField(verbose_name=u'礼物数目', default=0)
    listen_url = StringField(verbose_name=u'试听url', max_length=256, default="")
    pay_times = IntField(verbose_name=u'实际扣费次数')

    class Meta:
        app_label = "audio"
        verbose_name = u"记录"
        verbose_name_plural = verbose_name

    def normal_info(self):
        data = {}
        data['id'] = str(self.id)
        data['user_id'] = self.user_id
        data['join_id'] = self.join_id
        data['open_time'] = datetime_to_timestamp(self.open_time)
        data['start_time'] = datetime_to_timestamp(self.start_time)
        data['end_time'] = datetime_to_timestamp(self.end_time)
        data['report_user'] = datetime_to_timestamp(self.report_user)
        data['report_join'] = datetime_to_timestamp(self.report_join)
        data['status'] = self.status
        data['now_price'] = self.now_price
        data['spend'] = self.spend
        data['listen_url'] = self.listen_url
        return data

    @classmethod
    def create_child_audio(cls, user_identity, audio_price, listen_url, audio_status):
        try:
            user = User.objects.get(identity=user_identity)
            try:
                child_audio = cls.objects.get(user_id=user.id)
                child_audio.open_time = datetime.datetime.now()
                child_audio.now_price = audio_price
                child_audio.listen_url = listen_url
                child_audio.status = audio_status
                child_audio.save()

                child_user_info = ChildUserInfo.objects.get(user_id=user.id)
                child_user_info.now_price = audio_price
                child_user_info.update_time = datetime.datetime.now()
                child_user_info.listen_url = listen_url
                child_user_info.save()
                return True

            except ChildAudioRecord.DoesNotExist:
                child_audio = ChildAudioRecord(
                    user_id=user.id,
                    open_time=datetime.datetime.now(),
                    status=audio_status,
                    now_price=audio_price,
                    spend=0,
                    listen_url=listen_url,
                    pay_times=0
                )
                child_audio.save()

                child_user_info = ChildUserInfo(
                    user_id=user.id,
                    room_id=str(child_audio.id),
                    total_time=0,
                    total_income=0,
                    total_rate=0,
                    total_amount=0,
                    update_time=datetime.datetime.now(),
                    listen_url=listen_url,
                    now_price=audio_price
                )
                child_user_info.save()
                return True
        except Exception,e:
            logging.error("create child audio error:{0}".format(e))
            return False

    @classmethod
    def update_child_audio(cls, user_identity, audio_price, listen_url, audio_status):
        user = User.objects.get(identity=user_identity)

        child_audio = cls.objects.get(user_id=user.id)
        child_audio.open_time = datetime.datetime.now()
        child_audio.now_price = audio_price
        child_audio.listen_url = listen_url
        child_audio.status = audio_status
        child_audio.save()

        child_user_info = ChildUserInfo.objects.get(user_id=user.id)
        child_user_info.now_price = audio_price
        child_user_info.update_time = datetime.datetime.now()
        child_user_info.listen_url = listen_url
        child_user_info.save()
        return True

    @classmethod
    def close_child_audio(cls, record_id):
        child_audio = cls.objects.get(id=record_id)
        child_audio.status = 4
        child_audio.save()
        return True

    @classmethod
    def get_online_users(cls, page=1, page_count=5):
        users = cls.objects(status__gt=0, status__lt=4).order_by('-open_time')[(page-1)*page_count:page*page_count]
        return users
