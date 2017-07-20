# coding=utf-8

import datetime
import logging

from base.settings import CHATPAMONGO
from django.conf import settings
from mongoengine import *


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)

# 用户关注表
class FollowUser(Document):

    from_id = IntField(verbose_name=u'用户id', required=True)
    to_id = IntField(verbose_name=u'关注用户_id', required=True)
    create_time = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())


    @classmethod
    def follow_user_add(cls, from_user, to_user):
        follow_user = FollowUser.objects.filter(from_id=from_user.id, to_id=to_user.id).first()

        # 判断是不是好友了已经:
        friend_user = FriendUser.objects.filter(from_id=from_user.id, to_id=to_user.id).first()
        if not friend_user:
            if not follow_user:
                # 如果已经反向关注了.  互相关注成为好友
                rever_follow_user = FollowUser.objects.filter(to_id=from_user.id, from_id=to_user.id).first()
                if rever_follow_user:
                    rever_follow_user.delete()

                    friend = FriendUser()
                    friend.from_id = from_user.id
                    friend.to_id = to_user.id
                    friend.save()

                    rever_friend = FriendUser()
                    rever_friend.from_id = to_user.id
                    rever_friend.to_id = from_user.id
                    rever_friend.save()
                else:
                    follow_user = FollowUser()
                    follow_user.from_id = from_user.id
                    follow_user.to_id = to_user.id
                    follow_user.save()

                record = FollowUserRecord()
                record.from_id = from_user.id
                record.to_id = to_user.id
                record.oper_status = 1
                record.save()


    @classmethod
    def follow_user_delete(cls, from_user, to_user):
        follow_user = FollowUser.objects.filter(from_id=from_user.id, to_id=to_user.id).first()
        if follow_user:
            follow_user.delete()

        # 如果是互相关注, 要取消好友关系, 重新创建关注关系.
        friend_user = FriendUser.objects.filter(from_id=from_user.id, to_id=to_user.id).first()
        if friend_user:
            friend_user.delete()

            follow_user_new = FollowUser()
            follow_user_new.from_id = to_user.id
            follow_user_new.to_id = from_user.id
            follow_user_new.save()

        rever_friend_user = FriendUser.objects.filter(to_id=from_user.id, from_id=to_user.id).first()
        if rever_friend_user:
            rever_friend_user.delete()

        record = FollowUserRecord()
        record.from_id = from_user.id
        record.to_id = to_user.id
        record.oper_status = 2
        record.save()

    @classmethod
    def is_follow_user(cls, from_id, to_id):
        follow_user = FollowUser.objects.filter(from_id=from_id, to_id=to_id).first()
        follow_type = 0

        if follow_user:
            follow_type = 1
        else:
            friend_user = FriendUser.objects.filter(from_id=from_id, to_id=to_id).first()
            if friend_user:
                follow_type = 1
        return follow_type


class FollowUserRecord(Document):
    OPER_STATUS = (
        (1, u"关注"),
        (2, u"取消关注")
    )

    from_id = IntField(verbose_name=u'用户id', required=True)
    to_id = IntField(verbose_name=u'关注用户_id', required=True)
    oper_status = IntField(verbose_name=u'操作状态', choices=OPER_STATUS)
    create_time = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())


class FriendUser(Document):
    from_id = IntField(verbose_name=u'用户id', required=True)
    to_id = IntField(verbose_name=u'好友用户_id', required=True)
    create_time = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())

