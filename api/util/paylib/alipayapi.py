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
    MIIEpAIBAAKCAQEAqRhWL/5MOzQeXto01XI4PcEOx/oRXg3uinV5OAJkYkfzjrhXPHiraF1e
    MPSXdWz7A2Yj0j4H3yKp7WywWHd481/PwRRRViPYtg1+LZK+SXkBmpqvDwFSSUJPm++ccp31
    6SJM8vh0B2MVMfynogVFTsgthVMBbRNX2DFzhb4LGOhYBmlQyr15in/p0Zz37C9frYEANk28
    AqG0Bg3PvokjaRYujBNVU9ybXTXtAH3P5ScSnstzfrJELn0CbmYBNvU2PrNjWhGzCvffYvZl
    jxeV0CDGuY+Ae5UdIsljgekLVf6vwHuGvuXdGAk3Xf6j1Z+t+NmPlVFZS7RSpibyEx15kQID
    AQABAoIBAEcV6w2sCyIMbAQWGYXtyYT0hyE8mFaA5togPoB0SP0kIFjMWCgc1no+Xh2YhZ+g
    2/l20/JLj4WXjfY47f2S5C70BWO3BeZ/lVgbXgMMoKBElY8IHjXhqVUQ4mS8m3l3vGxwtgai
    uixs0/k6rMIpExTmhHR7C6tuKUzCpT0BQqsKOw9Vs3KEROHb+TbytjuTkNz8CHJcslk+QeEz
    D8zv+YAfaC6XJbAHjesylDcSmqZTEuYu3Yz6D1wh0SOgjQHTsWEoF6HUPlo4hO+kZWj4zrUF
    mjQRxNBaU6oGEbF+1Wmni3IRLIOH6JSLG3VkQ9SYbPpetTGUyv6OtcA+XUgOjU0CgYEA1db3
    ZwbMVymDxvhFhWphJ2t/pKahFuOJ32mg99HqJnb13ZeSYjezqjEhCO7Q4FEt/QoSU+mi/YWL
    DQpTEu3pXAVVb2u80pUclP46xqPQzobgGUi/eIaCuNKYhWlvtC5BPNtPX4nX9NEVYkx9JMOb
    ucZguDmuxPkvlpuA2idE2VMCgYEAym7+hQMCJzy/fMt/VedutsVKewdx83YweKxS9zNhcatS
    uMOF9JOTn1TxTJsOrfNF2f/JP0mdB4xAEDsgquWzVhYB0RZVi0vSSQtvXw18sVvjpTOsJaJm
    n1T1yIPAvW0aqe861DJPLn3VRXek/52AoHE2rY972Hcv2b0iklQL8QsCgYAKZ8RwIfeNgjqk
    Uu5nGI8TsPpsE6OhDn9l/KjVhkRjjMRX/QkleFpovK1D1wMY9zpKptPPe33v4jCq+MakFCmX
    bajjlWI1bKnWVuY0N3XPt7mvBB9F+aCgdTkIQZLeTi5cl6BYp68jfQBbYFlaZNJTerk7AGiG
    hIDvRtfAiwqewKBgQCbPgGcWdFF6/Vhq+HMLD6gla5nqS7/KW1Ercq2XsXk2SEIJpHNHXvBX
    e/q8qKQThcMdneMPFTbW/gpOl70EFG2vAvKoBkcSRpMACP5visZDMIIiBcFiYSvvgT7L+cYn
    dor5hW0c5x7p+5tZrK3gL8Ky6fF9FpiiAy/K6eelivOPwKBgQDO8TleGnCvQN3RGBUOtIAAs
    Fo47ebMg+6i1eMZsomw0o7BwI+p59h5vf2GzbyPWdOAXDTaq2gpXiIwIJsubQ2F34CUdbhrU
    DiloAJaTxFJhWKzkM+AFvSRJud+MYwWV7aJjG6t1SFVnGCquBvbEJJr8OUPSJaIGEH1KjEiV
    Kb3Pw==
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

