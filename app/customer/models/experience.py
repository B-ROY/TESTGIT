# coding=utf-8

from django.db import models
from app.customer.models.user import User
from base.core.util.dateutils import int_days
import logging
import datetime
from mongoengine import *
from base.settings import CHATPAMONGO

connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class UserExperienceType(Document):
    STATUS = [
        (0, u'未使用'),
        (1, u'使用'),
    ]

    name = StringField(max_length=32, verbose_name=u'名称')
    status = IntField(verbose_name=u'状态', choices=STATUS)

    identifier = StringField(max_length=32, verbose_name=u'前端标识符')
    experience = IntField(verbose_name=u'改变的经验值')

    limit_count = IntField(verbose_name=u'每天限制的次数')

    created_time = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())

    class Meta:
        app_label = "customer"
        verbose_name = u"经验上报种类"
        verbose_name_plural = verbose_name

    @classmethod
    def create(cls, identifier, name, experience, limit_count=0, status=1):
        try:
            _obj = cls()
            _obj.name = name
            _obj.identifier = identifier
            _obj.experience = experience
            _obj.limit_count = limit_count
            _obj.status = status
            _obj.created_time = datetime.datetime.now()

            _obj.save()
            return _obj
        except Exception, e:
            logging.error("create UserExperienceType error:{0}".format(e))
        return ''

    @classmethod
    def update(cls, obj_id, identifier, name, experience, limit_count=0, status=1):
        try:
            _obj = cls.objects.get(id=obj_id)
            _obj.name = name
            _obj.identifier = identifier
            _obj.experience = experience
            _obj.limit_count = limit_count
            _obj.status = status

            _obj.save()
            return _obj
        except Exception, e:
            logging.error("update UserExperienceType error:{0}".format(e))
        return ''


class UserExperienceLog(Document):
    STATUS = [
        (0, u'未使用'),
        (1, u'使用'),
    ]

    ex_type = GenericReferenceField("UserExperienceType", verbose_name=u'增加经验类型')
    user = GenericReferenceField("User", verbose_name=u'上传用户')
    liveRoom = GenericReferenceField("LiveRoom", verbose_name=u'直播房间')

    experience = IntField(verbose_name=u'改变的经验值')

    created_time = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())

    idate = IntField(verbose_name=u'日期')


    class Meta:
        app_label = "customer"
        verbose_name = u"经验上报日志"
        verbose_name_plural = verbose_name

    @classmethod
    def i_count(cls,ex_type,user_id):
        return cls.objects.filter(ex_type=ex_type,idate=int_days(),user__id=user_id).count()



    @classmethod
    def create(cls, ex_type, user, liveRoom_id, experience):
        try:
            _obj = cls()
            _obj.ex_type = ex_type
            _obj.user = user
            _obj.liveRoom_id = liveRoom_id
            _obj.experience = experience
            _obj.idate = int_days()
            _obj.created_time = datetime.datetime.now()

            _obj.save()
            return _obj
        except Exception, e:
            logging.error("create UserExperienceType error:{0}".format(e))
        return ''


class ExperienceManage(object):
    @classmethod
    def add_experience(cls, from_user, ex_type, room=""):
        success = 0
        try:
            _experience = ex_type.experience

            if UserExperienceLog.i_count(ex_type,from_user.id) <= ex_type.limit_count:
                from_user.add_experience(_experience)
                success = 1001
                # experience log
                UserExperienceLog.create(ex_type, from_user, room, _experience)
                success = 1002
            return success
        except:
            return success

    @classmethod
    def operate_experience(cls, from_user, ex_type):
        success = 0
        try:
            _experience = ex_type.experience
            from_user.add_experience(_experience)
            UserExperienceLog.create(ex_type, from_user, "", _experience)
            success = 1002
            return success
        except ExperienceManage, e:
            return success



