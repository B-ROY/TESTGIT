# coding=utf-8


from mongoengine import *


class DevInfoMatch(Document):


    model = StringField(verbose_name=u"手机型号")
    platform = IntField(verbose_name=u"平台") # 0.Android 1. IOS
    osver = StringField(verbose_name=u"操作系统版本号")
    ip = StringField(verbose_name=u"登录ip")
    visit_time = DateTimeField(verbose_name=u"访问推广页面时间")
    user_id = IntField(verbose_name=u"分享用户的id")
