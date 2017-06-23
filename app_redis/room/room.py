# coding=utf-8
import time
import json
from redis_model.redis_client import *


class RoomRedis(object):

    __KEY_PREFIX__ = "room_"

    __KEY_USER_ID__ = "user_id"
    __KEY_JOIN_ID__ = "join_id"
    __KEY_START_TIME__ = "start_time"
    __KEY_BILL_TIME__ = "bill_time"
    @classmethod
    def create_room_record(cls, room_id, user_id, join_id):
        dic = {}
        dic[cls.__KEY_START_TIME__] = int(time.time())
        dic[cls.__KEY_USER_ID__] = user_id
        dic[cls.__KEY_JOIN_ID__] = join_id
        RQueueClient.getInstance().redis.set(cls.__KEY_PREFIX__ + room_id, json.dumps(dic), nx=True)

    @classmethod
    def get_room_record(cls, room_id):
        room_record = RQueueClient.getInstance().redis.get(cls.__KEY_PREFIX__ + room_id)
        return json.loads(room_record)


    @classmethod
    def room_paybill(cls, room_id):
        room_record = RQueueClient.getInstance().redis.get(cls.__KEY_PREFIX__ + room_id)
        room_dic = json.loads(room_record)
        bill_time = room_dic.get(cls.__KEY_BILL_TIME__)
        if bill_time:
            room_dic[cls.__KEY_BILL_TIME__] = int(time.time())
            total_seconds = int(time.time()) - bill_time
            RQueueClient.getInstance().redis.set(cls.__KEY_PREFIX__ + room_id, json.dumps(room_dic), xx=True)
            if total_seconds >= 55:
                return (total_seconds + 5) / 60
            else:
                return 0
        else:
            room_dic[cls.__KEY_BILL_TIME__] = int(time.time())
            RQueueClient.getInstance().redis.set(cls.__KEY_PREFIX__ + room_id, json.dumps(room_dic), xx=True)
            return 1

    @classmethod
    def close_room(cls, room_id):
        RQueueClient.getInstance().redis.delete(cls.__KEY_PREFIX__ + room_id)
