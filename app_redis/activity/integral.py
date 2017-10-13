# coding=utf-8

from redis_model.redis_client import *
import datetime


class Integral(object):

    INTEGRAL_KEY = "integral_key"
    ACTIVITY_START_TIME = datetime.datetime(2017, 10, 13)
    ACTIVITY_END_TIME = datetime.datetime(2017, 11, 12)

    '''
    type = 1 通话积分
    type = 2 礼物积分
    '''
    @classmethod
    def add_integral(cls, user_id, integral, type):
        now_ = datetime.datetime.now()
        if cls.ACTIVITY_START_TIME < now_ < cls.ACTIVITY_END_TIME:
            # 增加总积分
            RQueueClient.getInstance().redis.hincrby(cls.INTEGRAL_KEY, str(user_id), integral)
            # 增加每日积分

            month = now_.month
            day = now_.day
            day_key = cls.INTEGRAL_KEY + str(month) + "_" + str(day) + "_" + str(type)
            RQueueClient.getInstance().redis.hincrby(day_key, str(user_id), integral)

    @classmethod
    def select_integral(cls, user_id):
        # 注意返回值为字符串 或 None
        integral = RQueueClient.getInstance().redis.hget(cls.INTEGRAL_KEY, str(user_id))
        if not integral:
            integral = 0
        return int(integral)

    @classmethod
    def select_integral_one_day(cls, user_id, month, day, type):
        day_key = cls.INTEGRAL_KEY + str(month) + "_" + str(day) + "_" + str(type)
        # 注意返回值为字符串 或 None

        integral = RQueueClient.getInstance().redis.hget(day_key, str(user_id))
        if not integral:
            integral = 0
        return int(integral)