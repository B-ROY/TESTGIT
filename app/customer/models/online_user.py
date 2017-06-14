# coding=utf-8
from mongoengine import *
import logging
import datetime
import time
from app.customer.models.user import *
from django.db import models
from base.settings import CHATPAMONGO


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


# 用户在线状态
class OnlineUser(Document):
    STATUS = [
        (0, u'不在线'),
        (1, u'在线'),
    ]

    user = GenericReferenceField("User", verbose_name=u'用户')
    status = IntField(verbose_name=u"状态", choices=STATUS)
    update_time = DateTimeField(verbose_name=u'更新时间', default=None)

    class Meta:
        app_label = "customer"
        verbose_name = u"在线用户"
        verbose_name_plural = verbose_name

    def normal_info(self):
        data = {}
        data["id"] = str(self.id)
        data["user_id"] = self.user.id
        data["status"] = self.status
        data["update_time"] = self.update_time
        return data

    @classmethod
    def create_online_user(cls, user_id):
        try:
            user = User.objects.get(id=user_id)
            online_user = OnlineUser(
                user=user,
                status=1,
                update_time=datetime.datetime.now(),
            )
            online_user.save()
            return True
        except Exception, e:
            logging.error("create online user error:{0}".format(e))
            return False

    @classmethod
    def update_online_user(cls, user_id, action):
        try:
            user = User.objects.filter(id=user_id).first()
            online_user = OnlineUser.objects.filter(user=user).first()
            if not online_user:
                desc = u"<html><p>" + u"恭喜您注册成功，快去体验我们给您带来的最新交友方式吧！！" + u"</p></html>"
                MessageSender.send_system_message(user_id, desc)
                return OnlineUser.create_online_user(user_id=user_id)
            if action == "Login":
                status = 1
            else:
                status = 0
            online_user.update(set__status=status, set__update_time=datetime.datetime.now())
            return True
        except OnlineUser.DoesNotExist:
            return OnlineUser.create_online_user(user_id=user_id)


    @classmethod
    def get_list(cls):
        try:
            online_list = OnlineUser.objects.filter(status=1).order_by("-update_time")
            return online_list
        except Exception, e:
            logging.error("get list error:{0}".format(e))
            return []

    @classmethod
    def get_list_v1(cls, query_time, method=0, page=1, page_count=20):
        try:
            if method == 0:
                online_list = OnlineUser.objects(status=1, update_time__lt=query_time).order_by("-update_time")[0:page_count]
                return online_list
            else:
                online_list = OnlineUser.objects(status=1, update_time__lt=query_time).order_by("-update_time")
                online_user = []
                for user in online_list:
                    if user.user.gender == method:
                        online_user.append(user)

                return online_user[0:page_count]

        except Exception, e:
            logging.error("get list v1 error:{0}".format(e))
            return []

    @classmethod
    def get_timestamp(cls, user):
        online_user = OnlineUser.objects.get(user=user)
        update_time = online_user.update_time
        return datetime_to_timestamp(update_time)


# 用户在线状态(缓冲区列表)
class OnlineBufferList(Document):

    METHOD = [
        (0, u"全部排序"),
        (1, u"只显示男性"),
        (2, u"只显示女性"),
    ]

    user_list = ListField(IntField(verbose_name=u"用户id"))
    update_time = DateTimeField(verbose_name=u"更新时间")
    method = IntField(verbose_name=u"排序方式", choices=METHOD)

    class Meta:
        app_label = "customer"
        verbose_name = u"缓冲区列表"
        verbose_name_plural = verbose_name

    def normal_info(self):
        data = {}
        data["id"] = str(self.id)
        data["user_list"] = self.user_list
        data["update_time"] = self.update_time
        data["method"] = self.method
        return data

    @classmethod
    def create_user_list(cls, method):
        try:
            user_list = OnlineBufferList(
                user_list=[],
                update_time=datetime.datetime.now(),
                method=method,
            )
            user_list.save()
            return True
        except Exception, e:
            logging.error("create user list error:{0}".format(e))
            return False

    @classmethod
    def get_user_list(cls, method=0, page=1, page_count=20):
        try:
            pre_list = OnlineBufferList.objects.get(method=method)

            if int((datetime.datetime.now() - pre_list.update_time).total_seconds()) > 60:
                online_user = OnlineUser.get_list()
                user_list = []
                if method == 0:
                    for user in online_user:
                        user_list.append(user.user.id)
                else:
                    for user in online_user:
                        if user.user.gender == method:
                            user_list.append(user.user.id)

                pre_list.user_list = user_list
                pre_list.update_time = datetime.datetime.now()
                pre_list.save()

            user_list = OnlineBufferList.objects.get(method=method).user_list[(page-1)*page_count:page*page_count]
            return True, user_list
        except OnlineBufferList.DoesNotExist:
            try:
                status = OnlineBufferList.create_user_list(method=method)
                return status, []
            except Exception, e:
                logging.error("get user list error:{0}".format(e))
                return False, None

