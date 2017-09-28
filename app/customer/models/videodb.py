# coding=utf-8

import datetime
import logging

from base.settings import CHATPAMONGO
from django.conf import settings
from mongoengine import *


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class VideoDb(Document):
    status = IntField(verbose_name=u'状态')  # 1.展示 2.未展示
    video_id = StringField(verbose_name=u'视频id')
    moment_id = StringField(verbose_name=u'动态id')
    video_type = IntField(verbose_name=u'视频类型')  # 1.私房视频 2.封面视频
    anchor_id = IntField(verbose_name=u'播主id')  # 播主id
    video_price = IntField(verbose_name=u'视频价格')  # 视频价格
    video_url = StringField(verbose_name=u'视频地址')  # 视频地址
    create_time = DateTimeField(verbose_name=u'入库时间')
    cover_url = StringField(verbose_name=u'视频封面地址') #视频地址

    @classmethod
    def create(cls,video_id,moment_id,video_type,anchor_id,video_price,video_url,cover_url):
        obj_ = cls()
        obj_.status = 2
        obj_.video_id = video_id
        obj_.moment_id = moment_id
        obj_.video_type = video_type
        obj_.anchor_id = anchor_id
        obj_.video_price = video_price
        obj_.video_url = video_url
        obj_.cover_url = cover_url
        obj_.create_time = datetime.datetime.now()
        obj_.save()


class VideoShow(Document):
    create_time = DateTimeField(verbose_name=u'展示时间')
    sort = IntField(verbose_name=u'排序')
    video_id = StringField(verbose_name=u'视频id')
    moment_id = StringField(verbose_name=u'动态id')
    video_type = IntField(verbose_name=u'视频类型')  # 1.私房视频 2.封面视频
    anchor_id = IntField(verbose_name=u'播主id')  # 播主id
    video_price = IntField(verbose_name=u'视频价格')  # 视频价格
    video_url = StringField(verbose_name=u'视频地址')  # 视频地址
    cover_url = StringField(verbose_name=u'视频封面地址') #视频地址

