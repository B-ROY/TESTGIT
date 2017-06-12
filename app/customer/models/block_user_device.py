# coding=utf-8
from django.db import models
import logging
from mongoengine import *
from base.settings import CHATPAMONGO
import datetime
from app.customer.models.user import User


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


class BlockUserRecord(Document):

    block_date = DateTimeField(verbose_name=u"封号日期")
    block_user_id = StringField(verbose_name=u"被封号者的昵称")
    block_user_dev = StringField(verbose_name=u"被封号者的设备")

    @classmethod
    def get_block_list(cls, last_day):
        return cls.objects.filter(block_date__lt=last_day)[0:7]

    @classmethod
    def write_record_daily(cls):
        today = datetime.datetime.today()

        yesterday = datetime.datetime.today() - datetime.timedelta(days=1)

        block_record = BlockUserDev.objects.filter(block_start__gte=yesterday, block_start__lt=today, status__ne=3)
        if block_record:
            block_user_daily_record = cls()
            block_user_daily_record.block_date = yesterday  # yesterday
            id_record = ""
            dev_record = ""
            for record in block_record:
                block_user = User.objects.get(id=record.block_user)
                if record.block_type == 1:
                    id_record += block_user.nickname + ","
                elif record.block_type == 2:
                    dev_record += block_user.nickname + ","

            block_user_daily_record.block_user_id = id_record[0:-1]
            block_user_daily_record.block_user_dev = dev_record[0:-1]
            block_user_daily_record.save()

    @classmethod
    def write_record_all(cls):
        today = datetime.datetime.today()

        yesterday = datetime.datetime.today()-datetime.timedelta(days=1)

        first_block_user_dev = BlockUserDev.objects.filter(status__ne=3).order_by("created_time").first()

        first_day = first_block_user_dev.created_time

        first_day = datetime.datetime(year=first_day.year, month=first_day.month, day=first_day.day)

        d = first_day
        while d < today+datetime.timedelta(days=1):
            next_day = d + datetime.timedelta(days=1)
            block_record = BlockUserDev.objects.filter(created_time__gte=d, created_time__lt=next_day, status__ne=3)

            #block_record = BlockUserDev.objects.filter(block_start__gte=yesterday, block_start__lt=today, status__ne=3)
            if block_record:
                block_user_daily_record = cls()
                block_user_daily_record.block_date = d#yesterday
                id_record = ""
                dev_record = ""
                for record in block_record:
                    block_user = User.objects.get(id=record.block_user)
                    if record.block_type == 1:
                        id_record += block_user.nickname + ","
                    elif record.block_type == 2:
                        dev_record += block_user.nickname + ","

                block_user_daily_record.block_user_id = id_record[0:-1]
                block_user_daily_record.block_user_dev = dev_record[0:-1]

                block_user_daily_record.save()
            d = next_day








