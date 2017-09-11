# coding=utf-8

import datetime
import logging

from app.audio.models.record import AudioRoomRecord
from app.customer.models.account import TradeDiamondRecord, TradeTicketRecord, Account
from app.customer.models.benifit import TicketAccount
from base.settings import CHATPAMONGO
from django.conf import settings
from mongoengine import *
from app.util.messageque.msgsender import MessageSender
from app_redis.room.room import RoomRedis
import international

connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class Gift(Document):
    BIG_GIFT_THRESHOLD = settings.BIG_GIFT_THRESHOLD

    STATUS = [
        (0, u'已删除'),
        (1, u'使用'),
    ]

    ANITYPE = [
        (0, u'静态'),
        (1, u'动态'),
    ]

    ANITYPE_MAP = {
        0: u'静态',
        1: u"动态",
    }
    GIFT_TYPE = {
        1: "礼物商城中的",
        2: "快捷送礼中的",
        3: "礼物门槛送礼物"
    }
    STATUS_DELETED = 0
    STATUS_USING = 1

    name = StringField(max_length=32, verbose_name=u'礼物名称')
    price = IntField(verbose_name=u'价格（单位：分)')
    status = IntField(verbose_name=u'状态', choices=STATUS)
    experience = IntField(verbose_name=u'经验值')
    ticket = IntField(verbose_name=u'粒子数')
    continuity = IntField(verbose_name=u'是否可连续送出')
    animation_type = IntField(verbose_name=u'状态')
    logo = StringField(max_length=256, verbose_name=u'礼物logo')
    is_flower = IntField(verbose_name=u'是否是花', default=0)
    seq = IntField(verbose_name=u'排序', default=0)
    gift_type = IntField(verbose_name=u'礼物类型（是否在快捷赠送的列表中显示）',choices=GIFT_TYPE)
    wealth_value = IntField(verbose_name=u'礼物增加送礼人的财富值')
    charm_value = IntField(verbose_name=u'礼物增加送礼人的魅力值')
    show_status = IntField(verbose_name=u'是否展示')  # 1展示 2不展示
    handy_order = IntField(verbose_name=u'快捷礼物排序')

    @property
    def logo_small(self):
        return self.logo + "/logo120"  # 万象优图样式

    def normal_info(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "price": self.price,
            "experience": self.experience,
            "ticket": self.ticket,
            "continuity": self.continuity,
            "animation_type": self.animation_type,
            "animation_type_desc": self.ANITYPE_MAP.get(self.animation_type, 0),
            "logo": self.logo,
            "logo_small": self.logo_small,
            "is_flower": self.is_flower,
            "seq": self.seq,
            "gift_type":self.gift_type,
            "wealth_value": self.wealth_value,
            "charm_value": self.charm_value,
        }

    @classmethod
    def list(cls, gift_type=1):
        return cls.objects.filter(status=Gift.STATUS_USING, gift_type=gift_type, show_status=1).order_by("handy_order")

    @classmethod
    def list_all(cls):
        return cls.objects.filter(status=Gift.STATUS_USING).order_by("price")

    @classmethod
    def list_mall(cls):
        return cls.objects.filter(status=Gift.STATUS_USING, gift_type__in=[1, 2], show_status=1).order_by("price")

    @classmethod
    def create(cls, name, price, experience, ticket, continuity, animation_type, logo, is_flower=0, gift_type=0, wealth_value=0, charm_value=0):
        try:
            _obj = cls()
            _obj.name = name
            _obj.price = price
            _obj.experience = experience
            _obj.ticket = ticket
            _obj.continuity = continuity
            _obj.animation_type = animation_type
            _obj.logo = cls.convert_http_to_https(logo)
            _obj.status = 1
            _obj.is_flower = is_flower
            _obj.gift_type = gift_type
            _obj.wealth_value = wealth_value
            _obj.charm_value = charm_value
            _obj.save()
            return _obj
        except Exception, e:
            logging.error("create Gift error:{0}".format(e))
        return ''

    @classmethod
    def update(cls, obj_id, name, price, experience, ticket, continuity, animation_type, logo, is_flower=0, gift_type=0,
               wealth_value=0, charm_value=0):
        try:
            _obj = cls.objects.get(id=obj_id)
            _obj.name = name
            _obj.price = price
            _obj.experience = experience
            _obj.ticket = ticket
            _obj.continuity = continuity
            _obj.animation_type = animation_type
            _obj.logo = cls.convert_http_to_https(logo)
            # _obj.status = status
            _obj.is_flower = is_flower
            _obj.gift_type = gift_type
            _obj.wealth_value = wealth_value
            _obj.charm_value = charm_value
            _obj.save()
            return _obj
        except Exception, e:
            logging.error("update Gift error:{0}".format(e))
        return ''
    @classmethod
    def gift_giving(cls, from_user, to_user, gift_id, gift_count, gift_price, room_id):
        try:

            gift = Gift.objects.get(id=gift_id)
            gift_total_price = gift_price*gift_count
            #看送礼人的钱是否足够送礼
            from_user_account = Account.objects.get(user=from_user)
            from_user_money = from_user_account.diamond
            if from_user_money < gift_total_price:
                return False, 4001, _(u"余额不足")

            # big_gift_发送公告
            if gift_total_price >= cls.BIG_GIFT_THRESHOLD:
                MessageSender.send_big_gift_info_message(
                    sender_id=from_user.id, sender_name=from_user.nickname,
                    receiver_id=to_user.id, receiver_name=to_user.nickname,
                    gift_id=gift_id, gift_count=gift_count, gift_name=gift.name
                )

            #记录本次交易
            #送礼人加经验 财富值 减钱

            account = Account.objects.get(user=from_user)
            account.diamond_trade_out(price=gift_total_price, desc=u"礼物赠送，收礼方id=%s, 礼物id=%s ,礼物数量=%s, 房间号=%s" %
                         (to_user.id, gift_id, str(gift_count), room_id), trade_type=TradeDiamondRecord.TradeTypeGift)
            from_user.update(
                inc__wealth_value = gift_total_price/10,
                inc__cost = gift_total_price,
            )

            to_user.update(
                inc__charm_value = gift_total_price / 10,
                inc__ticket = gift_total_price
            )

            # 2. 收礼人+经验, +粒子数

            # to_user.add_experience(10)
            ticket_account = TicketAccount.objects.get(user=to_user)
            ticket_account.add_ticket(trade_type=TradeTicketRecord.TradeTypeGift, ticket=gift_total_price, desc=
                                        u"收到礼物, 送礼方id=%s, 礼物id=%s, 礼物数量=%s, 房间号=%s" %
                                        (from_user.id, gift_id, str(gift_count), room_id))

            GiftRecord.create(gift_id=str(gift_id), gift_name=gift.name, gift_price=gift.price,
                              gift_count=gift_count, gift_logo=gift.logo, from_id=str(from_user.id),
                              to_id=str(to_user.id), room_id=room_id)

            if room_id:
                room_record = AudioRoomRecord.objects.get(id=room_id)
                if from_user.id == room_record.join_id and to_user.id == room_record.user_id:
                    room_record.add_gift_value(gift_total_price)


            return True, None, None
        except Exception, e:
            logging.error("gift giving error {%s}" % str(e))
            return False, None, None

    @classmethod
    def convert_http_to_https(cls, url):
        if "https" in url:
            return url
        else:
            return url.replace("http", "https")
            # return url

    class Meta:
        app_label = "customer"
        verbose_name = u"礼物"
        verbose_name_plural = verbose_name


class GiftRecord(Document):
    gift_id = StringField(max_length=32, verbose_name=u"礼物ID")
    gift_name = StringField(max_length=32, verbose_name=u"l礼物名字")
    gift_price = IntField(verbose_name=u"礼物价格")
    gift_count = IntField(verbose_name=u"赠送数量")
    gift_logo = StringField(max_length=255, verbose_name=u"礼物图标")
    from_id = StringField(max_length=32,verbose_name=u"送礼人")
    to_id = StringField(max_length=32, verbose_name=u"收礼人")
    room_id = StringField(max_length=32, verbose_name=u"送礼物房间id")
    create_time = DateTimeField(verbose_name=u"送礼时间")

    @classmethod
    def create(cls, gift_id, gift_name, gift_logo, gift_price, gift_count, from_id, to_id,room_id=""):
        gift_record = cls()
        gift_record.gift_id = gift_id
        gift_record.gift_name = gift_name
        gift_record.gift_logo = gift_logo
        gift_record.gift_price = gift_price
        gift_record.gift_count = gift_count
        gift_record.from_id = from_id
        gift_record.to_id = to_id
        gift_record.room_id = room_id
        gift_record.create_time = datetime.datetime.now()
        gift_record.save()

    @classmethod
    def get_received_list(cls, uid):
        gift_received_records = cls.objects.filter(to_id=uid)
        gift_received_list = {}

        for gift_record in gift_received_records:
            if gift_record.gift_id in gift_received_list:
                gift_received_list[gift_record.gift_id].gift_count += gift_record.gift_count
            else:
                gift_received_list[gift_record.gift_id] = gift_record
        gift_list = gift_received_list.values()
        gift_list.sort(key=lambda record: record.gift_price, reverse=True)
        return gift_list

    def get_normal_dic_info(self):
        return{
            "id": self.gift_id,
            "name": self.gift_name,
            "price": self.gift_price,
            "gift_count": self.gift_count,
            "logo": self.gift_logo,

        }


class GiftManager(object):
    # 语音账单检查
    @classmethod
    def audio_check(cls, room_id):
        try:
            count = RoomRedis.room_paybill(room_id)
            if count == 0:
                return False, 0
            else:
                return True, count

            # now_time = datetime.datetime.now()
            # desc = u"语音聊天id=%s" % room_id
            # user_bill = TradeDiamondRecord.objects.filter(desc=desc).order_by("-created_time")
            # if not user_bill:
            #     return True, 1
            # else:
            #     total_seconds = int((now_time - user_bill.first().created_time).total_seconds())
            #     if total_seconds >= 55:
            #         return True, (total_seconds + 5) / 60
            #     else:
            #         return False, 0

        except Exception, e:
            logging.error("audio check error:{0}".format(e))
            return False, 0

    # 语音账单(每分钟扣费)
    @classmethod
    # @transaction.commit_on_success
    def audio_bill(cls, room_id, times=1):
        from app.audio.models.record import AudioRoomRecord
        from app.customer.models.user import User
        try:
            roomrecord = AudioRoomRecord.objects.get(id=room_id)
            price = roomrecord.now_price

            # 1. 加入者+经验, -引力币
            from_user = User.objects.get(id=roomrecord.join_id)
            from_user_account = Account.objects.get(user=from_user)


            cost = price*times

            if from_user_account.diamond < price:
                return False, from_user_account.diamond
            from_user_account.diamond_trade_out(price=cost, desc=u"语音聊天id=%s" % room_id,trade_type=TradeDiamondRecord.TradeTypeAudio)

            from_user.update(inc__cost=cost)

            to_user = User.objects.get(id=roomrecord.user_id)
            to_user.update(
                inc__ticket=cost
            )


            # to_user.add_experience(10)
            ticket_account = TicketAccount.objects.get(user=to_user)
            ticket_account.add_ticket(trade_type=TradeTicketRecord.TradeTypeAudio, ticket=cost, desc=
            u"语音聊天id=%s" % room_id)

            account_money = from_user_account.diamond

        except Exception, e:
            logging.error("audio bill add error:{0}".format(e))
            return False, 0
        return True, account_money

    # 分享加钱
    @classmethod
    def share_bill(cls, user_id, diamon=50):
        from app.customer.models.user import User
        try:
            user = User.objects.get(id=user_id)
            user_account = Account.objects.get(user=user)
            user_bill = TradeDiamondRecord(
                user=user,
                before_balance=user_account.diamond,
                after_balance=user_account.diamond + diamon,
                diamon=diamon,
                desc=u"分享获得",
                created_time=datetime.datetime.now(),
                trade_type=TradeDiamondRecord.TradeTypeShare,
            )
            user_bill.save()

            user_account.last_diamond = user_account.diamond
            user_account.diamond += diamon
            user_account.diamond_bonus += diamon
            user_account.save()

        except Exception, e:
            logging.error("sign in bill error:{0}".format(e))
            return False
        return True

    # 消息门槛送礼物
    @classmethod
    def message_bill(cls, send_id, receive_id, money=100):
        from app.customer.models.user import User
        from app.customer.models.message import ChatMessageLimit
        try:
            # 1. 送礼者 -钱
            from_user = User.objects.get(id=send_id)
            from_user_account = Account.objects.get(user=from_user)
            if from_user_account.diamond < money:
                return True, 0

            from_user_bill = TradeDiamondRecord(
                user=from_user,
                before_balance=from_user_account.diamond,
                after_balance=from_user_account.diamond - money,
                diamon=money,
                desc=u"消息门槛送礼id=%s" % receive_id,
                created_time=datetime.datetime.now(),
                trade_type=TradeDiamondRecord.TradeTypeMessage,
            )
            from_user_bill.save()

            from_user_account.last_diamond = from_user_account.diamond
            from_user_account.diamond -= money
            from_user_account.save()

            status = ChatMessageLimit.create_chat_message(send_id=send_id, receive_id=receive_id, money=10)
            if not status:
                return False, 0

        except Exception, e:
            logging.error("audio bill add error:{0}".format(e))
            return False, 0
        return True, 10

