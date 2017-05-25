#coding=utf-8
from mongoengine import *
import logging
import datetime
import time
from base.core.util.dateutils import datetime_to_timestamp
from app.customer.models.user import *
from django.db import models
from base.settings import CHATPAMONGO

connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username, password=CHATPAMONGO.password)


class UserRoomInfo(Document):

    user_id = IntField(verbose_name=u'用户id', required=True)
    room_id = StringField(verbose_name=u'房间id', max_length=256, default=None)
    total_time = IntField(verbose_name=u'总时长(秒)', default=0)
    total_income = IntField(verbose_name=u'总收入', default=0)
    total_rate = IntField(verbose_name=u'总评分', default=0)
    total_amount = IntField(verbose_name=u'总订单数', default=0)
    update_time = DateTimeField(verbose_name=u'更新时间', default=None)
    listen_url = StringField(verbose_name=u'试听url', max_length=256, default="")
    now_price = IntField(verbose_name=u'当前价格', required=True)
    private_id = StringField(verbose_name=u'私密照片集', default="")
    
    class Meta:
        app_label = "audio"
        verbose_name = u"语音"
        verbose_name_plural = verbose_name

    def normal_info(self):
        data = {}
        data['id'] = str(self.id)
        data['user_id'] = self.user_id
        data['room_id'] = self.room_id
        data['total_time'] = self.total_time
        data['total_income'] = self.total_income
        data['total_rate'] = self.total_rate
        data['total_amount'] = self.total_amount
        data['update_time'] = datetime_to_timestamp(self.update_time)
        data['listen_url'] = self.listen_url
        data['now_price'] = self.now_price
        return data

    @classmethod
    def create_userroom(cls, user_id, room_id=None, update_time=None, total_time=0, total_income=0, total_rate=0,
                        total_amount=0, listen_url=None, now_price=0):
        user = UserRoomInfo.get_user_info(user_id)
        if not user:
            try:
                userroom = UserRoomInfo(
                    user_id=user_id,
                    room_id=room_id,
                    total_time=total_time,
                    total_income=total_income,
                    total_rate=total_rate,
                    total_amount=total_amount,
                    update_time=update_time,
                    listen_url=listen_url,
                    now_price=now_price,
                    )
                userroom.save()

            except Exception,e:
                logging.error("create user room error:{0}".format(e))
                return False
            return True

    @classmethod
    def update_userroom(cls, user_id, room_id=None, update_time=None, total_time=0, total_income=0, total_rate=0,
                        total_amount=0, listen_url=None, now_price=0):
        try:
            user = cls.objects.get(user_id=user_id)
            user.room_id = room_id
            user.total_time += total_time
            user.total_income += total_income
            user.total_rate += total_rate
            user.total_amount += total_amount
            user.update_time = update_time
            user.listen_url = listen_url
            user.now_price = now_price
            user.save()

        except Exception,e:
            logging.error("update user room error:{0}".format(e))
            return False
        return True

    @classmethod
    def get_user_info(cls, user_id):
        try:
            user = cls.objects.get(user_id=user_id)
        except UserRoomInfo.DoesNotExist:
            return None
        return user

    @classmethod
    def get_user_info_db(cls, user_id):
        try:
            user = User.objects.get(id=user_id)
        except Exception,e:
            logging.error("get user info in db error:{0}".format(e))
            return None
        return user

    @classmethod
    def get_room_id(cls, user_id):
        user = cls.objects.filter(user_id=user_id)
        if not user:
            return None
        else:
            return user.first().room_id
        # if user.first() != [] and user.first().room_id:
        #    room_id = user.first().room_id
        #    return room_id
        # else:
        #    return None


class PrivatePicture(Document):

    user_id = IntField(verbose_name=u'用户id', required=True)
    picture_list = ListField(DictField(verbose_name=u'私密图片', default={}))

    class Meta:
        app_label = "audio"
        verbose_name = u"语音私密照片"
        verbose_name_plural = verbose_name

    def normal_info(self):
        data = {}
        data['user_id'] = self.user_id
        data['picture_list'] = self.picture_list
        return data

    @classmethod
    def get_private_picture(cls, user_id):
        try:
            user_private = PrivatePicture.objects.filter(user_id=user_id)
            if not user_private:
                return True, []
            else:
                return True, user_private.first().picture_list
        except Exception,e:
            logging.error("get private picture error:{0}".format(e))
            return False, 0

    @classmethod
    def create_private_picture(cls, user_id, picture_url, price=0):
        try:
            data = {}
            data['picture_url'] = picture_url
            data['price'] = price
            user_private = PrivatePicture(
                user_id=user_id,
                picture_list=[data],
            )
            user_private.save()

            user = UserRoomInfo.get_user_info(user_id)
            if not user:
                user = UserRoomInfo(
                    user_id=user_id,
                    room_id=None,
                    total_time=None,
                    total_income=0,
                    total_rate=0,
                    total_amount=0,
                    update_time=datetime.datetime.now(),
                    listen_url=None,
                    now_price=None,
                    private_id=str(user_private.id),
                )
            else:
                user.private_id = str(user_private.id)
            user.save()

        except Exception,e:
            logging.error("create private picture error:{0}".format(e))
            return False, 0
        return True, 1

    @classmethod
    def add_private_picture(cls, user_id, picture_url, price=0):
        try:
            user_private = PrivatePicture.objects.get(user_id=user_id)
            if len(user_private.picture_list) < 5:
                data = {}
                data['picture_url'] = picture_url
                data['price'] = price

                if price == 0:
                    for i in range(len(user_private.picture_list)):
                        if user_private.picture_list[i]['price'] != 0:
                            user_private.picture_list.insert(i, data)
                            user_private.save()
                            return True, 1

                    user_private.picture_list.append(data)
                    user_private.save()
                    return True, 1
                else:
                    user_private.picture_list.append(data)
                    user_private.save()
                    return True, 1
            else:
                return False, 10001

        except PrivatePicture.DoesNotExist:
            status, code = PrivatePicture.create_private_picture(user_id, picture_url, price)
            return status, code

    @classmethod
    def change_private_picture(cls, user_id, picture_url, position, price=0):
        try:
            user_private = PrivatePicture.objects.get(user_id=user_id)
            user_private.picture_list[position - 1]['picture_url'] = picture_url
            user_private.picture_list[position - 1]['price'] = price
            user_private.save()
        except Exception,e:
            logging.error("change private picture error:{0}".format(e))
            return False
        return True

    @classmethod
    def delete_private_picture(cls, user_id, position):
        try:
            user_private = PrivatePicture.objects.get(user_id=user_id)
            user_private.picture_list.pop(position-1)
            user_private.save()
        except Exception,e:
            logging.error("delete private picture error:{0}".format(e))
            return False
        return True

