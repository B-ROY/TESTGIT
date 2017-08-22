# coding=utf-8

from django.db import models
import logging
import datetime
from wi_model_util.imodel import *
from mongoengine import *
from base.settings import CHATPAMONGO
from app.customer.models.vip import UserVip
from app.customer.models.community import UserMoment

connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class PrivateVideo(Document):

    user_id = IntField(verbose_name=u"用户id")
    cover_url = StringField(verbose_name=u"封面照片地址", max_length=256)
    video_url = StringField(verbose_name=u"视频地址", max_length=256)
    desc = StringField(verbose_name=u"视频描述", max_length=256)
    price = IntField(verbose_name=u"视频价格")
    create_time = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())
    delete_status = IntField(verbose_name=u"是否删除")  # 1:不删除 2:删除
    show_status = IntField(verbose_name=u"鉴黄显示状态")  # 1:展示 2:数美屏蔽 3:鉴定中
    is_valid = IntField(verbose_name=u"是否忽略(cms使用)", default=1)  # 1.不忽略 2.忽略

    class Meta:
        app_label = "customer"
        verbose_name = u"私房视频"
        verbose_name_plural = verbose_name

    @classmethod
    def delete_video(cls, video_id, user_id):
        video = PrivateVideo.objects.filter(id=video_id).first()
        try:
            if video:
                if int(video.user_id) == int(user_id):
                    video.update(set__delete_status=2)
                    user_moment = UserMoment.objects.filter(video_id=video_id).first()
                    if user_moment:
                        user_moment.update(set__delete_status=2)
            else:
                return False
        except Exception,e:
            logging.error("delete video error:{0}".format(e))
            return False
        return True

    @classmethod
    def check_video_count(cls, user):
        # 私房视频限制相关
        videos_vip_count = 0
        videos_anchor_vip_count = 20
        videos_anchor_count = 10
        videos_user_count = 0
        videos_used_count = PrivateVideo.objects.filter(user_id=user.id, delete_status=1, show_status__ne=2).count()

        is_video = user.is_video_auth
        user_vip = UserVip.objects.filter(user_id=user.id).first()

        code = 1
        message = ""
        if user_vip:
            if int(is_video) == 1:
                # 播住vip
                if videos_used_count >= videos_anchor_vip_count:
                    code = 2
                    message = u"播主VIP,私房视频最多15条"
            else:
                # 用户vip
                if videos_used_count >= videos_vip_count:
                    code = 2
                    message = u"用户VIP,不能发私房视频"
        else:
            if int(is_video) == 1:
                # 播主:
                if videos_used_count >= videos_anchor_count:
                    code = 2
                    message = u"播主私房视频最多10条"
            else:
                # 普通用户
                if videos_used_count >= videos_user_count:
                    code = 2
                    message = u"普通用户不能发私房视频"

        print message
        return code, message


class PrivateVideoPrice(Document):
    price = IntField(verbose_name=u"视频价格")
    only_vip = IntField(verbose_name=u"vip才可设置")  # 1: 是  2:否
    delete_status = IntField(verbose_name=u"是否删除")  # 1:不删除 2:删除

    class Meta:
        app_label = "customer"
        verbose_name = u"私房视频价格"
        verbose_name_plural = verbose_name


class VipWatchVideoRecord(Document):
    user_id = IntField(verbose_name=u"用户id")
    create_time = StringField(verbose_name=u"观看日期", max_length=64)
    video_id = StringField(verbose_name=u"视频id", max_length=64)

    @classmethod
    def create_record(cls, video_id, user_id):
        now = datetime.datetime.now()
        create_time = now.strftime("%Y-%m-%d")
        try:
            record = VipWatchVideoRecord.objects.filter(user_id=user_id, video_id=video_id, create_time=create_time).first()
            if not record:
                record = VipWatchVideoRecord()
                record.user_id = user_id
                record.create_time = create_time
                record.video_id = video_id
                record.save()
        except Exception,e:
            logging.error("create vip watch video record error:{0}".format(e))
            return False
        return True


class VideoPurchaseRecord(Document):
    user_id = IntField(verbose_name=u"用户id")
    video_id = StringField(verbose_name=u"视频id", max_length=64)
    create_time = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())

    @classmethod
    def create_record(cls, user_id, video_id):
        record = VideoPurchaseRecord()
        record.user_id = user_id
        record.video_id = video_id
        record.create_time = datetime.datetime.now()
        record.save()

    @classmethod
    def get_buy_status(cls, user_id, video_id):
        buy_video_status = 2
        record = VideoPurchaseRecord.objects.filter(user_id=user_id, video_id=video_id).first()
        if record:
            buy_video_status = 1
        return buy_video_status


class InviteMessage(Document):
    from_user_id = IntField(verbose_name=u"用户id")
    to_user_id = IntField(verbose_name=u"被邀请用户id")
    type = IntField(verbose_name=u"邀请类型")
    create_time = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())

    @classmethod
    def create_invite_message(cls, from_user_id, to_user_id, type):
        obj_ = cls()
        obj_.from_user_id = from_user_id
        obj_.to_user_id = to_user_id
        obj_.type = type
        obj_.create_time = datetime.datetime.now()
        obj_.save()




