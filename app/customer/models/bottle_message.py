# coding=utf-8
import random
from mongoengine import *
from base.settings import CHATPAMONGO
import datetime

connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class BottleMessageText(Document):

    USER_TYPE = [
        (0, "主播发送"),
        (1, "用户发送")
    ]

    GENDER = [
        (0, "Both"),
        (1, "男用户"),
        (2, "女用户")
    ]

    DELETE_STATUS = [
        (0, "已删除"),
        (2, "正在使用")
    ]
    label = IntField(verbose_name=u"标签", unique=True)
    message = StringField(verbose_name=u"消息")
    sender_type = IntField(verbose_name=u"发送者类型", choices=USER_TYPE)
    gender = IntField(verbose_name=u"性别")
    delete_status = IntField(verbose_name=u"是否删除", )
    create_time = DateTimeField(verbose_name=u"创建时间")

    @classmethod
    def create_message_text(cls, label, message, sender_type, gender):
        obj_ = cls()
        obj_.label = label
        obj_.message = message
        obj_.sender_type = sender_type
        obj_.gender = gender
        obj_.create_time = datetime.datetime.now()
        obj_.save()

    @classmethod
    def get_message_text(cls, sender_type, gender=0):

        return cls.objects.filter(sender_type=sender_type)

    @classmethod
    def get_one_mesasge_text(cls, sender_type):

        messages = cls.objects.all()
        num = random.randint(0,messages.count()-1)
        return messages[num]


    @classmethod
    def delete_message_text(cls):
        #todo 待开发
        pass
    @classmethod
    def update_message_test(cls):
        #todo 待开发
        pass




class BottleRecord(Document):

    SEND_STATUS = [
        (0, "开始发送"),
        (1, "发送成功"),
        (2, "发送失败")
    ]

    SENDER_TYPE = [
        (0, "主播发送"),
        (1, "用户发送")
    ]

    user_id = IntField(verbose_name=u"发送者id")
    label = IntField(verbose_name=u"消息标签")
    messages = StringField(verbose_name=u"消息内容")
    sender_type = IntField(verbose_name=u"发送者类型", choices=SENDER_TYPE)
    send_time = DateTimeField(verbose_name=u"发送时间")
    count = IntField(verbose_name=u"发送人数")
    status = IntField(verbose_name=u"发送状态", choices=SEND_STATUS)


    @classmethod
    def create_bottle_record(cls, user_id, label, messages, sender_type, count):
        obj_ = cls()
        obj_.user_id = user_id
        obj_.label = label
        obj_.messages = messages
        obj_.sender_type = sender_type
        obj_.send_time = datetime.datetime.now()
        obj_.count = count
        # todo 暂时默认 发送陈功
        obj_.status = 1
        obj_.save()


    @classmethod
    def update(cls, id, status):
        record = cls.objects.get(id=id)
        record.update(set__status=status)















