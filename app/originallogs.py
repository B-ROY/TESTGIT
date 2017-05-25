# coding=utf-8

from base.settings import CHATPAMONGO
from base.settings import CHATPALOGSMONGO
from mongoengine import *

connect(CHATPALOGSMONGO.db, alias="liaopa_stat", host=CHATPALOGSMONGO.host, port=CHATPALOGSMONGO.port, username=CHATPALOGSMONGO.username,password=CHATPALOGSMONGO.password)

class OriginalLog(Document):

    ip = StringField(verbose_name=u"用户ip",max_length=32)
    year = IntField(verbose_name=u"年")
    month = IntField(verbose_name=u"月")
    day = IntField(verbose_name=u"日")
    time = StringField(verbose_name=u"访问接口时间",max_length=32)
    user_id = IntField(verbose_name=u"用户id")
    uri = StringField(verbose_name=u"接口uri")
    args = DictField(verbose_name=u"接口参数")
    guid = StringField(verbose_name=u"设备号")
    status_code = IntField(verbose_name=u"接口状态吗")
    request_time = FloatField(verbose_name=u"接口响应时间")
    platform = StringField(verbose_name=u"平台")
    app_name = StringField(verbose_name=u"应用名")
    version_name = StringField(verbose_name=u"应用版本号")
    os = StringField(verbose_name=u"操作系统版本")
    phone_name = StringField(verbose_name=u"手机名称")
    channel = StringField(verbose_name=u"渠道")
    
    meta= {"db_alias": "liaopa_stat"}





