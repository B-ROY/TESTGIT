#coding=utf-8
from django.db import models
import logging
from app.customer.models.user import User
from wi_model_util.imodel import *
from django.db.models import Q
import time
import datetime
from mongoengine import *
from base.settings import CHATPAMONGO


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class FriendsList(Document):

    user_id = IntField(verbose_name=u'用户id')
    friends_list = ListField(IntField(verbose_name=u'用户好友列表'))
    stars_list = ListField(IntField(verbose_name=u'星标好友列表'))

    class Meta:
        app_label = "customer"
        verbose_name = u"用户好友列表"
        verbose_name_plural = verbose_name

    @classmethod
    def create_friends(cls, user_id, friend_id):
        try:
            user = FriendsList.objects.filter(user_id=user_id)
            if not user:
                user = FriendsList(
                    user_id=user_id,
                    friends_list=[friend_id],
                    stars_list=[],
                )
            else:
                user = user.first()
                if friend_id not in user.friend_list:
                    user.friend_list.append(friend_id)
            user.save()

            friend_user = FriendsList.objects.filter(user_id=friend_id)
            if not friend_user:
                friend_user = FriendsList(
                    user_id=friend_id,
                    friend_list=[user_id],
                    stars_list=[],
                )
            else:
                friend_user = friend_user.first()
                if user_id not in friend_user.friend_list:
                    friend_user.friend_list.append(user_id)
            friend_user.save()

            return True
        except Exception,e:
            logging.error("create friends error:{0}".format(e))
            return False

    @classmethod
    def check_friends(cls, user_id, friend_id):
        user = FriendsList.objects.filter(user_id=user_id)
        if not user:
            return False
        else:
            if friend_id in user.first().friend_list:
                return True
            else:
                return False

    @classmethod
    def delete_friends(cls, user_id, friend_id):
        try:
            user = FriendsList.objects.get(user_id=user_id)
            if friend_id in user.friend_list:
                user.friend_list.pop(friend_id)
            user.save()
        except Exception,e:
            logging.error("delete friends error:{0}".format(e))
            return False
        return True

    @classmethod
    def get_friends_list(cls, user_id):
        try:
            user = FriendsList.objects.get(user_id=user_id)
            return user.friend_list
        except FriendsList.DoesNotExist:
            return []


class FriendsRequestList(Document):

    REQUEST_STATUS = [
        (0, u'未读'),
        (1, u'已读'),
        (2, u'通过'),
        (3, u'拒绝'),
    ]

    user_id = IntField(verbose_name=u'用户id')
    requested_id = IntField(verbose_name=u'被申请用户id')
    request_time = ListField(DateTimeField(verbose_name=u'请求时间'))
    update_time = DateTimeField(verbose_name=u'更新时间')
    request_status = IntField(verbose_name=u'请求状态', choices=REQUEST_STATUS)

    class Meta:
        app_label = "customer"
        verbose_name = u"好友申请列表"
        verbose_name_plural = verbose_name

    @classmethod
    def create_friends_request(cls, user_id, requested_id):
        try:
            request = FriendsRequestList.objects.filter(user_id=user_id, requested_id=requested_id)
            if not request:
                request = FriendsRequestList(
                    user_id=user_id,
                    requested_id=requested_id,
                    request_time=[datetime.datetime.now()],
                    update_time=datetime.datetime.now(),
                    request_status=0,
                )
            else:
                request = request.first()
                request.request_time.append(datetime.datetime.now())
                request.update_time = datetime.datetime.now()

            request.save()
            return True
        except Exception,e:
            logging.error("create friends request error:{0}".format(e))
            return False

    @classmethod
    def change_request_status(cls, user_id, requested_id, status):
        try:
            request = FriendsRequestList.objects.filter(user_id=user_id, requested_id=requested_id).first()
            request.request_status = status
            request.update_time = datetime.datetime.now()
            request.save()
            return True
        except Exception,e:
            logging.error("change request status error:{0}".format(e))
            return False

    # 获取用户所有被申请列表
    @classmethod
    def get_requested_list(cls, user_id):
        requests = FriendsRequestList.objects.filter(requested_id=user_id).order_by("-update_time")
        return requests





