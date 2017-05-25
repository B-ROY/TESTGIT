#coding=utf-8
from mongoengine import *
import logging
import datetime
from app.customer.models.user import *
from app.customer.models.gift import *
from base.settings import CHATPAMONGO


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class ShareInfo(Document):

    SHARE_CHANNEL = [
        (0, u"微信好友"),
        (1, u"朋友圈"),
        (2, u"qq好友"),
        (3, u"qq空间"),
        (4, u"新浪微博"),
    ]

    guid = StringField(verbose_name=u"设备id", max_length=64)
    user_id = IntField(verbose_name=u"用户id")
    share_channel = IntField(verbose_name=u"分享渠道", choices=SHARE_CHANNEL)
    share_time = DateTimeField(verbose_name=u"分享时间", default=datetime.datetime.now())

    class Meta:
        app_label = u"customer"
        verbose_name = u"分享"
        verbose_name_plural = verbose_name

    @classmethod
    def create_shareinfo(cls, guid, user_id, share_channel):
        try:
            userinfo = ShareInfo(guid=guid, user_id=user_id, share_channel=share_channel, share_time=datetime.datetime.now())
            userinfo.save()
            return True
        except Exception,e:
            logging.error("create share info error:{0}".format(e))
            return False

    """
    # 检测设备本周是否分享过
        share_channel 原来分share_channel渠道 现在不分渠道了 只对用户和设备进行检验
    """

    @classmethod
    def check_shareinfo(cls, guid, user_id, share_channel):
        guidinfo = ShareInfo.objects.filter(guid=guid).order_by("-share_time").first()

        if not guidinfo:
            userinfo = ShareInfo.objects.filter(user_id=user_id).order_by("-share_time").first()
            if not userinfo:
                return False
            else:
                now_week = datetime.datetime.now().isocalendar()[1]
                share_week = userinfo.share_time.isocalendar()[1]
                if now_week == share_week:
                    return True
                else:
                    return False
        else:
            now_week = datetime.datetime.now().isocalendar()[1]
            share_week = guidinfo.share_time.isocalendar()[1]
            if now_week == share_week:
                return True
            else:
                return False

class ShareStat(Document):
    SHARE_CHANNEL = [
        (0, u"微信好友"),
        (1, u"朋友圈"),
        (2, u"qq好友"),
        (3, u"qq空间"),
        (4, u"新浪微博"),
    ]
    RESULT_STATUS = [
        (0, u"取消"),
        (1, u"分享成功"),
        (2, u"异常结果")
    ]
    SHARE_USE = [
        (0, u"分享得钱"),
        (1, u"分享邀请好友")
    ]
    guid = StringField(verbose_name=u"设备id", max_length=64)
    user_id = IntField(verbose_name=u"用户id")
    share_channel = IntField(verbose_name=u"分享渠道", choices=SHARE_CHANNEL)
    share_time = DateTimeField(verbose_name=u"分享时间", default=datetime.datetime.now())
    share_use = IntField(verbose_name=u"分享用途", choices=SHARE_USE)
    count = IntField(verbose_name=u"分享次数")
    success_count = IntField(verbose_name=u"分享成功次数")

    @classmethod
    def create_invite_shareinfo(cls, guid, user_id, share_channel, share_use, count, success_count):
        try:
            invite_shareinfo = cls(guid=guid, user_id=user_id, share_channel=share_channel,
                                   share_time=datetime.datetime.now(), share_use=share_use,
                                   count=count, success_count=success_count)
            invite_shareinfo.save()
            return True
        except Exception, e:
            logging.error("create share info error:{0}".format(e))
            return False


