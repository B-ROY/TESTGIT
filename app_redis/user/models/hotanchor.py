# coding=utf-8

from redis_model.redis_client import *


class HotAnchorRedis():

    __KEY_HOT_ANCHOR = "hotanchor"

    @classmethod
    def pop_hot_anchor(cls):
        return RQueueClient.getInstance().redis.lpop(cls.__KEY_HOT_ANCHOR)


    @classmethod
    def push_hot_anchor(cls, id_list):
        a = RQueueClient.getInstance().redis.rpush(cls.__KEY_HOT_ANCHOR, *id_list)
        print a
        return a
