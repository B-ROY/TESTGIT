# coding=utf-8

from redis_model.redis_client import *


class UserRedis():

    __KEY_USER_ID = "user_id"
    __KEY_USER_IDENTITY = "user_identity"
    __KEY_USER_LOGIN = "user_login"
    __KEY_RECOMMEND_ID = "user_recommed_id"
    __KEY_RECOMMEND = "user_recommed"
    __KEY_ANCHOR_ID = "index_anchor_id"
    __KEY_ANCHOR = "index_anchor"

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
        RQueueClient.getInstance().redis.delete(cls.__KEY_USER_LOGIN+"_"+userid)
        a =RQueueClient.getInstance().redis.get(cls.__KEY_USER_LOGIN+"_"+userid)

    @classmethod
    def get_user_login(cls,userid):
        a =RQueueClient.getInstance().redis.get(cls.__KEY_USER_LOGIN+"_"+userid)
        return a

    @classmethod
    def add_user_recommed_id(cls,userids):
        RQueueClient.getInstance().redis.rpush(cls.__KEY_RECOMMEND_ID,*userids)

    @classmethod
    def add_user_recommed(cls,usermap):
        RQueueClient.getInstance().redis.set(cls.__KEY_RECOMMEND,usermap)

    @classmethod
    def get_recommed_list(cls):
        return  RQueueClient.getInstance().redis.lrange(cls.__KEY_RECOMMEND_ID,0,-1)

    @classmethod
    def get_recommed(cls):
        return RQueueClient.getInstance().redis.get(cls.__KEY_RECOMMEND)

    @classmethod
    def delete_user_recommed_id(cls):
        RQueueClient.getInstance().redis.delete(cls.__KEY_RECOMMEND_ID)
    @classmethod
    def delete_user_recommed(cls):
        RQueueClient.getInstance().redis.delete(cls.__KEY_RECOMMEND)

    @classmethod
    def add_index_id(cls,userids):
        RQueueClient.getInstance().redis.rpush(cls.__KEY_ANCHOR_ID,*userids)

    @classmethod
    def add_index_anchor(cls,usermap):
        RQueueClient.getInstance().redis.set(cls.__KEY_ANCHOR,usermap)

    @classmethod
    def delete_index_anchor_id(cls):
        RQueueClient.getInstance().redis.delete(cls.__KEY_ANCHOR_ID)
    @classmethod
    def delete_index_anchor(cls):
        RQueueClient.getInstance().redis.delete(cls.__KEY_ANCHOR)

    @classmethod
    def get_index_anchor_list(cls,pageindex,offset):
        return RQueueClient.getInstance().redis.lrange(cls.__KEY_ANCHOR_ID, pageindex, offset)

    @classmethod
    def get_index_anchor(cls):
        return RQueueClient.getInstance().redis.get(cls.__KEY_ANCHOR)