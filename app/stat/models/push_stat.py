# coding=utf-8

from mongoengine import *


class PushStat(Document):
    msg_id = StringField(verbose_name=u"对应的MsgRule的id", unique=True)

    android_num = IntField(verbose_name=u"android推送总数量")
    ios_num = IntField(verbose_name=u"ios推送总量")
    android_rec_anchor = IntField(verbose_name=u"Android播主接收数量")
    android_rec_user = IntField(verbose_name=u"Android用户收到的数量")
    android_click_anchor = IntField(verbose_name=u"Android主播点击数量")
    android_click_user = IntField(verbose_name=u"Android用户点击的数量")

    ios_rec_anchor = IntField(verbose_name=u"IOS播主接收数量")
    ios_rec_user = IntField(verbose_name=u"IOS用户接收的数量")
    ios_click_anchor = IntField(verbose_name=u"点击数量")
    ios_click_user = IntField(verbose_name=u"ios点击的数量")

