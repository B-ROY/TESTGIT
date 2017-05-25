# -*- coding: utf-8 -*-
import urllib2
import logging
import json

#https://sandbox.itunes.apple.com/verifyReceipt
# 我们提交给苹果审核的是正式版，我们以为苹果审核时，我们应该连接苹果的线上验证服务器来验证购买凭证。结果我理解错了，苹果在审核App时，只会在sandbox环境购买，其产生的购买凭证，也只能连接苹果的测试验证服务器。但是审核的app又是连接的我们的线上服务器。所以我们这边的服务器无法验证通过IAP购买，造成我们app的又一次审核被拒。
# 解决方法是判断苹果正式验证服务器的返回code，如果是21007，则再一次连接测试服务器进行验证即可。苹果的这一篇文档上有对返回的code的详细说明。
#2、由于国内有许多小白用户，他们的手机从购买时就被渠道商帮忙越狱过了并且安装了IAP free插件。所以对于这类用户，他们即使想付费购买，由于系统原有的IAP支付功能已经被破坏，所以他们是无法正常付费的。麻烦的是，他们会以为这是我们的app的问题，转而给我们的客服打电话投诉。这让我们非常郁闷。
# http://blog.jobbole.com/38032/

class ApplePayConfig(object):
    PASSWORD = ""


class ApplePayBase(object):

    def create_request_data(self):
        raise NotImplementedError


class ApplePayDoPay(ApplePayBase):

    def create_request_data(self):
        pass

    def do_pay_params(self):
        return {}


class ApplePayNotice(ApplePayBase):
    """
    苹果支付通知接口
    wiki
    https://developer.apple.com/library/ios/releasenotes/General/ValidateAppStoreReceipt/Chapters/ValidateRemotely.html#//apple_ref/doc/uid/TP40010573-CH104-SW1
    """
    def __init__(self, receipt, is_test=True):
        if is_test:
            self.url = 'https://sandbox.itunes.apple.com/verifyReceipt'
        else:
            self.url = 'https://buy.itunes.apple.com/verifyReceipt'

        self.receipt = receipt

    def create_request_data(self):
        return {
            'receipt-data': self.receipt,
            'password': ApplePayConfig.PASSWORD,
        }

    def post_data(self):
        """
        标准post 可以自己实现 ,需要定义 self.create_request_data()
        """
        data = self.create_request_data()
        json_data = json.dump(data)
        try:
            result = urllib2.urlopen(
                self.url, data=json_data,).read()
        except Exception, e:
            logging.error("post data error %s " % e)
        return json.loads(result)

    def validate(self):
        data = self.post_data()

        return data.get('status') == 0


