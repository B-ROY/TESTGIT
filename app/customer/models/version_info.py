#!/usr/bin/env python
# -*- coding: utf-8 -*-  
__author__ = 'zen@heydo.tv'
__date__ = '2016-06-21'

import logging
import datetime
from django.db import models
from mongoengine import *
from base.settings import CHATPAMONGO


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class VersionInfo(Document):
    SWITCH_PlATFORM = [
        (u'IOS', u'IOS'),
        (u'ANDROID', u'ANDROID'),
        (u'H5', u'H5'),
        (u'WEB', u'WEB'),
        (u'ALL', u'ALL'),
    ]

    DELETE_STATUS = [
        (0, u'正常'),
        (1, u'删除'),
    ]

    app_name = StringField(verbose_name=u'app名称', max_length=64)
    version = StringField(verbose_name=u'客户端当前版本', max_length=255, default=0)
    download_url = StringField(max_length=255, verbose_name=u'下载地址', default='')
    platform = StringField(verbose_name=u'平台,逗号分隔', max_length=255, default=0)
    created_time = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())
    upgrade_type = StringField(max_length=255, verbose_name=u'升级类型')
    delete_status = IntField(verbose_name=u'删除状态', choices=DELETE_STATUS, default=0)
    version_code = IntField(verbose_name=u'版本号',default=0)
    upgrade_info = StringField(max_length=65535, verbose_name=u'升级描述')
    channel = StringField(max_length=128, verbose_name=u"渠道名称")

    def __unicode__(self):
        return self.version

    class Meta:
        app_label = "customer"
        verbose_name = u"版本信息"
        verbose_name_plural = verbose_name

    @classmethod
    def create(cls, app_name, version, platform, upgrade_type, download_url='', version_code=0, upgrade_info='', channel=""):
        try:
            obj = cls()
            obj.app_name = app_name
            obj.version = version
            obj.platform = platform.upper()
            obj.upgrade_type = upgrade_type
            obj.download_url = download_url
            obj.version_code = version_code
            obj.upgrade_info = upgrade_info
            obj.created_time = datetime.datetime.now()
            obj.channel = channel
            obj.save()
            return obj
        except Exception, e:
            logging.error("create Switcher error:{0}".format(e))

    @classmethod
    def update(cls, obj_id, app_name, version, platform, upgrade_type, download_url='', version_code=0,upgrade_info='', channel=""):
        try:
            obj = cls.objects.get(id=obj_id)
            obj.app_name = app_name
            obj.version = version
            obj.platform = platform.upper()
            obj.upgrade_type = upgrade_type
            obj.download_url = download_url
            obj.version_code = version_code
            obj.upgrade_info = upgrade_info
            obj.channel = channel
            obj.save()
            return obj
        except Exception, e:
            logging.error("create Switcher error:{0}".format(e))

    @classmethod
    def get_all(cls):
        return cls.objects.filter(delete_status=0)

    @classmethod
    def get_version_info(cls, platform, app_name, channel=None):
        platform = platform.upper()
        if channel:
            version_info = cls.objects.filter(app_name=app_name, platform=platform, channel=channel).order_by(
                "-version").first()
        else:
            version_info = cls.objects.filter(app_name=app_name, platform=platform).order_by(
                "-version").first()

        """之前代码， 留作参考， 一会删掉
        version_infos = cls.get_all()

        for version_info in version_infos:
            if platform.upper() in version_info.platform and app_name == version_info.app_name:
                return version_info
        """
        return version_info

    def format_version_info(self):
        return {
            'app_name': self.app_name,
            'version': self.version,
            'upgrade_type': self.upgrade_type,
            'download_url': self.download_url,
            'version_code': self.version_code,
            'channel':self.channel,
            'desc': self.upgrade_info
        }


class VersionUpdate(Document):

    PLATFORM = [
        (0, "ANDROID"),
        (1, "IOS")
    ]


    platform = IntField(verbose_name=u"平台")
    app_name = StringField(verbose_name=u"应用名称")
    channel = StringField(verbose_name=u"渠道")
    min_version = StringField(verbose_name=u"应用版本")
    current_version = StringField(verbose_name=u"当前版本")
    download_url = StringField(verbose_name=u"下载地址")

    @classmethod
    def create_version_update(cls, platform, app_name, channel, min_version, current_version):
        version_update_item = cls.objects(platform=platform, app_name=app_name, channel=channel, min_version=min_version, current_version=current_version)
        version_update_item.save()
        pass

    @classmethod
    def get_version_info(cls,platform, app_name, channel, min_version, current_version):
        platform = platform.upper()
        if platform == "ANDROID":
            platform_num = 0
        else:
            platform_num = 1

        if platform_num == 0:#安卓


            pass
        elif platform_num == 1:#ios
            version_info = cls.objects.filter(app_name=app_name, channel=channel).first()

            if not version_info:
                app_name = "liaoai"#默认查询liaoai


            pass


        pass



class VersionReview(Document):
    platform = IntField(verbose_name=u"平台")
    app_name = StringField(verbose_name=u"应用名称")
    channel = StringField(verbose_name=u"渠道")
    version = StringField(verbose_name=u"应用版本")

    @classmethod
    def create_version_review(cls, platform, app_name, channel, version):
        version_review_item = cls(platform=platform, app_name=app_name, channel=channel,version=version)
        version_review_item.save()

    """
        check the app whether need review
    
    """
    def check_review(cls, platform, app_name, channel, version):





        pass



