# coding=utf-8

from mongoengine import *
import datetime


class ReportText(Document):
    DELETE_STATUS = [
        (0, "已删除"),
        (2, "正在使用")
    ]

    label = IntField(verbose_name=u"标签", unique=True)
    text = StringField(verbose_name=u"举报文案")
    report_type = IntField(verbose_name=u"举报类型")
    create_time = DateTimeField(verbose_name=u"创建时间")
    delete_status = IntField(verbose_name=u"是否删除", choices=DELETE_STATUS)

    @classmethod
    def create_report_text(cls, label, message,report_type):
        obj_ = cls()
        obj_.label = label
        obj_.text = message
        obj_.report_type = report_type
        obj_.create_time = datetime.datetime.now()
        obj_.save()

    @classmethod
    def get_report_texts(cls, report_type):
        return cls.objects.filter(report_type=report_type)


    @classmethod
    def delete_report_text(cls):
        # todo
        pass

    @classmethod
    def update_report_text(cls):
        #todo
        pass


class ReportRecord(Document):

    REPORT_TYPE = [
        (0, u"个人主页"),
        (1, u"私信聊天也"),
        (2, u"通话页主播举报用户"),
        (3, u"通话也用户举报主播")
    ]

    label = IntField(verbose_name=u"标签")
    report_type = IntField(verbose_name=u"举报类型", choices=REPORT_TYPE)
    text = StringField(verbose_name=u"举报文字")
    report_time = DateTimeField(verbose_name=u"举报时间")
    pic_url = StringField(verbose_name=u"举报图片url")
    file_id = StringField(verbose_name=u"文件ID")
    user_id = StringField(verbose_name=u"举报人ID")
    report_id = StringField(verbose_name=u"被举报人ID")

    @classmethod
    def create_report_record(cls, label, report_type, text, pic_url, file_id, user_id, report_id):
        obj_ = cls()
        obj_.label = label
        obj_.report_id = report_id
        obj_.text = text
        obj_.report_time = datetime.datetime.now()
        obj_.pic_url = pic_url
        obj_.file_id = file_id
        obj_.user_id =user_id
        obj_.report_type = report_type
        obj_.save()


    @classmethod
    def delete_report_record(cls):
        #todo 删除乱举报等等
        pass



























