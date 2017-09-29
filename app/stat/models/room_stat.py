# coding=utf-8

from mongoengine import *


class AgoraErrorStat(Document):

    ERROR_ACTION = [
        (1, "signal登录"),
        (2, "signal呼叫"),
        (0, "siganl加房"),
        (0, "signal退房"),
        (0, "signal"),
        (10, "media onError")
    ]

    erorr_action = IntField(verbose_name=u"错误类型")
    room_id = StringField(verbose_name=u"房间号")
    error_code = IntField(verbose_name=u"错误码")
    error_desc = IntField(verbose_name=u"错误描述")
    occur_time = DateTimeField(verbose_name=u"发生错误时间")
    user_id = IntField(verbose_name=u"用户id")


"""
    房间结束后 声网房间数据统计
"""
class RoomDataStat(Document):
    user_id = IntField(verbose_name=u"用户id")
    room_id = StringField(verbose_name=u"房间id")
    stat_data = StringField(verbose_name=u"房间数据统计")




