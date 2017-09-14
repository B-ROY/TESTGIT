# -*- coding: utf-8 -*-

import hashlib
import urllib2
import urllib
import json
from django.conf import settings

class WePayConfig(object):
    MCHID = "1435567302"
    APPID = "wx9434b2be7019584d"
    KEY = "65b8b4b9242ebdcd645c9622138708ee"
    #TODO: 这个我使用的MCHID与APPID生成的秘钥，然后提交的微信电商平台的秘钥中进行修改,hmac.new("wx6cad6cc1ace6b7db","1361353202").hexdigest().upper()

class HeliDoPay():
    """
    合利宝下单接口
    """
    def __init__(self,  out_trade_no, total_fee, ip="", goods_name="buy", desc="buy"):
        self.P1_bizType = "AppPaySdk"
        self.P2_customerNumber = settings.helipay_customerNumber
        # self.P2_customerNumber = "C1800001347"
        self.P3_orderId = out_trade_no
        self.P4_goodsName = goods_name
        self.P5_orderAmount = float('%.2f' % (float(total_fee)/100))
        self.P6_currency = "CNY"
        self.P7_orderIp = ip
        self.P8_notifyUrl = settings.notify_url
        # self.P8_notifyUrl = "http://123.207.175.223/api/live/helipay/notify"
        self.P9_isRaw = "1"
        self.P10_appPayType = "WXPAY"
        self.P11_limitCreditPay = ""
        self.P12_deviceInfo = ""
        self.P13_appid = WePayConfig.APPID
        self.P14_desc = desc

    def get_sign(self):
        """生成签名"""
        sign_key = settings.helipay_sign_key
        # sign_key = "zP6UOCVkfm5DQQJR988eCsGhL1zrPJnF"
        sign_content = "&" + self.P1_bizType + "&" + self.P2_customerNumber + "&" + str(self.P3_orderId) + "&" \
                       + self.P4_goodsName + "&" + str(self.P5_orderAmount) + "&" + self.P6_currency + "&" \
                       + str(self.P7_orderIp) + "&" + self.P8_notifyUrl + "&" + self.P9_isRaw + "&" \
                       + self.P10_appPayType + "&" + self.P11_limitCreditPay + "&" + self.P12_deviceInfo + "&" \
                       + self.P13_appid + "&" + self.P14_desc + "&" + sign_key
        smd5 = hashlib.md5()
        smd5.update(sign_content)
        return smd5.hexdigest()

    def post_submit(self):

        url = settings.helipay_url
        # url = "http://test.trx.helipay.com/trx/app/interface.action"
        #定义要提交的数据
        postdata = dict(P1_bizType=self.P1_bizType, P2_customerNumber=self.P2_customerNumber, P3_orderId=self.P3_orderId, P4_goodsName=self.P4_goodsName,
                        P5_orderAmount=self.P5_orderAmount, P6_currency=self.P6_currency, P7_orderIp=self.P7_orderIp, P8_notifyUrl=self.P8_notifyUrl,
                        P9_isRaw=self.P9_isRaw, P10_appPayType=self.P10_appPayType, P11_limitCreditPay=self.P11_limitCreditPay, P12_deviceInfo=self.P12_deviceInfo,
                        P13_appid=self.P13_appid, P14_desc=self.P14_desc, sign=self.get_sign())
        #url编码
        postdata = urllib.urlencode(postdata)
        request = urllib2.Request(url, postdata)
        response = urllib2.urlopen(request).read()
        response_dict = json.loads(response)
        print str(response_dict)
        pay_info = json.loads(response_dict["rt8_payInfo"])

        prepay_id = pay_info["prepayid"]

        param_map = {
            'prepayid': prepay_id,
            'appid': pay_info["appid"],
            'partnerid': pay_info["partnerid"],
            'package': 'Sign=WXPay',
            'noncestr': pay_info["noncestr"],
            'timestamp': pay_info["timestamp"]
        }

        sort_param = sorted(
            [(key, value)for key, value in param_map.iteritems()],
            key=lambda x: x[0]
        )

        sign = pay_info["sign"]

        pay_params = '&'.join(['='.join(x) for x in sort_param])
        pay_params += "&sign=" + sign

        data = {
            "prepay_id": prepay_id,
            'pay_params': pay_params
        }
        return data


    @classmethod
    def verify_notice_sign(cls, rt1_customerNumber, rt2_orderId, rt3_systemSerial, rt4_status,
                           rt5_orderAmount, rt6_currency, rt7_timestamp, rt8_desc, sign):
        # sign_key = "zP6UOCVkfm5DQQJR988eCsGhL1zrPJnF"
        sign_key = settings.helipay_sign_key
        sign_content = "&" + rt1_customerNumber + "&" + rt2_orderId + "&" + rt3_systemSerial + "&" + rt4_status + "&" + rt5_orderAmount + "&" + rt6_currency + "&" + rt7_timestamp + "&" + rt8_desc + "&" + sign_key
        smd5 = hashlib.md5()
        smd5.update(sign_content)
        sign_gen = smd5.hexdigest()
        if sign_gen == sign:
            return True
        else:
            return False


import time
# helipay = HeliDoPay("1", 1000, ip="127.0.0.1")
# helipay.post_submit()
# import datetime
# print int(time.time())  p_20170808171155

