#coding=utf-8
from wepayapi import WePayBase, WePayConfig_Open_Liaopa
import urllib2
import requests
from api.apiexceptions import apiexception

# https://pay.weixin.qq.com/wiki/doc/api/tools/mch_pay.php?chapter=14_2
class WeMPay(WePayBase):
    """厂商支付"""
    CA_FILE = '/mydata/python/Chatpa/app/apiclient_cer1.pem'
    NO_CHECK = 0
    FORCE_CHECK = 1
    OPTION_CHECK = 2

    def __init__(self, openid, partner_trade_no, amount, desc='withdraw', ip="", check_name=0, user_name=''):
        self.url = "https://api.mch.weixin.qq.com/mmpaymkttransfers/promotion/transfers"
        self.nonce_str = self.random_str()
        self.partner_trade_no = str(partner_trade_no)
        self.openid = openid
        self.amount = amount
        self.desc = desc
        self.check_name = check_name
        self.user_name = user_name
        self.ip = ip
        self.xml = ''

    def create_xml(self):
        param_map = {
            'mch_appid': WePayConfig_Open_Liaopa.APPID,
            'mchid': WePayConfig_Open_Liaopa.MCHID,
            'nonce_str': self.nonce_str,
            'partner_trade_no': self.partner_trade_no,
            'openid': self.openid,
            'amount': str(self.amount),
            'desc': self.desc,
            'spbill_create_ip': self.ip,
        }
        if self.check_name:
            param_map['re_user_name'] = self.user_name
            if self.check_name == 1:
                param_map['check_name'] = 'FORCE_CHECK'
            else:
                param_map['check_name'] = 'OPTION_CHECK'
        else:
            param_map['check_name'] = 'NO_CHECK'

        param_map['sign'] = self.get_sign(param_map)
        self.xml = self.dict_to_xml(param_map)
        return self.xml

    def post_xml(self, second=30):
        # temp return for debug
        data1 = """<xml>
<return_code><![CDATA[SUCCESS]]></return_code>
<return_msg><![CDATA[]]></return_msg>
<mch_appid><![CDATA[wxec38b8ff840bd989]]></mch_appid>
<mchid><![CDATA[10013274]]></mchid>
<device_info><![CDATA[]]></device_info>
<nonce_str><![CDATA[lxuDzMnRjpcXzxLx0q]]></nonce_str>
<result_code><![CDATA[SUCCESS]]></result_code>
<partner_trade_no><![CDATA[10013574201505191526582441]]></partner_trade_no>
<payment_no><![CDATA[1000018301201505190181489473]]></payment_no>
<payment_time><![CDATA[2015-05-19 15：26：59]]></payment_time>
</xml>"""


        try:
            # data = urllib2.urlopen(self.url, self.create_xml(), timeout=second).read()
            #data = urllib2.urlopen(self.url, self.create_xml(), timeout=second, cafile=WeMPay.CA_FILE).read()
            data=requests.post(url=self.url, data=self.create_xml(),cert=WeMPay.CA_FILE, verify=False).text
            print data

        except Exception as e:
            print "112" + str(e)
            raise apiexception.WePayException(-999)
        return self.xml_to_dict(data)

    # TODO: add openssl CA
    # // Trust own CA and all self-signed certs
    # // Allow TLSv1 protocol only

if __name__ == '__main__':
    # m = WeMPay(openid, trade_no, amount, ip='127.0.0.1')
    pass