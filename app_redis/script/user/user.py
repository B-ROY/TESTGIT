# coding=utf-8

from app_redis.user.models.user import UserRedis
from app.genLuckNumber import gen_luck_number

class UserRedisScript:

    @classmethod
    def push_user_id(cls):
        """
            push user_id into redis
            key: "user_id"
        """
        user_redis = UserRedis()
        id_list = range(1, 300011)

        user_redis.push_user_id(id_list)

    @classmethod
    def push_user_identity(cls):
        """
        push user_identity into redis
        key : "user_identity"


        """
        user_redis = UserRedis()
        identity_list = gen_luck_number()
        user_redis.push_user_identity(identity_list=identity_list)