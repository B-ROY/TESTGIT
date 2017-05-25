#coding=utf-8

import httplib
import urllib, urllib2
import json
import base64
import functools
import logging
import time


class RequestApi(object):

    TimeOut = 3
    DEBUG_LEVEL = 1
    HOST = "api.weixin.qq.com"

    @classmethod
    def request(cls, method, path, params, headers={}, host=''):
        _headers = {'Accept-Language': 'zh-cn', 'User-Agent': 'Python/Automate', "Accept-Charset": "utf-8"}
        _headers.update(headers)

        conn = httplib.HTTPSConnection(host, timeout=cls.TimeOut)
        
        for k, v in params.items():
            if v == '' or v == None:
                del params[k]

        params = urllib.urlencode(params)
        if method == "GET":
            path = "%s?%s" % (path, params)
            params = ''
        else:
            path = "%s" % path
            
        logging.debug("*[Requst]* %s %s %s" % (method, host + path, params))
        conn.request(method, path, params, _headers)
        #conn.set_debuglevel(cls.DEBUG_LEVEL)
        try:
            r = conn.getresponse()
            data =  r.read()
            return data
        except Exception,e:
            logging.error("*[Requst]* %s %s %s request error:%s" % (method, host + path, params,e))
            raise e
        finally:
            conn.close()


    @classmethod
    def post_body_request(cls, path, body, headers={}, host=''):
        print '====enter 3===='
        print host
        print body
        method = "POST"
        
        _headers = {'Accept-Language': 'zh-cn', 'User-Agent': 'Python/Automate', "Accept-Charset": "utf-8"}
        _headers.update(headers)

        conn = httplib.HTTPSConnection(host, timeout=cls.TimeOut)
        path = "%s" % path
            
        logging.debug("*[Requst]* %s %s %s" % (method, host + path, body))
        conn.request(method, path, body, _headers)
        #conn.set_debuglevel(cls.DEBUG_LEVEL)
        try:
            r = conn.getresponse()
            data =  r.read()
            print data
            return data
        except Exception,e:
            logging.error("*[Requst]* %s %s %s request error:%s" % (method, host + path, body,e))
            raise e
        finally:
            conn.close()


    @classmethod
    def get(cls, path, params, headers={}, host=''):
        return cls.request("GET", path, params, headers, host)

    @classmethod
    def get_json(cls, path, params, headers={}, host=''):
        return json.loads(cls.request("GET", path, params, headers, host))

    @classmethod
    def post(cls, path, params, headers={}, host=''):
        return cls.request("POST", path, params, headers, host)

    @classmethod
    def post_json(cls, path, params, headers={}, host=''):
        return json.loads(cls.request("POST", path, params, headers, host))

        
