# coding=utf-8
from django.db import models
import logging
from app.customer.models.user import User
import datetime
from api.apiexceptions.apiexception import *
from xml.dom.minidom import parse
from xml.etree.ElementTree import XML
import xml.dom.minidom
import re
# https://docs.python.org/2/library/xml.etree.elementtree.html
from app.customer.models.account import Account, WithdrawRequest
from django.db import transaction
from mongoengine import *
from base.settings import CHATPAMONGO


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


# 从钱到引力币，从引力币到钱
class WeChatFillNotice(Document):
    out_trade_no = StringField(verbose_name=u"out_trade_no", max_length=32)
    appid = StringField(verbose_name=u"appid", max_length=32)
    bank_type = StringField(verbose_name=u"bank_type", max_length=32)
    cash_fee = IntField(verbose_name=u"cash_fee")
    fee_type = StringField(verbose_name=u"fee_type", max_length=32)
    is_subscribe = StringField(verbose_name=u"is_subscribe", max_length=32)
    mch_id = StringField(verbose_name=u"mch_id", max_length=32)
    nonce_str = StringField(verbose_name=u"nonce_str", max_length=32)
    device_info = StringField(verbose_name=u"device_info", max_length=32)
    openid = StringField(verbose_name=u"openid", max_length=32)
    result_code = StringField(verbose_name=u"result_code", max_length=32)
    return_code = StringField(verbose_name=u"return_code", max_length=32)
    sign = StringField(verbose_name=u"sign", max_length=32)
    time_end = StringField(verbose_name=u"time_end", max_length=32)
    total_fee = StringField(verbose_name=u"total_fee", max_length=32)
    trade_type = StringField(verbose_name=u"trade_type", max_length=32)
    transaction_id = StringField(verbose_name=u"transaction_id", max_length=32)
    err_code_des = StringField(verbose_name=u"transaction_id", max_length=128)
    attach = StringField(verbose_name=u"transaction_id", max_length=128)
    coupon_fee = IntField(verbose_name=u"transaction_id")
    created_at = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())

    class Meta:
        app_label = "customer"
        verbose_name = u"微信回调信息"
        verbose_name_plural = verbose_name

    @classmethod
    def create_order(cls, xml):
        root = xml
        wcn = WeChatFillNotice()

        wcn.app_id = root.find('appid').text
        wcn.out_trade_no = root.find('out_trade_no').text
        wcn.created_at = datetime.datetime.now()
        bank_type = root.find('bank_type')

        if bank_type is not None:
            wcn.bank_type = bank_type.text

        cash_fee = root.find('cash_fee')
        if cash_fee is not None:
            wcn.cash_fee = root.find('cash_fee').text

        fee_type = root.find('fee_type')
        if fee_type is not None:
            wcn.fee_type = fee_type.text

        is_subscribe = root.find('is_subscribe')
        if is_subscribe is not None:
            wcn.is_subscribe = is_subscribe.text

        wcn.mch_id = root.find('mch_id').text
        wcn.nonce_str = root.find('nonce_str').text

        device_info = root.find('device_info')
        if device_info is not None:
            wcn.device_info = device_info.text

        result_code = root.find('result_code')
        if result_code is not None:
            wcn.result_code = result_code.text

        openid = root.find('openid')
        if openid is not None:
            wcn.openid = openid.text

        return_code = root.find('return_code')
        if return_code is not None:
            wcn.return_code = return_code.text

        wcn.sign = root.find('sign').text

        time_end = root.find('time_end')
        if time_end is not None:
            wcn.time_end = time_end.text

        trade_type = root.find('trade_type')
        if trade_type is not None:
            wcn.trade_type = trade_type.text

        transaction_id = root.find('transaction_id')
        if transaction_id is not None:
            wcn.transaction_id = transaction_id.text

        err_code_des = root.find('err_code_des')
        if err_code_des is not None:
            wcn.err_code_des = err_code_des.text

        attach = root.find('attach')
        if attach is not None:
            wcn.attach = root.find('attach').text

        coupon_fee = root.find('coupon_fee')
        if coupon_fee is not None:
            wcn.coupon_fee = coupon_fee.text

        return cls.fill_in(wcn)

    @classmethod
    # @transaction.commit_on_success
    def fill_in(cls, wcn):
        print "transcation start"
        success = Account.fill_in(wcn.out_trade_no)

        if success:
            print u"success"
            wcn.save()
        else:
            raise Exception("trade order error")

        return True


class AppleVerify(Document):
    out_trade_no = StringField(verbose_name=u"out_trade_no", max_length=32)
    pay_receipt = StringField(verbose_name=u"pay_receipt", max_length=65535)
    created_at = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())
    status = IntField(verbose_name="status", default=0)

    class Meta:
        app_label = "customer"
        verbose_name = u"苹果支付回调"
        verbose_name_plural = verbose_name

    @classmethod
    def create_verify(cls, out_trade_no, pay_receipt):

        rec = cls.objects.filter(pay_receipt=pay_receipt).all()
        if len(rec) > 0:
            return -1
        av = cls.objects.filter(out_trade_no=out_trade_no).first()
        if not av:
            av = cls(out_trade_no=out_trade_no, pay_receipt=pay_receipt, created_at=datetime.datetime.now(), status=0)

        av.save()
        return av

    def is_verified(self):
        return self.status == 1

    def verified(self):
        self.stauts = 1
        self.save()

    # @transaction.commit_on_success
    def fill_in(self, receipt):
        print "transcation start"

        if self.is_verified():
            raise Exception("verified")

        avr = AppleVerifyResult(out_trade_no=self.out_trade_no)
        avr.bid = receipt.get('bid', '')
        avr.bvrs = receipt.get('bvrs', '')
        avr.item_id = receipt.get('item_id', '')
        avr.original_purchase_date = receipt.get('original_purchase_date', '')
        avr.original_purchase_date_ms = receipt.get('original_purchase_date_ms', '')
        avr.original_purchase_date_pst = receipt.get('original_purchase_date_pst', '')
        avr.original_transaction_id = receipt.get('original_transaction_id', '')
        avr.product_id = receipt.get('product_id', '')
        avr.purchase_date = receipt.get('purchase_date', '')
        avr.purchase_date_ms = receipt.get('purchase_date_ms', '')
        avr.purchase_date_pst = receipt.get('purchase_date_pst', '')
        avr.quantity = receipt.get('quantity', '')
        avr.transaction_id = receipt.get('transaction_id', '')
        avr.created_at = datetime.datetime.now()
        avr.save()

        success = Account.fill_in(self.out_trade_no)

        if success:
            print u"success"
            self.verified()
        else:
            raise Exception("trade order error")

        return True


class AppleVerifyResult(Document):
    out_trade_no = StringField(verbose_name=u"out_trade_no", max_length=32)
    bid = StringField(verbose_name=u"bid", max_length=32)
    bvrs = StringField(verbose_name=u"bid", max_length=32)
    item_id = StringField(verbose_name=u"bid", max_length=32)
    original_purchase_date = StringField(verbose_name=u"bid", max_length=32)
    original_purchase_date_ms = StringField(verbose_name=u"bid", max_length=32)
    original_purchase_date_pst = StringField(verbose_name=u"bid", max_length=64)
    original_transaction_id = StringField(verbose_name=u"bid", max_length=32)
    product_id = StringField(verbose_name=u"bid", max_length=32)
    purchase_date = StringField(verbose_name=u"bid", max_length=32)
    purchase_date_ms = StringField(verbose_name=u"bid", max_length=32)
    purchase_date_pst = StringField(verbose_name=u"bid", max_length=64)
    quantity = StringField(verbose_name=u"bid", max_length=32)
    transaction_id = StringField(verbose_name=u"bid", max_length=32)
    created_at = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())

    class Meta:
        app_label = "customer"
        verbose_name = u"苹果支付回调"
        verbose_name_plural = verbose_name


class WexinJSVerify(Document):
    out_trade_no = StringField(verbose_name=u"out_trade_no", max_length=32)
    pay_receipt = StringField(verbose_name=u"pay_receipt")
    created_at = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())
    status = IntField(verbose_name="status", default=0)

    class Meta:
        app_label = "customer"
        verbose_name = u"苹果支付回调"
        verbose_name_plural = verbose_name

    @classmethod
    def create_verify(cls, out_trade_no, pay_receipt):

        av = cls.objects.filter(out_trade_no=out_trade_no).first()
        if not av:
            av = cls(out_trade_no=out_trade_no, pay_receipt=pay_receipt, created_at=datetime.datetime.now(), status=0)

        av.save()
        return av

    def is_verified(self):
        return self.status == 1

    def verified(self):
        self.stauts = 1
        self.save()

    # @transaction.commit_on_success
    def fill_in(self, receipt):
        print "transcation start"

        if self.is_verified(self):
            raise Exception("verified")

        success = Account.fill_in(self.out_trade_no)

        if success:
            print u"success"
            self.verified()
        else:
            raise Exception("trade order error")

        return True


class WeChatWithdrawNotice(Document):
    partner_trade_no = StringField(verbose_name=u"partner_trade_no", max_length=32)
    return_code = StringField(verbose_name=u"return_code", max_length=32)
    return_msg = StringField(verbose_name=u"return_msg", max_length=32)
    mch_appid = StringField(verbose_name=u"mch_appid", max_length=32)
    mchid = StringField(verbose_name=u"mchid", max_length=32)
    device_info = StringField(verbose_name=u"device_info", max_length=32)
    nonce_str = StringField(verbose_name=u"nonce_str", max_length=32)
    payment_no = StringField(verbose_name=u"payment_no", max_length=32)
    created_at = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())

    class Meta:
        app_label = "customer"
        verbose_name = u"提现回调"
        verbose_name_plural = verbose_name

    @classmethod
    def create_order(cls, xml):
        root = xml
        wcn = WeChatWithdrawNotice()

        wcn.created_at = datetime.datetime.now()

        partner_trade_no = root.find('partner_trade_no')
        if partner_trade_no is not None:
            wcn.partner_trade_no = partner_trade_no.text

        return_code = root.find('return_code')
        if return_code is not None:
            wcn.return_code = return_code.text

        return_msg = root.find('return_msg')
        if return_msg is not None:
            wcn.return_msg = return_msg.text

        mch_appid = root.find('mch_appid')
        if mch_appid is not None:
            wcn.mch_appid = mch_appid.text

        mchid = root.find('mchid')
        if mchid is not None:
            wcn.mchid = mchid.text

        device_info = root.find('device_info')
        if device_info is not None:
            wcn.device_info = device_info.text

        nonce_str = root.find('nonce_str')
        if nonce_str is not None:
            wcn.nonce_str = nonce_str.text

        payment_no = root.find('payment_no')
        if payment_no is not None:
            wcn.payment_no = payment_no.text

        return cls.withdraw_fill_in(wcn)

    @classmethod
    def withdraw_fill_in(cls, wcn):
        print "withdraw start"
        success = WithdrawRequest.withdraw_fill_in(wcn.partner_trade_no)

        if success:
            print u"success"
            wcn.save()
        else:
            raise Exception("withdraw fill in error")
        return True


class AlipayFillNotice(Document):

    seller_email = StringField(verbose_name=u"卖家支付宝账号")
    app_id = StringField(verbose_name=u"支付包id")
    buyer_pay_amount = FloatField(verbose_name=u"买家付款金额， 单位（分）")
    buyer_logon_id = StringField(verbose_name=u"买件支付宝账号")
    gmt_create = StringField(verbose_name=u"交易创建时间")
    out_trade_no = StringField(verbose_name=u"商户订单号")
    trade_status = StringField(verbose_name=u"交易状态")
    gmt_payment = StringField(verbose_name=u"卖家付款时间")
    trade_no = StringField(verbose_name=u"支付包交易号")
    seller_id = StringField(verbose_name=u"卖家支付宝用户号")
    total_amount = FloatField(verbose_name=u"订单金额")
    notify_time = StringField(verbose_name=u"通知时间")
    notify_id = StringField(verbose_name=u"通知ID")
    buyer_id = StringField(verbose_name=u"买家支付宝用户号")



    class Meta:
        app_label = "customer"
        verbose_name = u"微信回调信息"
        verbose_name_plural = verbose_name

    @classmethod
    def create_order(cls, notice_dict):
        acn = AlipayFillNotice()
        acn.seller_email = notice_dict.get("seller_email")
        acn.app_id = notice_dict.get("app_id")
        acn.buyer_pay_amount = float(notice_dict.get("buyer_pay_amount"))
        acn.buyer_logon_id = notice_dict.get("buyer_logon_id")
        acn.gmt_create = notice_dict.get("gmt_create")
        acn.out_trade_no = notice_dict.get("out_trade_no")
        acn.trade_status = notice_dict.get("trade_status")
        acn.gmt_payment = notice_dict.get("gmt_payment")
        acn.trade_no = notice_dict.get("trade_no")
        acn.seller_id = notice_dict.get("seller_id")
        acn.total_amount = float(notice_dict.get("total_amount"))
        acn.notify_time = notice_dict.get("notify_time")
        acn.notify_id = notice_dict.get("notify_id")
        acn.buyer_id = notice_dict.get("notify_id")

        return cls.fill_in(acn)

    @classmethod
    # @transaction.commit_on_success
    def fill_in(cls, acn):
        print "transcation start"
        success = Account.fill_in(acn.out_trade_no)

        if success:
            print u"success"
            acn.save()
        else:
            raise Exception("trade order error")

        return True


class GooglePayVeriry(Document):

    out_trade_no = StringField(verbose_name=u"商户订单号")
    google_order_id = StringField(verbose_name=u"Google订单号")
    notice_time = DateTimeField(verbose_name=u"通知时间")
    buy_time = DateTimeField(verbose_name=u"购买时间")

    @classmethod
    def create_order(cls, verify_dict):
        gpv = GooglePayVeriry()
        gpv.out_trade_no = verify_dict.get("order_id")
        gpv.google_order_id = verify_dict.get("google_order_id")
        gpv.notice_time = datetime.datetime.now()
        gpv.buy_time = verify_dict.get("buy_time")

        return cls.fill_in(gpv)

    @classmethod
    def fill_in(cls, gpv):
        success = Account.fill_in(gpv.out_trade_no)
        if success:
            print u"google pay success"
            gpv.save()
        else:
            raise Exception("trado order error")
        return True
