# coding=utf-8

from mongoengine import *



class PictureDetect(Document):

    PIC_CHANNEL = [
        (1, u"封面"),
        (2, u"用户头像")
    ]

    user = GenericReferenceField("User", verbose_name=u"用户")
    pic_url = StringField(verbose_name=u"图片url")
    pic_channel = IntField(verbose_name=u"图片场景")
    created_time = DateTimeField(verbose_name=u"创建时间")



class TextDetect(Document):

    TEXT_CHANNEL = [
        (1, u"昵称"),
        (2, u"个性签名")
    ]

    user = GenericReferenceField("User", verbose_name=u"用户")
    text = StringField(verbose_name=u"欲修改文本")
    text_channel = IntField(verbose_name=u"文本场景")
    created_time = DateTimeField(verbose_name=u"创建时间")
