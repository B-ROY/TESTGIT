# coding=utf-8

from redis_model.redis_client import *
import json

class GooglePayRedis():
    """
        存储 google play access_token ,
        该access_token可用来查询订单状态
    """
    ___KEY_GOOGLE_PAY_ACCESS_TOKEN__ = "google_pay_access_token"

    @classmethod
    def get_access_token(cls):
        return RQueueClient.getInstance().redis.get(cls.___KEY_GOOGLE_PAY_ACCESS_TOKEN__)

    @classmethod
    def set_access_token(cls, access_token, exptimetime):
        data = {
            "access_token": access_token,
            "exptime": exptimetime
        }
        RQueueClient.getInstance().redis.set(cls.___KEY_GOOGLE_PAY_ACCESS_TOKEN__, json.dumps(data))
