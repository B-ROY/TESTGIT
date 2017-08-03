#coding=utf-8
from mongoengine import *
import logging
import datetime
from app.customer.models.user import *
from django.db import models
from app.picture.models.picture import PictureInfo
from base.settings import CHATPAMONGO


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class CommentInfo(Document):

    STATUS = [
        (0, u'显示'),
        (1, u'删除'),
    ]

    user_id = IntField(verbose_name=u'评论用户id', required=True)    # A发表评论
    picture_id = StringField(verbose_name=u'图片id', max_length=1024, default=None)
    reply_id = IntField(verbose_name=u'回复人id', default=0)    # B评论回复了A
    comment = StringField(verbose_name=u'评论内容', max_length=1024, default=None)
    like_count = IntField(verbose_name=u'点赞数', default=0)
    created_at = DateTimeField(verbose_name=u'评论时间', default=None)
    status = IntField(verbose_name=u'状态', default=0, choices=STATUS)

    class Meta:
        app_label = "comment"
        verbose_name = u"图片评论"
        verbose_name_plural = verbose_name

    def normal_info(self):
        data = {}
        data['id'] = str(self.id)
        data['user_id'] = self.user_id
        data['picture_id'] = self.picture_id
        data['reply_id'] = self.reply_id
        data['comment'] = self.comment
        data['like_count'] = self.like_count
        data['created_at'] = datetime_to_timestamp(self.created_at)
        data['status'] = self.status
        return data

    @classmethod
    def create_comment(cls, user_id, picture_id, reply_id=0, created_at=None, comment=None):
        try:
            comment = CommentInfo(
                user_id=user_id,
                picture_id=picture_id,
                reply_id=reply_id,
                created_at=created_at,
                comment=comment,
                like_count=0,
                status=0,
            )
            comment.save()
        except Exception,e:
            logging.error("create comment error:{0}".format(e))
            return False
        return comment.id

    @classmethod
    def comment_view(cls, comment_id):
        try:
            comment = CommentInfo.objects.get(id=comment_id)
        except Exception,e:
            logging.error("comment view error:{0}".format(e))
            return False
        return comment

    @classmethod
    def get_comment_user(cls, user_id):
        try:
            user = User.objects.get(id=user_id)
        except Exception,e:
            logging.error("get comment user error:{0}".format(e))
            return False
        return user

