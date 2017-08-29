# coding=utf-8

from django.db import models
import logging
import datetime
from wi_model_util.imodel import *
from mongoengine import *
from base.settings import CHATPAMONGO
from app.util.messageque.msgsender import MessageSender

connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class ChatMessage(Document):
    from_user_id = IntField(verbose_name=u"用户id")
    to_user_id = IntField(verbose_name=u"接收用户id")
    create_time = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())
    type = IntField(verbose_name=u"消息类型")  # 1:文本  2:图片  3: 音频
    content = StringField(max_length=1024, verbose_name=u"消息内容")
    conversation_id = StringField(verbose_name=u"会话id", max_length=64)
    resource_url = StringField(verbose_name=u"图片,音频 资源地址", max_length=512)
    show_status = IntField(verbose_name=u"图片,音频 鉴定状态")  # 1:通过  2:屏蔽  3:鉴定中

    @classmethod
    def create_chat_message(cls, from_user_id, to_user_id, type, content, conversation_id, resource_url):

        # if not conversation_id:
        #     con = UserConversation.create_conversation_message(from_user_id, to_user_id, 2, 2)
        #     conversation_id = str(con.id)

        obj_ = cls()
        obj_.from_user_id = from_user_id
        obj_.to_user_id = to_user_id
        obj_.type = type
        obj_.content = content
        obj_.create_time = datetime.datetime.now()
        obj_.conversation_id = conversation_id
        obj_.resource_url = resource_url
        if int(type) == 2:
            obj_.show_status = 3
        else:
            obj_.show_status = 1
        obj_.save()

        # 改变会话状态:
        status = 0
        create_time = None
        conversation = UserConversation.objects.filter(id=conversation_id).first()
        con_type = conversation.type
        now = datetime.datetime.now()
        if con_type == 3:
            # 道具阶段状态
            conversation.update(set__type=2)
            conversation.update(set__wait_time=now)
        if con_type == 2:
            # 查看对方是否有此会话的回复: 如果有, 变成建立状态
            message = ChatMessage.objects.filter(conversation_id=conversation_id, from_user_id=to_user_id, to_user_id=from_user_id).first()
            if message:
                conversation.update(set__type=1)
                conversation.update(set__start_time=now)
                status = 1
                create_time = now

        if int(type) == 2:
            #  图片鉴定
            MessageSender.send_picture_detect(pic_url=resource_url, user_id=0, pic_channel=0, source=4, obj_id=str(obj_.id))

        return status, create_time, conversation_id


class UserConversation(Document):
    from_user_id = IntField(verbose_name=u"用户id")
    to_user_id = IntField(verbose_name=u"接收用户id")
    send_id = IntField(verbose_name=u"道具使用 用户id")
    create_time = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())
    type = IntField(verbose_name=u"会话状态")  # 1:建立  2:未建立  3:道具阶段  4:关闭
    start_time = DateTimeField(verbose_name=u"会话开始时间")
    stop_time = DateTimeField(verbose_name=u"会话关闭时间")
    wait_time = DateTimeField(verbose_name=u"等待开始时间")
    is_send_tool = IntField(verbose_name=u"是否使用道具")  # 1:使用  2:未使用
    tool_time_type = IntField(verbose_name=u"道具消耗的类型")  # 0:限时  1:永久
    stop_type = IntField(verbose_name=u"是否使用道具")  # 1:到时关闭  2:取消操作

    @classmethod
    def create_conversation_message(cls, from_user_id, to_user_id, type, is_send_tool):
        obj_ = cls()
        obj_.from_user_id = from_user_id
        obj_.to_user_id = to_user_id
        obj_.type = type
        obj_.is_send_tool = is_send_tool
        obj_.create_time = datetime.datetime.now()
        obj_.save()
        return obj_


    @classmethod
    def cancel(cls, conversation_id, from_user_id, to_user_id):
        conversation = cls.objects.filter(id=conversation_id, from_user_id=from_user_id, to_user_id=to_user_id).first()
        rever_conversation = cls.objects.filter(id=conversation_id, from_user_id=to_user_id, to_user_id=from_user_id).first()
        if conversation:
            conversation.update(set__type=4)
            conversation.update(set__stop_time=datetime.datetime.now())
            conversation.update(set__stop_type=2)

        if rever_conversation:
            rever_conversation.update(set__type=4)
            rever_conversation.update(set__stop_time=datetime.datetime.now())
            rever_conversation.update(set__stop_type=2)


