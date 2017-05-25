# coding=utf-8
from django.db import models
import datetime
from mongoengine import *
from base.settings import CHATPAMONGO


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class WeChatWithdrawResult(models.Model):
    """
    微信企业付款业务 https://pay.weixin.qq.com/wiki/doc/api/tools/mch_pay.php?chapter=14_2
    """
    return_code = StringField(verbose_name=u'返回状态码', max_length=16, default='')
    return_msg = StringField(verbose_name=u'返回信息', max_length=128, default='')

    # 以下字段在return_code为SUCCESS的时候有返回
    mch_appid = StringField(verbose_name=u'商户appid', max_length=32, default='')
    mchid = StringField(verbose_name=u'商户号', max_length=32, default='')
    device_info = StringField(verbose_name=u'设备号', max_length=32, default='')
    nonce_str = StringField(verbose_name=u'随机字符串', max_length=32, default='')
    result_code = StringField(verbose_name=u'业务结果', max_length=16, default='')
    err_code = StringField(verbose_name=u'错误代码', max_length=32, default='')
    err_code_des = StringField(verbose_name=u'错误代码描述', max_length=128, default='')

    # 以下字段在return_code 和result_code都为SUCCESS的时候有返回
    partner_trade_no = StringField(verbose_name=u'商户订单号', max_length=32, default='')
    payment_no = StringField(verbose_name=u'微信订单号', max_length=64, default='')
    payment_time = StringField(verbose_name=u'微信支付成功时间', max_length=32, default='')

    class Meta:
        app_label = "customer"
        verbose_name = u"微信提现记录"
        verbose_name_plural = verbose_name



    @classmethod
    def save_record(cls, withdraw_callback):
        obj = cls()
        for key in withdraw_callback:
            if hasattr(obj, key):
                value = withdraw_callback[key]
                if value:
                    setattr(obj, key, value or '')
        obj.save()

