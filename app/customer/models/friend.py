# coding=utf-8

import datetime
import logging

from base.settings import CHATPAMONGO
from django.conf import settings
from mongoengine import *


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)

#  好友关系表
class Friend(Document):

    FRIEND_STATUS = (
        (1, u"申请"),
        (2, u"同意")
    )

    user_id = IntField(verbose_name=u'用户id', required=True)
    friend_id = IntField(verbose_name=u'friend_id', required=True)
    friend_status = IntField(verbose_name=u'朋友状态', choices=FRIEND_STATUS)
    create_time = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())
    update_time = DateTimeField(verbose_name=u"更新时间", default=datetime.datetime.now())


    # 申请好友
    @classmethod
    def apply_friend(cls, user_id, friend_id):
        now = datetime.datetime.now()
        friend = Friend.objects.filter(user_id=user_id, friend_id=friend_id, friend_status=1).first()
        if not friend:
            friend = Friend()
            friend.user_id = user_id
            friend.friend_id = friend_id
            friend.friend_status = 1
            friend.create_time = now
            friend.update_time = now
            friend.save()
        else:
            friend.update_time = now
            friend.save()
        FriendRecord.add(user_id, friend_id, 1)

        # 申请状态表
        FriendStatusRecord.add(user_id, friend_id, 1)




    # 同意添加好友
    @classmethod
    def add_friend(cls, user_id, friend_id):
        now = datetime.datetime.now()
        print "user_id", user_id
        print "friend_id", friend_id

        friend = Friend.objects.filter(user_id=friend_id, friend_id=user_id, friend_status=1).first()
        if friend:
            print "--------------"
            friend.friend_status = 2
            friend.update_time = now
            friend.save()
            FriendRecord.add(user_id, friend_id, 2)
            print "success!!!!!"

            # 申请状态表
            FriendStatusRecord.add(user_id, friend_id, 2)




        reverse_friend = Friend.objects.filter(user_id=user_id, friend_id=friend_id, friend_status=1).first()
        if reverse_friend:
            reverse_friend.friend_status = 2
            reverse_friend.update_time = now
        else:
            reverse_friend = Friend()
            reverse_friend.user_id = user_id
            reverse_friend.friend_id = friend_id
            reverse_friend.friend_status = 2
            reverse_friend.create_time = now
            reverse_friend.update_time = now
        reverse_friend.save()

    # 拒绝添加好友
    @classmethod
    def reject_friend(cls, user_id, friend_id):
        friend = Friend.objects.filter(user_id=friend_id, friend_id=user_id, friend_status=1).first()

        friend.delete()
        FriendRecord.add(user_id, friend_id, 3)

        reverse_friend = Friend.objects.filter(user_id=user_id, friend_id=friend_id, friend_status=1).first()
        if reverse_friend:
            reverse_friend.delete()

    # 拉黑好友
    @classmethod
    def black_friend(cls, user_id, friend_id):
        friend = Friend.objects.filter(user_id=friend_id, friend_id=user_id, friend_status=2).first()

        friend.delete()
        FriendRecord.add(user_id, friend_id, 4)

        reverse_friend = Friend.objects.filter(user_id=user_id, friend_id=friend_id, friend_status=2).first()
        if reverse_friend:
            reverse_friend.delete()


# 好友记录表
class FriendRecord(Document):
    FRIEND_STATUS = (
        (1, u"申请"),
        (2, u"同意"),
        (3, u"拒绝"),
        (4, u"拉黑"),
    )

    CLEAR_STATUS = (
        (0, u"未清除"),
        (1, u"清除")
    )

    oper_user_id = IntField(verbose_name=u'动作操作方 用户id', required=True)
    to_user_id = IntField(verbose_name=u'对方用户id', required=True)
    friend_status = IntField(verbose_name=u'朋友状态', choices=FRIEND_STATUS)
    create_time = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())

    @classmethod
    def add(cls, oper_user_id, to_user_id, friend_status):
        record = FriendRecord()
        record.oper_user_id = oper_user_id
        record.to_user_id = to_user_id
        record.friend_status = friend_status
        record.save()


# 好友关系 状态表(申请列表使用)
class FriendStatusRecord(Document):
    FRIEND_STATUS = (
        (1, u"申请"),
        (2, u"同意"),
        (3, u"拒绝"),
        (4, u"拉黑"),
    )

    oper_user_id = IntField(verbose_name=u'动作操作方 用户id', required=True)
    to_user_id = IntField(verbose_name=u'对方用户id', required=True)
    friend_status = IntField(verbose_name=u'朋友状态', choices=FRIEND_STATUS)
    create_time = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())

    @classmethod
    def add(cls, oper_user_id, to_user_id, friend_status):
        status_record = FriendStatusRecord()
        status_record.oper_user_id = oper_user_id
        status_record.to_user_id = to_user_id
        status_record.friend_status = friend_status
        status_record.save()

    @classmethod
    def clear_record_list(cls, user_id):
        cls.objects.filter(to_user_id=user_id, friend_status=1).delete()
        cls.objects.filter(oper_user_id=user_id, friend_status=2).delete()

    @classmethod
    def black_user_clear(cls, oper_user_id, to_user_id):
        cls.objects.filter(oper_user_id=oper_user_id, to_user_id=to_user_id).delete()
        cls.objects.filter(oper_user_id=to_user_id, to_user_id=oper_user_id).delete()








