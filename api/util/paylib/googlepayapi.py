# coding=utf-8

import logging
import urllib
from api.handler.thridpard.http_request import RequestApi
from app_redis.googlepay import *
import time
import json

class GooglePayConfig(object):
    CLIENT_ID = "126218993875-5tkfiqlvqg3g8ga6o3cidmqbo17onp0u.apps.googleusercontent.com"
    CLIENT_SECRET = "eg9cHWUg0nWYrwgdLLMJHjb2"
    REFRESH_TOKEN = "1/bw9YzAtEHetevxXJjc-h9OSpBiOmyxlg0_MlpbnA2y6_M3oiV54pAe5v3KdcRs38"


class GooglePayBase(object):

    def create_request_data(self):
        raise NotImplementedError


class GooglePayDoPay(GooglePayBase):

    def create_request_data(self):
        pass

    @classmethod
    def do_pay_params(cls):
        return {}


class GooglePayNotice(GooglePayBase):
    """
    谷歌支付回调接口

    """
    def __init__(self, package_name, product_id, purchase_token):
        self.host = "accounts.google.com"
        self.path = "/o/oauth2/token"
        self.package_name = package_name
        self.product_id = product_id
        self.purchase_token = purchase_token

    def create_request_data(self):
        return {
            "refresh_token": "1/bw9YzAtEHetevxXJjc-h9OSpBiOmyxlg0_MlpbnA2y6_M3oiV54pAe5v3KdcRs38",
            "client_id": "126218993875-5tkfiqlvqg3g8ga6o3cidmqbo17onp0u.apps.googleusercontent.com",
            "client_secret": "eg9cHWUg0nWYrwgdLLMJHjb2",
            "grant_type": "refresh_token"
        }

    def post_data(self):
        """
        标准post 可以自己实现 ,需要定义 self.create_request_data()
        """
        data = GooglePayRedis.get_access_token()
        access_token_data = json.loads(data)
        ctime = int(time.time())
        if access_token_data.get("exptime") < ctime:
            # 从redis 中get_access_token 如果取不到 请求
            params = self.create_request_data()
            params_encode = urllib.urlencode(params)
            data = RequestApi.post_body_request(self.path, params_encode,
                                                {"Content-Type": "application/x-www-form-urlencoded"}, self.host)
            access_token = data.get("access_token")
            expires_in = data.get("expires_in")
            GooglePayRedis.set_access_token(access_token, ctime+expires_in-60)
        else:
            access_token = access_token_data.get("access_token")

        purchase_check_host = "www.googleapis.com"
        purchase_check_path = "/androidpublisher/v2/applications/"+self.package_name\
                             +"/purchases/products/"+self.product_id+"/tokens/"\
                             + self.purchase_token + "?access_token=" + access_token

        data = RequestApi.get_json(purchase_check_path, {"access_token":access_token}, {}, purchase_check_host)
        logging.error("googlepay check data is " + data)
        return data

    def validate(self):
        try:
            data = self.post_data()
            return data.get('purchaseState') == 0
        except Exception as e:
            logging.error("check google pay error " + str(e) + "---- data is " + str(data))
            return False
