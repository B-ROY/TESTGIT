# coding=utf-8

from redis_model.redis_client import *


class UserRedis():

    __KEY_USER_ID = "user_id"
    __KEY_USER_IDENTITY = "user_identity"

    @classmethod
    def pop_user_id(cls):
        return RQueueClient.getInstance().redis.lpop(cls.__KEY_USER_ID)

    @classmethod
    def pop_user_identity(cls):
        return RQueueClient.getInstance().redis.lpop(cls.__KEY_USER_IDENTITY)

    @classmethod
    def push_user_id(cls, id_list):
        a = RQueueClient.getInstance().redis.rpush(cls.__KEY_USER_ID, *id_list)
        print a
        return a

    @classmethod
    def push_user_identity(cls, identity_list):
        a = RQueueClient.getInstance().redis.rpush(cls.__KEY_USER_IDENTITY, *identity_list)
        print a
        return a

