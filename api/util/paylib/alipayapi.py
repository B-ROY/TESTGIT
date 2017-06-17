# -*- coding: utf-8 -*-

import urllib
import urllib2
import logging

import base64
from base.core.util.dateutils import int_days
import hmac
import hashlib
import json
import datetime
import rsa

__author__ = 'biwei'

"""
app 支付需要数据
公共参数
{
    app_id:"",
    method:"alipay.trade.app.pay", (app支付传这个)
    format:"JSON",（仅支持JSON，没得选)
    charset:"utf-8",(还支持，gbk， gbk2312)
    sign_type:"RSA2",(还支持RSA，官方建议使用RSA， 这里我们使用RSA2
    sign:"",（签名， 签名方式见对应方法）
    timestatmp:"",
    version:",1.0
    notify_url:"",(与微信统一，采用异步回调的方式)
    biz_content:"",(业务参数)

}
业务参数:
{
    body:"商品具体描述",
    subject:"商品标题",
    out_trade_no:"订单号(唯一),
    time_out_express：""订单失效时间，1m-15d, 单位 m d h c(当天), 不接受小数点 如1.5转换成90d
    total_amount:"", 单位 元 保留小数点后两位
    product_code:"QUICK_MSECURITY_PAY", 销售产品码 app支付 固定为"QUICK_MSECURITY_PAY"

    #---以下均为可选参数
    seller_id:"", 收款支付宝ID 有默认 不必须传
    goods_type：""，商品主类型：0—虚拟类商品，1—实物类商品 
    passback_params:"",
    promo_params:"",
    extend_params:"",
    enable_pay_channels:"",
    disable_pay_channels:"",
    store_id:""

}




"""





class AliPayConfig(object):
    """
    支付宝 公共配置
    """
    APP_ID = "2017031406213995"
    SIGN_TYPE = "RSA2"
    INPUT_CHARSTE = "utf-8"
    KEY = 'lbgghw3lqek0byiy820v0sjpnplgj1j3'
    ALI_SERVICE_PATH = "https://openapi.alipay.com/gateway.do"
    PRIVATE_KEY = '''-----BEGIN RSA PRIVATE KEY-----
    MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCLOfpiJmUINoMU
    uGSXQzTv6G3y7dZp4on1zyKNUcuVaiYO8blwYwILyO8IPc4SZQ/Naff9NAbsgmR1
    7IBpVfn8+Hs+GtLrHT6oQNo4GB3uElPYalKuNFNFB6t7MF3ZDVaN8mKWS18Zy6zR
    J6a3vQ6YHNwxJYtugulEw59suCdEvRdUhqTO1ENT0aM49lnQJQQvV8OijEN31klD
    mnwRBNBRndJviWtvG7OgywQ7zWGZSnuv8Avg1Z8/zBIMU0arTf8eTDUQWWEuTewy
    erskIq4sJ2qSofixdh1/MPMPoKy4zpkkgobMynKdBvTPz1MdpD5XpXwvf8AkEO7p
    ztuhMo+ZAgMBAAECggEAVz4WeuiKSNI344UEa5DOnELumtqUkDdHsgOBKEMIKnGg
    tZ6dUCKKhq37sxNfjUFM3LA5mK3AZPX0U7zGXrtkcjOWrr0KTBBAUhiJZbsfDi7n
    4WYGt2jMgSYkO4Z8WGW2Ri6LvpguWLC7czjAjMRoX8M964IWVEKuP8vBm9Ptr3FL
    Ui3vY8Geq0+4TV9guquZ5TV+v7AWmNL3h1niVT/Cup60yMf6UW5FihMBvu09gbkf
    nkc0pSqIEmBuCPQ30Nvrg357EWbmn9bs4B80LoYNdqhM7ruHmLYbksacOwFY9CkX
    sRTMdpJbvoteUHjQl8SqW0qcnSzejl8Yt/xaTvtODQKBgQDYqfW8Czvuhb+Wn8XO
    ihNan5EZfNnRMoW3KJl42zEMNiZaHxtz8im++jX4cr+IbgSNu0kl1WvOkM/PTiaK
    ar/UEq3/AgnpmDODCYEtIescrmaNgRtVFqORuNE0j+26S5Wq7Hm6JfWnkROQSoN+
    eWGvZLeihbr/+n6ZninCtBONmwKBgQCkgOePgWFlqU7PyBzgQ44D5UTd0T/7Kehl
    m3QNLvHRpQEx9rJbMZz9hOXmANPFtr4NE/8E1jnmvsdL528jadfHnwugyLlAzMHI
    FjeScuI/XrxiUfYCMy0h8ImnQw3HWTfVlqDBXDCYWTXx1wta2yvSwNqWshgCgzbw
    q5s1d+YE2wKBgAnArMUIJGx6LMOU8Yx4fqKHqDpjelKGWaqC81WTWEPadCN+Xvf7
    IJHuJVvHnoN/oEjY81P2pWGo9xG3zNhSMcxUAu0FpHiVV0xAs0XazwB9gTRBaX+N
    A1Pd49zf1a2bFWOaPWh5qPMf/qdyEzUwNYt1lyaDqoU3O1ei3PJctLydAoGAbv2y
    Pvbyeh8j17mTEhVCaop0Tp1yZ8o8zOF4CbUU33hPOCDU8galf7/9RZRlTk8gJ77I
    H8FSy8cIvMPoDqLJPhynQdJse7YrQQ8Ma7krwcnvnP7j11QkLXQXzEzHrSsbKvc4
    e33yI7h9VzDarnCWPtp0IZ0D6h4SIYwHaqn8/mUCgYAz8fvrXnLhc4VJ+Xazh5IT
    Q5w9mCPyM2NZBM90TXlGnx8VeTdFseB9572Tst9xqA1gKespJESn4TVvL0WZ9aNH
    heSEnj7nkY+OQ9JzUrw5l1Xs5U8sE5pOZZRRpyZ789aqUh65vQDBdTD9kqSpIvA2
    li2ugYE0rz/aargkkWVDIg==
    -----END RSA PRIVATE KEY-----'''



class AliPayBase(object):
    """
    支付宝api 基类
    """

    def get_sign(self, param_map, sign_type="RSA2"):
        # 对参数排序

        sort_param = sorted(
            [(key, unicode(value).encode('utf-8')) for key, value in param_map.iteritems()],
            key=lambda x: x[0]
        )
        content = '&'.join(['='.join(x) for x in sort_param])

        print "content is " + str(content)

        private_key = rsa.PrivateKey.load_pkcs1(AliPayConfig.PRIVATE_KEY.encode())
        sign = rsa.sign(content, private_key, 'SHA-256')
        print sign
        ssn = base64.urlsafe_b64encode(sign)
        print ssn
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
            logging.error("post data error %s %s" % (data['service'], e))

        return result


class AliPayDoPay(AliPayBase):
    """
    支付宝 下单接口封装
    """

    def __init__(self, out_trade_no, subject, total_fee, body='buy', payment_type=1, sign_type="RSA2"):

        self.method = "alipay.trade.app.pay"
        self.notify_url = "http://123.207.175.223/api/live/alipay/notice"
        self.out_trade_no = out_trade_no
        self.subject = subject
        self.payment_type = payment_type
        self.total_fee = total_fee
        self.body = body
        self.sign_type = sign_type

    def create_request_data(self):

        biz_content = {
            "body": self.body,
            "subject": self.subject,
            "out_trade_no": self.out_trade_no,
            "time_out_express": "30m",
            "total_amount": self.total_fee,
            "product_code": "QUICK_MSECURITY_PAY"

        }

        param_map = {
            "app_id": AliPayConfig.APP_ID,
            "method": self.method,
            "format": "json",
            "charset": "utf-8",
            "sign_type": "RSA2",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.0",
            "notify_url": self.notify_url,
            "biz_content": json.dumps(biz_content)
        }
        return param_map

    def do_pay_params(self):
        params = self.create_request_data()

        _sign = self.get_sign(param_map=params)
        params["sign"] = _sign

        sort_param = sorted(
            [(key, unicode(value).encode('utf-8')) for key, value in params.iteritems()],
            key=lambda x: x[0]
        )
        content = '&'.join(['='.join(x) for x in sort_param])

        # result
        data = {
            "pay_params": content
        }
        print "data is is is " + str(data)
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

