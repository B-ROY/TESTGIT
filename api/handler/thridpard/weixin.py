#coding=utf-8
import urllib
import os,sys
import time

import pylibmc


from http_request import RequestApi
from django.conf import settings
import logging

code_cache = pylibmc.Client(settings.memcache_settings["user_cache"], binary=True,behaviors={"tcp_nodelay": True, "ketama": True})

#https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&t=resource/res_list&verify=1&id=open1419316505&token=d1ba14cda9ea1b84db275b2f26404bc9a6583fe5&lang=zh_CN
#https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&t=resource/res_list&verify=1&id=open1419317853&token=d1ba14cda9ea1b84db275b2f26404bc9a6583fe5&lang=zh_CN
#http://mp.weixin.qq.com/wiki/home/
class WexinAPI(object):

    @classmethod
    def get_access_token(cls,code):
        # TODO: 微信开放平台
        params = {
            #"appid":"wx43f595ba15a12166", # 爱哇啦
            #"secret":"af2bba025ccdb410050d25b0628b2396", # 爱哇啦
            "appid":"wx9434b2be7019584d", # 聊啪
            "secret":"5f6f10b1bc29d3d1f4bd5dc150cb5450", # 聊啪
            "code":code,
            "grant_type":"authorization_code",
        }


        result = RequestApi.get_json('/sns/oauth2/access_token', params, headers={}, host='api.weixin.qq.com')

        print result
        # { 
        # "access_token":"ACCESS_TOKEN", 
        # "expires_in":7200, 
        # "refresh_token":"REFRESH_TOKEN",
        # "openid":"OPENID", 
        # "scope":"SCOPE" 
        # }

        return result
    @classmethod
    def get_open_id_h5(cls, code):
        cache = code_cache.get(code)
        if cache is not None:
            openid = cache["open_id"]
        else:
            try:
                params = {
                    #"appid":"wx43f595ba15a12166", # 爱哇啦
                    #"secret":"af2bba025ccdb410050d25b0628b2396", # 爱哇啦
                    "appid":"wx5d62865ec8234f14", # 爱聊娱乐
                    "secret":"a1e20b172074e6c64c8d8c93e9260f77", # 爱聊娱乐
                    "code":code,
                    "grant_type":"authorization_code",
                }

                result = RequestApi.get_json('/sns/oauth2/access_token', params, headers={}, host='api.weixin.qq.com')
                print result
                openid = result["openid"]
                cache={}
                cache["open_id"] = openid
                code_cache.add(code, cache)
            except Exception, e:
                logging.error(result)
                raise e

        # {
        # "access_token":"ACCESS_TOKEN",
        # "expires_in":7200,
        # "refresh_token":"REFRESH_TOKEN",
        # "openid":"OPENID",
        # "scope":"SCOPE"
        # }

        return openid


    @classmethod
    def get_user_info(cls,access_token,openid):
        params = {
            "access_token":access_token,
            "openid":openid
        }
        result = RequestApi.get_json("/sns/userinfo", params, headers={}, host='api.weixin.qq.com')

        # { 
        #     "openid":"OPENID",
        #     "nickname":"NICKNAME",
        #     "sex":1,
        #     "province":"PROVINCE",
        #     "city":"CITY",
        #     "country":"COUNTRY",
        #     "headimgurl": "http://wx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ4eMsv84eavHiaiceqxibJxCfHe/0",
        #     "privilege":[
        #     "PRIVILEGE1", 
        #     "PRIVILEGE2"
        #     ],
        #     "unionid": " o6_bmasdasdsad6_2sgVt7hMZOPfL"
        # }

        return result

    @classmethod
    def get_h5_user_info(cls,access_token,openid):
        params = {
            "access_token":access_token,
            "openid":openid
        }
        result = RequestApi.get_json("/cgi-bin/user/info", params, headers={}, host='api.weixin.qq.com')

        print result
        # { 
        #     "openid":"OPENID",
        #     "nickname":"NICKNAME",
        #     "sex":1,
        #     "province":"PROVINCE",
        #     "city":"CITY",
        #     "country":"COUNTRY",
        #     "headimgurl": "http://wx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ4eMsv84eavHiaiceqxibJxCfHe/0",
        #     "privilege":[
        #     "PRIVILEGE1", 
        #     "PRIVILEGE2"
        #     ],
        #     "unionid": " o6_bmasdasdsad6_2sgVt7hMZOPfL"
        # }

        return result




