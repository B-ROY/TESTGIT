#coding=utf-8
from mongoengine import *
import logging
from app.customer.models.user import *
from django.db import models
from base.settings import CHATPAMONGO


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)

class pushMsg(Document):
    Msg_type = [
        (1,u'文本消息'),
        (2,u'自定义消息')
    ]

    Pushor = IntField(verbose_name=u'发送者')
    Receiver = IntField(verbose_name=u'接收者')
    Message_type = IntField(verbose_name=u'私信类型',choices=Msg_type)
    title = StringField(verbose_name=u'标题', max_length=256,default='')
    content = StringField(verbose_name=u'内容', max_length=256,default='')
    links = StringField(verbose_name=u'链接', max_length=256,default='')
    pushTime = DateTimeField(verbose_name=u"发送时间", default=datetime.datetime.now())
    pushStatus = StringField(verbose_name=u'发送状态', max_length=256,default='')
    class Meta:
        app_label = "audio"
        verbose_name = u"推送消息历史记录"
        verbose_name_plural = verbose_name