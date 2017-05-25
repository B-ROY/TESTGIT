# -*- coding: utf-8 -*-
__author__ = 'zen'
import urllib
import hashlib
import urllib2
import logging

#doc https://doc.open.alipay.com/doc2/detail.htm?spm=a219a.7629140.0.0.qXxvNP&treeId=59&articleId=103663&docType=1
#sign https://doc.open.alipay.com/doc2/detail?treeId=58&articleId=103242&docType=1
import rsa
import base64
from base.core.util.dateutils import int_days

class AliPayConfig(object):
    """
    支付宝 公共配置
    """
    SIGN_TYPE = "RSA"
    INPUT_CHARSTE = "utf-8"
    KEY = 'lbgghw3lqek0byiy820v0sjpnplgj1j3'
    SELLER_ID = "xyg@seeugo.com"
    PARTNER = "2088901476732889"
    ALI_SERVICE_PATH = "https://mapi.alipay.com/gateway.do"
    PRIVATE_KEY = '''-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQDNx1NT9PdO/k1NW2Tc7L3PWOGhzufgRX7TVSAf29v2EQoq1bNI
c1BxG8aVba38nlmw1jq5P5ZxGq+YnhudD0NT5FgVLrQMX0SboO1Y0NZrgbk34OZy
8guCxE3iLCZfUtXOu5fZbZtnYGjV72FQAjxn9PARHUaVXgM7v6MU+1QSywIDAQAB
AoGAOGlCMKvg+CjCrEg3uFC2IBdvk1oTOuoSQID/k3xEKoq1TNTUlzH1hWxl3iT5
I12NnOq9oncKGOuF48LEMyQyAlmZGsivdvYq1d+uGwTK7hlaMTqAGqYQVWrhQaI/
GYdzMUxoY664LPzHzLBvK6iop02HZZrZflyAO6vGIxPs+kECQQDs9p2dIvMjeUn9
sEborCewmeTG8Id4KdpHMivtFYXlzcV8kSCJAQLHsja6H//w4IDI20P9LmHR88oJ
u3i1RRyxAkEA3k9dfuWZ2f20COuyifNWBfQ6GTqrd3HzyteJZaunt5KVhTjSJ7fz
KOdGqRpE0DxpuF5IPAHXaYpa04uw/bNWOwJAbPpOKkI0h4/0U1OKiN8DsdhUuplL
9BtrY2rTgMlxNuqXdF5aFCf+21A+kwK8dk8Ja1ZLwlhebGwt8qPhM5yBQQJBAIxr
rS7ecFPVgMaxulCQt6GDJr+Q44XLIKbbhhoGVyYJHRDNV1FnS9xmWaeuxBCUWGLw
isf8kchEcCJ3dhCKGskCQCXeBSfHcklcDYeLTpMne6J1QoRAHYurFQ6JBYvKVWIP
ewBy8LA1+RXYWz2Qq2A4Yb+jZpo9wNUHFOnoXNNGlr0=
-----END RSA PRIVATE KEY-----'''


class AliPayBase(object):
    """
    支付宝api 基类
    """
    def get_sign(self, param_map, sign_type="RSA"):
        #对参数排序

        sort_param = sorted(
            [(key, unicode(value).encode('utf-8')) for key, value in param_map.iteritems()],
            key=lambda x: x[0]
        )
        content = '&'.join(['='.join(x) for x in sort_param])

        private_key = rsa.PrivateKey.load_pkcs1(AliPayConfig.PRIVATE_KEY)
        sign = rsa.sign(content, private_key, 'SHA-1')
        ssn = base64.urlsafe_b64encode(sign)
        print ssn
        ssn = urllib.quote_plus(ssn)
        return ssn

    def create_request_data(self):
        raise NotImplementedError

    def post_data(self):
        """
        标准post 可以自己实现 ,需要定义 self.create_request_data()
        """
        data = self.create_request_data()
        try:
            result = urllib2.urlopen(
                AliPayConfig.ALI_SERVICE_PATH,
                data=urllib.urlencode(data)).read()
        except Exception, e:
            logging.error("post data error %s %s" % (data['service'],e))

        return result


class AliPayDoPay(AliPayBase):
    """
    支付宝 下单接口封装
    """
    def __init__(self, out_trade_no, subject, total_fee, body='buy', payment_type=1,sign_type="RSA"):
        self.service = "mobile.securitypay.pay"
        self.notify_url = "http://api.mobile.heydo.cc/api/live/alipay/notice"
        self.out_trade_no = out_trade_no
        self.subject = subject
        self.payment_type = payment_type
        self.total_fee = total_fee
        self.body = body
        self.sign_type = sign_type

    def create_request_data(self):
       
        param_map = {
            'service':'"mobile.securitypay.pay"',
            '_input_charset':'"utf-8"',
            'notify_url':'"'+self.notify_url+'"',
            'out_trade_no':'"'+str(self.out_trade_no)+'"',
            'subject':'"'+self.subject+'"',
            'payment_type':'"'+str(self.payment_type)+'"',
            'seller_id':'"'+AliPayConfig.SELLER_ID+'"',
            'total_fee':'"'+str(self.total_fee)+'"',
            'partner':'"'+str(AliPayConfig.PARTNER)+'"',
            'body':'"'+str(self.body)+'"',
        }
        return param_map

        

    def do_pay_params(self):
        params = self.create_request_data()
        
        _sign = self.get_sign(param_map=params)
        params["sign_type"] =  '"RSA"'
        params["sign"] =  '"' + _sign + '"'

        sort_param = sorted(
            [(key, unicode(value).encode('utf-8')) for key, value in params.iteritems()],
            key=lambda x: x[0]
        )
        content = '&'.join(['='.join(x) for x in sort_param])

        #result
        data = {
            "pay_params": content
        }
        return data


class AliPayVerifyNotice(AliPayBase):
    """
    支付宝通知结果验证
    """
    def __init__(self, notice_params):
        self.service = 'notify_verify'
        self.notice_params = notice_params

    def verify_sign(self):

        server_sign = self.get_sign(
            params_map=self.notice_params)
        client_sign = self.notice_params.get("sign")

        return server_sign == client_sign

    def create_request_data(self):
        params = {
            "partner": AliPayConfig.partner,
            "service": self.service,
            "notify_id": self.notice_params['notify_id']
        }
        return params

    def verify_notify_id(self):
        """验证通知是否"""
        result = self.post_data()
        return result == "true"

    def validate(self):
        pass


class AliPayBatchTrans(AliPayBase):
    """
    支付宝批量付款接口
    doc: https://doc.open.alipay.com/doc2/detail.htm?spm=a219a.7629140.0.0.g88hGW&treeId=64&articleId=103773&docType=1
    """
    def __init__(self, batch_no, batch_num, batch_fee, detail_data):
        self.service = "batch_trans_notify"
        self.batch_no = batch_no
        self.batch_num = batch_num
        self.batch_free = batch_fee
        self.detail_data = detail_data

    def create_request_data(self):
        param_map = {
            'partner': AliPayConfig.PARTNER,
            'service': self.service,
            'sign_type': AliPayConfig.SIGN_TYPE,
            'seller_id': AliPayConfig.SELLER_ID,
            '_input_charset': AliPayConfig.INPUT_CHARSTE,
            'account_name': AliPayConfig.SELLER_ID,
            'Email': AliPayConfig.SELLER_ID,
            'detail_data': self.detail_data,
            'batch_no': self.batch_no,
            'batch_num': self.batch_num,
            'batch_fee': self.batch_free,
            'pay_date': str(int_days()),
        }
        sign = self.get_sign(params_map=param_map)
        param_map['sign'] = sign
        sort_param = sorted(
            [(key, urllib2.quote(unicode(value).encode('utf-8'))) for key, value in param_map.iteritems()],
            key=lambda x: x[0]
        )
        return sort_param

    def batch_trans(self):
        data = self.post_data()
        return data

