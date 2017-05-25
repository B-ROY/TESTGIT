# -*- coding: utf-8 -*-

__author__ = 'zen'
from exceptions import BaseException


#每个模块定义自己的 exception，统一继承 ApiExcption
class ApiException(BaseException):
    def __init__(self, code):
        self.code = code
        self.desc = ""


#账号错误码
ACCOUNT_INSUFFICIENT_BALANCE = -101
RULE_MISS = -102
ACCOUNT_EXCEPTION_MAP = {
    ACCOUNT_INSUFFICIENT_BALANCE: u'账号余额不足', #没有足够的票
    RULE_MISS: u'找不到对应规则'
}


class AccountException(ApiException):

    def __init__(self, code):
        self.code = code
        self.desc = ACCOUNT_EXCEPTION_MAP.get(code)

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code


WE_PAY_EXCEPTION = {
    -999: u"未知异常"
}
class WePayException(ApiException):

    def __init__(self, code):
        self.code = code
        self.desc = WE_PAY_EXCEPTION.get(code)

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code


if __name__ == "__main__":

    def a():
        raise AccountException(ACCOUNT_INSUFFICIENT_BALANCE)

    try:
        a()
    except ApiException,e:
        print "###############",e.code,e.desc
