# coding=utf-8

import datetime
import logging

from base.settings import CHATPAMONGO
from django.conf import settings
from mongoengine import *
from api.handler.thridpard.qcloud.im import *
from app.customer.models.follow_user import *


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)

#  黑名单
class BlackUser(Document):

    from_id = IntField(verbose_name=u'用户id', required=True)
    to_id = IntField(verbose_name=u'黑名单用户_id', required=True)
    create_time = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())

    # 添加黑名单, mongo单向保存
    @classmethod
    def black_add(cls, from_user, to_user):
        # action_status, action_info = QCloudIM.black_list_add(from_user, to_user)
        black_user = BlackUser()
        black_user.from_id = from_user.id
        black_user.to_id = to_user.id
        black_user.save()

        record = BlackUserRecord()
        record.from_id = from_user.id
        record.to_id = to_user.id
        record.oper_status = 1
        record.save()

        # 删除关注关系
        follow_user = FollowUser.objects.filter(from_id=from_user.id, to_id=to_user.id).first()
        if follow_user:
            follow_user.delete()
            record = FollowUserRecord()
            record.from_id = from_user.id
            record.to_id = to_user.id
            record.oper_status = 2
            record.save()

        rever_follow_user = FollowUser.objects.filter(from_id=to_user.id, to_id=from_user.id).first()
        if rever_follow_user:
            rever_follow_user.delete()
            record = FollowUserRecord()
            record.from_id = to_user.id
            record.to_id = from_user.id
            record.oper_status = 2
            record.save()

        # 如果是好友删除好友关系
        friend_user = FriendUser.objects.filter(from_id=from_user.id, to_id=to_user.id).first()
        if friend_user:
            friend_user.delete()
        rever_friend_user = FriendUser.objects.filter(to_id=from_user.id, from_id=to_user.id).first()

        if rever_friend_user:
            rever_friend_user.delete()


    # 删除黑名单用户
    @classmethod
    def black_delete(cls, from_user, to_user):
        user = BlackUser.objects.filter(from_id=from_user.id, to_id=to_user.id).first()
        if user:
          user.delete()

        record = BlackUserRecord()
        record.from_id = from_user.id
        record.to_id = to_user.id
        record.oper_status = 2
        record.save()

    # 黑名单列表
    @classmethod
    def black_user_list(cls, from_user):
        black_users = BlackUser.objects.filter(from_id=from_user.id)
        return black_users

    @classmethod
    def is_black(cls, user_id, black_user_id):
        black_user = BlackUser.objects.filter(from_id=user_id, to_id=black_user_id).first()
        rever_black_user = BlackUser.objects.filter(from_id=black_user_id, to_id=user_id).first()

        if black_user and not rever_black_user:
            return 1  # 您把对方拉黑


        if rever_black_user and not black_user:
            return 2  # 对方把您拉黑

        if black_user and rever_black_user:
            return 0  # 互相拉黑

        return 3  # 均未拉黑






class BlackUserRecord(Document):
    OPER_STATUS = (
        (1, u"拉黑"),
        (2, u"解除拉黑")
    )

    from_id = IntField(verbose_name=u'用户id', required=True)
    to_id = IntField(verbose_name=u'黑名单用户_id', required=True)
    oper_status = IntField(verbose_name=u'操作状态', choices=OPER_STATUS)
    create_time = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())