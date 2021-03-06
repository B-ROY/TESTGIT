# -*- coding: utf-8 -*-
__author__ = 'zen'
import hashlib
import urllib2
import random
import string
import time
import copy
import xml.etree.ElementTree as ET
from api.apiexceptions import apiexception
import logging
from base.core.util.dateutils import int_days
from django.conf import settings

# doc -- https://pay.weixin.qq.com/wiki/doc/api/tools/mch_pay.php?chapter=14_2
#        https://pay.weixin.qq.com/wiki/doc/api/app/app.php?chapter=9_1
# test api -- http://mp.weixin.qq.com/debug/cgi-bin/readtmpl?t=pay/index&pass_ticket=Vk3Mm8MK6EcgHMomyKlmt7Rj6ktvDqMJ4VAiUleuaveLdfnQtlJDTHolUEts8nIq
# niubility -- http://www.cocoachina.com/bbs/read.php?tid=321546
# xxxxxxxxxx https://doc.open.alipay.com/doc2/detail.htm?spm=a219a.7629140.0.0.qXxvNP&treeId=59&articleId=103663&docType=1

#TODO: 微信开放平台支付
class WePayConfig(object):
    #MCHID = "1322576001"
    #APPID = "wxa994a8c2f4cd80e3"
    #KEY = "256A9B75437B7776F2E8BAE828C1FE91"
    #黑洞的KEY
    #MCHID = "1361353202"
    #APPID = "wx6cad6cc1ace6b7db"
    #KEY = "EF9518800362628F0B864F806D954B94"
    #哇啦的KEY
    MCHID = "1435567302"
    APPID = "wx9434b2be7019584d"
    KEY = "65b8b4b9242ebdcd645c9622138708ee"
    #TODO: 这个我使用的MCHID与APPID生成的秘钥，然后提交的微信电商平台的秘钥中进行修改,hmac.new("wx6cad6cc1ace6b7db","1361353202").hexdigest().upper()
    


class WePayBase(object):
    """
    微信支付基类
    """

    # def post_xml(self, second=30):
    #     raise NotImplementedError

    def dict_to_xml(self, param_map):
        """array转xml"""
        xml = ["<xml>"]
        for k, v in param_map.iteritems():
            if v.isdigit():
                xml.append("<{0}>{1}</{0}>".format(k, v))
            else:
                xml.append("<{0}><![CDATA[{1}]]></{0}>".format(k, v))
        xml.append("</xml>")
        return "".join(xml)

    def xml_to_dict(self, xml):
        data = {}
        root = ET.fromstring(xml)
        for child in root:
            value = child.text
            data[child.tag] = value
        return data

    def get_sign(self, param_map):
        """生成签名"""
        sort_param = sorted(
            [(key, unicode(value).encode('utf-8')) for key, value in param_map.iteritems()],
            key=lambda x: x[0]
        )
        content = '&'.join(['='.join(x) for x in sort_param])
        sign_content = "{0}&key={1}".format(content, WePayConfig.KEY)
        print sign_content
        smd5 = hashlib.md5()
        smd5.update(sign_content)
        return smd5.hexdigest().upper()

    def random_str(self):
        content = string.lowercase + string.digits
        return ''.join(random.sample(content, 16))


class WePayDoPay(WePayBase):
    """
    微信下单接口
    """
    def __init__(self,  out_trade_no, total_fee, body='buy', subject='buy', payment_type="APP",ip=""):
        self.url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
        self.notify_url = settings.Weixin_pay_notifyurl
        self.out_trade_no = str(out_trade_no)
        self.subject = subject
        self.trade_type = payment_type
        self.total_fee = str(total_fee)
        self.body = body
        self.ip = ip
        self.prepay_id = ''
        self.xml = ''
        self.nonce_str = self.random_str()

    def post_xml(self, second=30):
        try:
            data = urllib2.urlopen(
                self.url, self.create_xml(),
                timeout=second).read()

        except Exception:
            raise apiexception.WePayException(-999)
        return data

    def create_xml(self):
        """生成接口参数xml"""
        param_map = {
            'appid': WePayConfig.APPID,
            'mch_id': WePayConfig.MCHID,
            'spbill_create_ip': self.ip,
            'nonce_str': self.nonce_str,
            'out_trade_no': self.out_trade_no,
            'body': self.body,
            'total_fee': self.total_fee,
            'notify_url': self.notify_url,
            'trade_type': self.trade_type
        }

        param_map['sign'] = self.get_sign(param_map)
        self.xml = self.dict_to_xml(param_map)
        return self.xml

    def _get_prepay_id(self):
        """获取prepay_id"""

        result = self.xml_to_dict(self.post_xml())
        print result
        result_code = result.get('result_code')
        err_code = result.get('err_code')
        if result_code != "SUCCESS":
            e = apiexception.WePayException(err_code)
            e.desc = result.get("return_msg","")
            raise e

        self.prepay_id = result.get('prepay_id')
        self.nonce_str = result.get("nonce_str")
        return self.prepay_id

    def do_pay_params(self):
        prepay_id = self._get_prepay_id()
        param_map = {
            'prepayid': prepay_id,
            'appid': WePayConfig.APPID,
            'partnerid': WePayConfig.MCHID,
            'package': 'Sign=WXPay',
            'noncestr': self.nonce_str,
            'timestamp': str(int(time.time()))
        }

        sort_param = sorted(
            [(key, value)for key, value in param_map.iteritems()],
            key=lambda x: x[0]
        )

        sign = self.get_sign(param_map)
        print sign

        pay_params = '&'.join(['='.join(x) for x in sort_param])
        pay_params +="&sign=" + sign

        data = {
            "prepay_id": prepay_id,
            'pay_params': pay_params
        }
        return data

    def do_create_qrcode(self):
        self.trade_type = "NATIVE"
        result = self.xml_to_dict(self.post_xml())
        print result
        result_code = result.get('result_code')
        err_code = result.get('err_code')
        if result_code != "SUCCESS":
            e = apiexception.WePayException(err_code)
            e.desc = result.get("return_msg", "")
            raise e
        self.prepay_id = result.get('prepay_id')
        self.nonce_str = result.get("nonce_str")
        self.code_url = result.get('code_url')

        return {"code_url":self.code_url}


    def verify_notice_sign(self,xml):
        """
        校验签名
        """
        root = xml
        param_map = {}
        sign = ""
        for child in root:
            if child.tag !="sign":
                param_map[child.tag] = child.text
            else:
                sign = child.text

        we_sign = self.get_sign(param_map)

        print sign
        print we_sign

        if sign == we_sign:
            return True
        else:
            return False

class WePayOrderQuery(WePayBase):

    SUCCESS, FAIL = "SUCCESS", "FAIL"

    def __init__(self, out_trade_no):
        self.url = "https://api.mch.weixin.qq.com/pay/orderquery"
        self.out_trade_no = out_trade_no
        self.nonce_str = self.random_str()

    def create_xml(self):
        """生成接口参数xml"""
        param_map = {
            'appid': WePayConfig.APPID,
            'mch_id': WePayConfig.MCHID,
            'nonce_str': self.nonce_str,
            'out_trade_no': self.out_trade_no,
        }

        param_map['sign'] = self.get_sign(param_map)
        self.xml = self.dict_to_xml(param_map)
        return self.xml

    def post_xml(self, second=30):
        try:
            data = urllib2.urlopen(
                self.url, self.create_xml(),
                timeout=second).read()
            print "order query result is " + data
        except Exception:
            raise apiexception.WePayException(-999)
        return self.xml_to_dict(data)


class WePayNotice(WePayBase):
    """响应型接口基类"""
    SUCCESS, FAIL = "SUCCESS", "FAIL"

    def __init__(self, xml_data):
        self.xml_data = xml_data
        self.recieve_param = self._format_params(
            xml_data=xml_data)

    def _format_params(self, xml_data):
        """将微信的请求xml转换成dict，以方便数据处理"""
        return self.xml_to_dict(xml=xml_data)

    def validate(self):
        """校验签名"""
        tmp = copy.deepcopy(self.recieve_param)
        del tmp['sign']
        sign = self.get_sign(tmp) #本地签名

        return self.recieve_param['sign'] == sign

    def return_data(self, data):
        """设置返回微信的xml数据"""
        return self.dict_to_xml(data)

