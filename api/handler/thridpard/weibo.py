#coding=utf-8
import urllib
import os,sys
import time


from http_request import RequestApi

#doc http://open.weibo.com/wiki/2/users/show
class WeiBoAPI(object):


    @classmethod
    def get_token_info(cls,access_token, openid):
        params = {
            "access_token":access_token,
            "uid" : openid
        }

        result = RequestApi.get_json("/2/users/show.json", params, headers={}, host='api.weibo.com')

        #result["nickname"] = result.get("screen_name")
        #result["headimgurl"] = result.get("avatar_large")

        return result








