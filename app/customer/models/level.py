# coding=utf-8

from django.db import models
import logging
import datetime
# from app.customer.models.user import User
from wi_model_util.imodel import *
from mongoengine import *
from base.settings import CHATPAMONGO


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class Level(Document):
    STATUS = [
        (0, u'未使用'),
        (1, u'使用'),
    ]

    id = IntField(primary_key=True)
    name = StringField(max_length=32, verbose_name=u'名称')
    grade = IntField(verbose_name=u'等级')
    status = IntField(verbose_name=u'状态', choices=STATUS)
    experience = IntField(verbose_name=u'等级需要经验值')
    created_time = DateTimeField(verbose_name=u"添加时间", default=datetime.datetime.now())

    class Meta:
        app_label = "customer"
        verbose_name = u"等级"
        verbose_name_plural = verbose_name

    def normal_info(self):
        return {
            "name":self.name,
            "grade":self.grade,
            "experience":self.experience,
        }

    @classmethod
    def create(cls, grade, name, experience, status=1):
        try:
            _obj = cls()
            _obj.id = cls.objects.all().count() + 1
            _obj.name = name
            _obj.grade = grade
            _obj.experience = experience
            _obj.created_time = datetime.datetime.now()
            _obj.status = status

            _obj.save()
            return _obj
        except Exception, e:
            logging.error("create Level error:{0}".format(e))
        return ''

    @classmethod
    def update(cls, obj_id, grade, name, experience, status=1):
        try:
            _obj = cls.objects.get(id=obj_id)
            _obj.name = name
            _obj.grade = grade
            _obj.experience = experience
            _obj.status = status

            _obj.save()
            return _obj
        except Exception, e:
            logging.error("update Level error:{0}".format(e))
        return ''

    def next_level(self):
        next_level_grade = self.grade + 1
        try:
            next_level = Level.objects.get(grade=next_level_grade)
            return next_level
        except Level.DoesNotExist:
            return None
        #return get_object_or_none(Level, grade=self.grade + 1)

    def up_level(self):
        up_level_grade = self.grade - 1
        try:
            up_level = Level.objects.get(grade=up_level_grade)
            return up_level
        except Level.DoesNotExist:
            return None
        #return get_object_or_none(Level, grade=self.grade - 1)

    #@classmethod
    #def last_level(cls):
    #    return cls.objects.aggregate(last_level=models.Max('grade'))["last_level"] or 0

    @classmethod
    def last_level(cls):
        return cls.objects.all().count()
        # qs = cls.objects.raw("select max(grade) from customer_level ")
        # for _max in qs or []:
        #     return _max
        #
        # return 1


# class LevelRecord(models.Model):

#     user = models.ForeignKey(User, verbose_name=u'用户')
#     from_level = models.IntegerField(verbose_name=u'从哪一级')
#     to_level = models.IntegerField(verbose_name=u'升级到哪一集')
#     created_time = models.DateTimeField(auto_now_add=True, verbose_name=u"关注时间", db_index=True)


