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

    __KEY_RECOMMEND_ID_V3 = "user_recommed_id_v3"
    __KEY_RECOMMEND_ID_ALL = "user_recommed_id_all"
    __KEY_RECOMMEND_V3 = "user_recommed_v3"
    __KEY_ANCHOR_ID_V3 = "index_anchor_id_v3"
    __KEY_ANCHOR_ID_ALL = "index_anchor_id_all"
    __KEY_ANCHOR_V3 = "index_anchor_v3"

    __KEY_RECOMMEND_ID_pure = "user_recommed_id_pure"
    __KEY_RECOMMEND_ID_ALL_pure = "user_recommed_id_all_pure"
    __KEY_RECOMMEND_pure = "user_recommed_pure"
    __KEY_ANCHOR_ID_pure = "index_anchor_id_pure"
    __KEY_ANCHOR_ID_ALL_pure = "index_anchor_id_all_pure"
    __KEY_ANCHOR_pure = "index_anchor_pure"

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



    @classmethod
    def add_user_recommed_id_v3(cls,userids):
        RQueueClient.getInstance().redis.rpush(cls.__KEY_RECOMMEND_ID_V3,*userids)

    @classmethod
    def add_user_recommed_id_pure(cls,userids):
        RQueueClient.getInstance().redis.rpush(cls.__KEY_RECOMMEND_ID_pure,*userids)

    @classmethod
    def add_user_recommed_id_all(cls,userids):
        RQueueClient.getInstance().redis.rpush(cls.__KEY_RECOMMEND_ID_ALL,*userids)

    @classmethod
    def add_user_recommed_id_all_pure(cls,userids):
        RQueueClient.getInstance().redis.rpush(cls.__KEY_RECOMMEND_ID_ALL_pure,*userids)
    @classmethod
    def add_user_recommed_v3(cls,usermap):
        RQueueClient.getInstance().redis.set(cls.__KEY_RECOMMEND_V3,usermap)

    @classmethod
    def add_user_recommed_pure(cls,usermap):
        RQueueClient.getInstance().redis.set(cls.__KEY_RECOMMEND_pure,usermap)

    @classmethod
    def get_recommed_list_v3(cls):
        return  RQueueClient.getInstance().redis.lrange(cls.__KEY_RECOMMEND_ID_V3,0,-1)
    @classmethod
    def get_recommed_list_pure(cls):
        return  RQueueClient.getInstance().redis.lrange(cls.__KEY_RECOMMEND_ID_pure,0,-1)

    @classmethod
    def get_recommed_list_all(cls):
        return RQueueClient.getInstance().redis.lrange(cls.__KEY_RECOMMEND_ID_ALL, 0, -1)
    @classmethod
    def get_recommed_list_all_pure(cls):
        return RQueueClient.getInstance().redis.lrange(cls.__KEY_RECOMMEND_ID_ALL_pure, 0, -1)

    @classmethod
    def get_recommed_v3(cls):
        return RQueueClient.getInstance().redis.get(cls.__KEY_RECOMMEND_V3)
    @classmethod
    def get_recommed_pure(cls):
        return RQueueClient.getInstance().redis.get(cls.__KEY_RECOMMEND_pure)

    @classmethod
    def delete_user_recommed_id_v3(cls):
        RQueueClient.getInstance().redis.delete(cls.__KEY_RECOMMEND_ID_V3)

    @classmethod
    def delete_user_recommed_id_pure(cls):
        RQueueClient.getInstance().redis.delete(cls.__KEY_RECOMMEND_ID_pure)
    @classmethod
    def delete_user_recommed_id_all(cls):
        RQueueClient.getInstance().redis.delete(cls.__KEY_RECOMMEND_ID_ALL)
    @classmethod
    def delete_user_recommed_id_all_pure(cls):
        RQueueClient.getInstance().redis.delete(cls.__KEY_RECOMMEND_ID_ALL_pure)
    @classmethod
    def delete_user_recommed_v3(cls):
        RQueueClient.getInstance().redis.delete(cls.__KEY_RECOMMEND_V3)
    @classmethod
    def delete_user_recommed_pure(cls):
        RQueueClient.getInstance().redis.delete(cls.__KEY_RECOMMEND_pure)


    # // added by biwei
    @classmethod
    def delete_user_recommed_id_v3_one(cls, _id):
        RQueueClient.getInstance().redis.lrem(cls.__KEY_RECOMMEND_ID_V3, _id)
        RQueueClient.getInstance().redis.lrem(cls.__KEY_ANCHOR_ID_V3, _id)

    @classmethod
    def delete_index_anchor_id_v3_one(cls, _id):
        RQueueClient.getInstance().redis.lrem(cls.__KEY_RECOMMEND_ID_ALL, _id)
    @classmethod
    def add_user_recommed_id_v3_one(cls, _id):
        #
        hot_list_all = cls.get_recommed_list_all()
        anchor_list_all = cls.get_index_anchor_list_all(0, -1)

        hot_list = cls.get_recommed_list_v3()
        anchor_list = cls.get_index_anchor_list_v3(0,-1)

        if str(_id) in hot_list_all and str(_id) not in hot_list:
            index = hot_list_all.index(str(_id))
            print index
            if index == 0:
                RQueueClient.getInstance().redis.lpush(cls.__KEY_RECOMMEND_ID_V3, _id)
            else:
                v = hot_list_all[index-1]
                RQueueClient.getInstance().redis.linsert(cls.__KEY_RECOMMEND_ID_V3, "after", v, _id)

        elif str(_id) in anchor_list_all and str(_id) not in anchor_list:
            index = anchor_list_all.index(str(_id))
            if index == 0:
                RQueueClient.getInstance().redis.lpush(cls.__KEY_ANCHOR_ID_V3, _id)
            else:
                v = anchor_list_all[index-1]
                RQueueClient.getInstance().redis.linsert(cls.__KEY_ANCHOR_ID_V3, "after", v, _id)

    # //

    @classmethod
    def add_index_id_v3(cls,userids):
        RQueueClient.getInstance().redis.rpush(cls.__KEY_ANCHOR_ID_V3,*userids)

    @classmethod
    def add_index_id_pure(cls,userids):
        RQueueClient.getInstance().redis.rpush(cls.__KEY_ANCHOR_ID_pure,*userids)

    @classmethod
    def add_index_id_all(cls,userids):
        RQueueClient.getInstance().redis.rpush(cls.__KEY_ANCHOR_ID_ALL,*userids)

    @classmethod
    def add_index_id_all_pure(cls,userids):
        RQueueClient.getInstance().redis.rpush(cls.__KEY_ANCHOR_ID_ALL_pure,*userids)
    @classmethod
    def add_index_anchor_v3(cls,usermap):
        RQueueClient.getInstance().redis.set(cls.__KEY_ANCHOR_V3,usermap)
    @classmethod
    def add_index_anchor_pure(cls,usermap):
        RQueueClient.getInstance().redis.set(cls.__KEY_ANCHOR_pure,usermap)

    @classmethod
    def delete_index_anchor_id_v3(cls):
        RQueueClient.getInstance().redis.delete(cls.__KEY_ANCHOR_ID_V3)
    @classmethod
    def delete_index_anchor_id_pure(cls):
        RQueueClient.getInstance().redis.delete(cls.__KEY_ANCHOR_ID_pure)
    @classmethod
    def delete_index_anchor_id_all(cls):
        RQueueClient.getInstance().redis.delete(cls.__KEY_ANCHOR_ID_ALL)
    @classmethod
    def delete_index_anchor_id_all_pure(cls):
        RQueueClient.getInstance().redis.delete(cls.__KEY_ANCHOR_ID_ALL_pure)
    @classmethod
    def delete_index_anchor_v3(cls):
        RQueueClient.getInstance().redis.delete(cls.__KEY_ANCHOR_V3)
    @classmethod
    def delete_index_anchor_pure(cls):
        RQueueClient.getInstance().redis.delete(cls.__KEY_ANCHOR_pure)

    @classmethod
    def get_index_anchor_list_v3(cls,pageindex,offset):
        return RQueueClient.getInstance().redis.lrange(cls.__KEY_ANCHOR_ID_V3, pageindex, offset)
    @classmethod
    def get_index_anchor_list_pure(cls,pageindex,offset):
        return RQueueClient.getInstance().redis.lrange(cls.__KEY_ANCHOR_ID_pure, pageindex, offset)

    @classmethod
    def get_index_anchor_list_all(cls, pageindex, offset):
        return RQueueClient.getInstance().redis.lrange(cls.__KEY_ANCHOR_ID_ALL, pageindex, offset)
    @classmethod
    def get_index_anchor_list_all_pure(cls, pageindex, offset):
        return RQueueClient.getInstance().redis.lrange(cls.__KEY_ANCHOR_ID_ALL_pure, pageindex, offset)

    @classmethod
    def get_index_anchor_v3(cls):
        return RQueueClient.getInstance().redis.get(cls.__KEY_ANCHOR_V3)
    @classmethod
    def get_index_anchor_pure(cls):
        return RQueueClient.getInstance().redis.get(cls.__KEY_ANCHOR_pure)

    '''
        判断用户是否为目标用户 判断标准为充值是否大于200
        1. 首页接口 用户列表 根据是否是目标用户吐不同数据
        2. 在充值接口判断 如果充值大于200 则判定为目标用户
        
        
    '''
    __KEY_TARGET_USER__ = "key_target_user"

    @classmethod
    def add_target_user(cls, user_id):
        return RQueueClient.getInstance().redis.sadd(cls.__KEY_TARGET_USER__, user_id)

    @classmethod
    def is_target_user(cls, user_id):
        return RQueueClient.getInstance().redis.sismember(cls.__KEY_TARGET_USER__, str(user_id))

    '''
        返回删除的数量 如果返回值为0:q
         则user_id不再列表中
    '''
    @classmethod
    def delete_target_user(cls, user_id):
        # 暂时没有删除逻辑
        return RQueueClient.getInstance().redis.srem(cls.__KEY_TARGET_USER__, str(user_id))

    __KEY__PURE_ANCHOR = "key_pure_anchor"

    @classmethod
    def add_pure_anchor(cls, user_id):
        return RQueueClient.getInstance().redis.sadd(cls.__KEY__PURE_ANCHOR, user_id)

    @classmethod
    def is_pure_anchor(cls, user_id):
        return RQueueClient.getInstance().redis.sismember(cls.__KEY__PURE_ANCHOR, str(user_id))

    '''
        返回删除的数量 如果返回值为0:q
         则user_id不再列表中
    '''

    @classmethod
    def delete_pure_anchor(cls, user_id):
        # 暂时没有删除逻辑
        return RQueueClient.getInstance().redis.srem(cls.__KEY__PURE_ANCHOR, str(user_id))


















