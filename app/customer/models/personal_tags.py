# coding=utf-8
from mongoengine import *
import logging
import datetime
from app.customer.models.user import *
from django.db import models
from base.settings import CHATPAMONGO


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class UserTags(Document):

    user_id = IntField(verbose_name=u'用户id', required=True)
    user_tags = ListField(StringField(verbose_name=u'标签', max_length=256, default=None))

    class Meta:
        app_label = "customer"
        verbose_name = u"用户标签"
        verbose_name_plural = verbose_name

    def normal_info(self):
        data = {}
        data['id'] = str(self.id)
        data['user_id'] = self.user_id
        data['user_tags'] = self.user_tags
        return data

    @classmethod
    def create_usertags(cls, user_id):
        try:
            user_tags = UserTags.check_user(user_id)
            if not user_tags:
                user_tags = UserTags(
                    user_id=user_id,
                    user_tags=None,
                )
                user_tags.save()
            else:
                return False
        except Exception,e:
            logging.error("create user tags error:{0}".format(e))
            return False
        return user_tags

    @classmethod
    def check_user(cls, user_id):
        try:
            user_tags = UserTags.objects.get(user_id=user_id)
        except UserTags.DoesNotExist:
            return None
        return user_tags

    @classmethod
    def update_usertags(cls, user_id, tag_str=None):
        try:
            user_tags = UserTags.check_user(user_id)
            if not user_tags:
                user_tags = UserTags.create_usertags(user_id)
            if tag_str == '':
                user_tags.user_tags = None
                user_tags.save()
                return True

            tag_list = tag_str.split(',')
            user_tags.user_tags = None
            for tag_name in tag_list:
                tag = TagTimes.objects.get(tag_name=tag_name)
                tag.tag_times += 1
                tag.save()
                user_tags.user_tags.append(tag_name)
                user_tags.save()

            # 技能标签 任务
            from app.customer.models.task import Task
            role = Task.get_role(user_id)
            task_identity = 0
            if role == 1:
                task_identity = 33
            elif role == 3:
                task_identity = 6
            elif role == 2:
                task_identity = 49
            if task_identity:
                MessageSender.send_do_task(user_id=user_id, task_identity=task_identity)


        except Exception,e:
            logging.error("update user tags error:{0}".format(e))
            return False
        return True

    @classmethod
    def get_usertags(cls, user_id):
        try:
            user_tags = UserTags.objects.filter(user_id=user_id)
            if user_tags:
                tags = user_tags.first().user_tags
                return tags
            else:
                return []
        except Exception,e:
            logging.error("get user tags error:{0}".format(e))
            return False


class TagTimes(Document):
    tag_name = StringField(verbose_name=u'标签名', max_length=256, required=True)
    tag_times = IntField(verbose_name=u'标签使用次数', default=0)

    class Meta:
        app_label = "customer"
        verbose_name = u"标签及使用次数"
        verbose_name_plural = verbose_name

    def normal_info(self):
        data = {}
        data['id'] = str(self.id)
        data['tag_name'] = self.tag_name
        data['tag_times'] = self.tag_times
        return data

    @classmethod
    def create_tagtimes(cls, tag_name):
        try:
            tag = TagTimes.objects.filter(tag_name=tag_name)
            if tag:
                return False
            else:
                tag = TagTimes(
                    tag_name=tag_name,
                    tag_times=0,
                )
                tag.save()
        except Exception,e:
            logging.error("create tag times error:{0}".format(e))
            return False
        return True

    @classmethod
    def get_taglist(cls):
        tags = TagTimes.objects.all().order_by('-tag_times')
        return tags
        #return tags
