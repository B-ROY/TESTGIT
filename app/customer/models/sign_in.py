#coding=utf-8
from mongoengine import *
import logging
import datetime
from app.customer.models.user import *
from app.customer.models.gift import *
from django.db import models
from base.settings import CHATPAMONGO


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class UserSignIn(Document):

    user_id = IntField(verbose_name=u'用户id', required=True)
    update_time = DateTimeField(verbose_name=u'更新时间', default=None)
    max_date = IntField(verbose_name=u'最大连续签到天数', default=0)
    continuous_date = IntField(verbose_name=u'连续签到天数', default=0)
    sign_date = ListField(DateTimeField(verbose_name=u'签到时间', default=None))

    class Meta:
        app_label = "customer"
        verbose_name = u"签到"
        verbose_name_plural = verbose_name

    def normal_info(self):
        data = {}
        data['id'] = str(self.id)
        data['user_id'] = self.user_id
        data['max_date'] = self.max_date
        data['continuous_date'] = self.continuous_date
        return data

    @classmethod
    def create_user(cls, user_id, now_time):
        try:
            user = UserSignIn(
                user_id=user_id,
                update_time=now_time,
                max_date=1,
                continuous_date=1,
                sign_date=[now_time],
            )
            user.save()

            GiftManager.signin_bill(user_id)

            data = {}
            data["is_sign_in"] = True
            data["experience"] = 30
            data["continuous_date"] = 1
            data["gold"] = 5

        except Exception,e:
            logging.error("create user error:{0}".format(e))
            return False, 10000  # 用户创建失败
        return True, data

    @classmethod
    def user_sign_in(cls, user_id, now_time):
        try:
            user = cls.objects.get(user_id=user_id)
            if user.update_time.strftime('%Y-%m-%d') == now_time.strftime('%Y-%m-%d'):
                data = cls.sign_in_info(user_id)
                data["error_code"] = 10001
                return False, data  # 重复签到
            else:
                user.update_time = now_time
                one_day = datetime.timedelta(days=1)
                con_date = user.sign_date[-1] + one_day

                if con_date.strftime('%Y-%m-%d') == now_time.strftime('%Y-%m-%d'):
                    user.continuous_date += 1
                else:
                    user.continuous_date = 1

                if user.max_date <= user.continuous_date:
                    user.max_date = user.continuous_date
                user.sign_date.append(now_time)
                user.save()

                GiftManager.signin_bill(user_id)

                data = {}
                data["is_sign_in"] = True
                data["gold"] = 5

                con_day = user.continuous_date % 7
                if con_day % 7 == 0:
                    con_day = 7

                data["experience"] = 25 + con_day * 5
                data["continuous_date"] = user.continuous_date

                return True, data
        except UserSignIn.DoesNotExist:
            status, code = UserSignIn.create_user(user_id, now_time)
            return status, code

    @classmethod
    def get_tomorrow_data(cls, user_id):
        try:
            user = cls.objects.get(user_id=user_id)
            data = {}
            con_day = user.continuous_date % 7
            if con_day % 7 == 0:
                con_day = 7
            data["gold"] = 5
            data["experience"] = 30 + con_day * 5

        except Exception,e:
            logging.error("get tomorrow data error:{0}".format(e))
            return False, 10002
        return data, con_day

    @classmethod
    def sign_in_info(cls, user_id):
        try:
            user = cls.objects.filter(user_id=user_id)
            data = {}
            if not user:
                data["is_sign_in"] = False
                data["experience"] = 0
                data["continuous_date"] = 0
                data["gold"] = 0
                return data
            else:
                user = user.first()
                data["gold"] = 5
                con_day = user.continuous_date % 7
                if con_day % 7 == 0:
                    con_day = 7
                data["is_sign_in"] = UserSignIn.check_sign_in(user_id)
                data["experience"] = 25 + con_day * 5
                if UserSignIn.check_sign_in(user_id):
                    data["continuous_date"] = user.continuous_date
                else:
                    now_time = datetime.datetime.now()
                    one_day = datetime.timedelta(days=1)
                    yesterday_time = now_time - one_day
                    if user.update_time.strftime('%Y-%m-%d') == yesterday_time.strftime('%Y-%m-%d'):
                        data["continuous_date"] = user.continuous_date
                    else:
                        data["continuous_date"] = 0
                return data

        except Exception,e:
            logging.error("sign in info error:{0}".format(e))
            return False

    @classmethod
    def check_sign_in(cls, user_id):
        try:
            user = cls.objects.get(user_id=user_id)
            now_time = datetime.datetime.now()
            if user.update_time.strftime('%Y-%m-%d') == now_time.strftime('%Y-%m-%d'):
                return True
            else:
                return False
        except Exception,e:
            logging.error("check sign in error:{0}".format(e))
            return False
