# coding=utf-8

from redis_model.redis_client import *


class UserRedis():

    __KEY_USER_ID = "user_id"
    __KEY_USER_IDENTITY = "user_identity"
    __KEY_USER_LOGIN = "user_login"

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

    @classmethod
    def set_user_login(cls,userid,value):
        RQueueClient.getInstance().redis.set(cls.__KEY_USER_LOGIN+"_"+userid,value)

    @classmethod
    def remove_user_login(cls,userid):
        return RQueueClient.getInstance().redis.delete(cls.__KEY_USER_LOGIN+"_"+userid)

    @classmethod
    def get_user_login(cls,userid):
        RQueueClient.getInstance().redis.get(cls.__KEY_USER_LOGIN+"_"+userid)
