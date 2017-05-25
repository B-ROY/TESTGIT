#coding=utf-8
from mongoengine import *
import logging
import datetime
from app.customer.models.user import *
from app.customer.models.gift import *
from base.settings import CHATPAMONGO
from app.audio.models.record import AudioRoomRecord


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class ChatMessageLimit(Document):
    send_id = IntField(verbose_name=u"送礼用户id")
    receive_id = IntField(verbose_name=u"收礼用户id")
    money = IntField(verbose_name=u"门槛价格")
    send_time = DateTimeField(verbose_name=u"送礼时间", default=datetime.datetime.now())

    class Meta:
        app_label = u"customer"
        verbose_name = u"私聊门槛"
        verbose_name_plural = verbose_name

    @classmethod
    def check_friends(cls, send_id, receive_id):
        try:
            message = ChatMessageLimit.objects.filter(send_id=send_id, receive_id=receive_id).first()
            has_sent_gift = GiftRecord.objects.filter(from_id=str(send_id), to_id=str(receive_id)).first()
            has_paid_call = AudioRoomRecord.objects.filter(user_id=receive_id, join_id=send_id, now_price__gt=0)
            if not message and not has_sent_gift and not has_paid_call:
                message_reverse = ChatMessageLimit.objects.filter(send_id=receive_id, receive_id=send_id).first()
                has_sent_gift_reverse = GiftRecord.objects.filter(from_id=str(receive_id), to_id=str(send_id)).first()
                has_paid_call_reverse = AudioRoomRecord.objects.filter(user_id=send_id, join_id=receive_id, now_price__gt=0)
                if not message_reverse and not has_sent_gift_reverse and not has_paid_call_reverse:
                    return True, False
                else:
                    return True, True
            else:
                return True, True
        except Exception,e:
            logging.error("check friends error:{0}".format(e))
            return False, False

    @classmethod
    def create_chat_message(cls, send_id, receive_id, money=10):
        try:
            status, friend_status = ChatMessageLimit.check_friends(send_id=send_id, receive_id=receive_id)
            if status and not friend_status:
                message = ChatMessageLimit(send_id=send_id, receive_id=receive_id, money=money, send_time=datetime.datetime.now())
                message.save()
                send_user = User.objects.get(id=send_id)
                receive_user = User.objects.get(id=receive_id)
                send_user.wealth_value += money/10
                receive_user.charm_value += money/10
                send_user.save()
                receive_user.save()
            return True
        except Exception,e:
            logging.error("create chat message error:{0}".format(e))
            return False
