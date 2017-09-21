# coding=utf-8


from mongoengine import *
import datetime

class DevInfoMatch(Document):


    model = StringField(verbose_name=u"手机型号")
    platform = IntField(verbose_name=u"平台") # 0.Android 1. IOS
    osver = StringField(verbose_name=u"操作系统版本号")
    ip = StringField(verbose_name=u"登录ip")
    visit_time = DateTimeField(verbose_name=u"访问推广页面时间")
    has_match = IntField(verbose_name=u"是否已经匹配")# 0:未匹配 1:已匹配
    user_id = IntField(verbose_name=u"分享用户的id")
    invite_ret_code = IntField(verbose_name=u"是否邀请成功")
    city = StringField(verbose_name=u"")

    @classmethod
    def add_dev_info_match(cls, model, platform, osver, ip, user_id):
        dev_info = cls.objects.filter(model=model, platform=platform, osver=osver, ip=ip).first()
        if not dev_info:
            dev_info = DevInfoMatch(model=model, osver=osver, platform=platform,
                                    visit_time=datetime.datetime.now(), user_id=user_id, ip=ip, has_match=0)
            dev_info.save()

    @classmethod
    def match_dev_info(cls, model, platform, osver, ip):
        dev_infos = DevInfoMatch.objects.filter(model=model, osver=osver, platform=platform, has_match=0)
        if dev_infos:
            for dev_info in dev_infos:
                if ip == dev_info.ip:
                    dev_info.update(set__has_match=1)
                    return dev_info
                else:
                    # todo ip可能会有wifi和移动网络的区别 可根据ip库判断地域 再加上时间判断

                    pass
        return None



