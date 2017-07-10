# coding=utf-8
from django.conf import settings
from ucpaasSMS import UcpaasSMS
from tencentSMS import TencentSMS


class SMS(object):

    def __init__(self, sms_type=0):
        if settings.INTERNATIONAL_TYPE == 0 and sms_type == 0:
            print 0
            self.sms = UcpaasSMS()
        else:
            print 1

            self.sms = TencentSMS()

    def sendRegiesterCode(self, toTelNumber, method=0, sms_type=0):
        return self.sms.sendRegiesterCode(toTelNumber, method, sms_type)

    def getCacheData(self, toTelNumber):
        return self.sms.getCacheData(toTelNumber)

    def delSmsCodeCache(self, toTelNumber):
        self.sms.delSmsCodeCache(toTelNumber)

    def get_access_token(self, phoneNumber, openId, create_time=None):
        return self.sms.get_access_token(phoneNumber, openId, create_time)