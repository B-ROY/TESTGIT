#coding=utf-8
import urllib
import os,sys
import time
import logging
from http_request import RequestApi
import json
import hashlib

# doc is here 
# http://wiki.open.qq.com/wiki/mobile/API%E5%88%97%E8%A1%A8
# h5:http://wiki.connect.qq.com/get_user_info
# http://wiki.open.qq.com/wiki/v3/user/get_qqconnect_openid


class QQAPI(object):

    CUSTOMER_KEY = "6xoMc0c1hkKndwnM"
    # CUSTOMER_KEY = "6t6YB9aXKCz2TkGL"

    
    @classmethod
    def get_h5_user_info(cls,access_token,openid):

        params = {
            "access_token":access_token,
            "openid":openid,
            "oauth_consumer_key": "1105884053",
            #"oauth_consumer_key":"101312588",
            "format":"json"
        }
        # TODO: 这里要进行修改,oauth_consumer_key:101312588 这个是当时出了问题导致了重新注册了这个H5专门的一个id，在黑洞中已经修改，这个最后要统一起来
        
        result = RequestApi.get_json("/user/get_user_info", params, headers={}, host='graph.qq.com')
        #print "result",result

        if result.get("ret")!=0:
            raise Exception(json.dumps(result))


        result["headimgurl"] = result.get("figureurl_qq_2","")
        if result.get("u'gender"):
            if result.get("gender") == u"男":
                result["gender"] = 1
            else:
                result["gender"] = 2
        else:
            result["gender"] = 2
      

        return result


    @classmethod
    def get_user_info(cls,access_token,openid,platform="ios"):

        params = {
            "access_token":access_token,
            "openid":openid,
            #"oauth_consumer_key":"1105414753",
            "oauth_consumer_key": "1105884053",
            "format":"json"
        }

        #if platform == "ios":
        #    params["oauth_consumer_key"] =  "1105414753"
        #elif platform == "h5":
        #    return cls.get_h5_user_info(access_token,openid)
        #else:
        #    params["oauth_consumer_key"] =  "1105414753"

        if platform == "h5":
            return cls.get_h5_user_info(access_token, openid)
        else:
            params["oauth_consumer_key"] = "1105884053"

        result = RequestApi.get_json("/user/get_simple_userinfo", params, headers={}, host='graph.qq.com')
        print "result",result

        if result.get("ret")!=0:
            raise Exception(json.dumps(result))


        result["headimgurl"] = result.get("figureurl_qq_2","")
        if result.get("u'gender"):
            if result.get("gender") == u"男":
                result["sex"] = 1
            else:
                result["sex"] = 2
        else:
            result["gender"] = 2
        # {
        # "ret":0,
        # "msg":"",
        # "nickname":"Peter",
        # "figureurl":"http://qzapp.qlogo.cn/qzapp/111111/942FEA70050EEAFBD4DCE2C1FC775E56/30",
        # "figureurl_1":"http://qzapp.qlogo.cn/qzapp/111111/942FEA70050EEAFBD4DCE2C1FC775E56/50",
        # "figureurl_2":"http://qzapp.qlogo.cn/qzapp/111111/942FEA70050EEAFBD4DCE2C1FC775E56/100",
        # "figureurl_qq_1":"http://q.qlogo.cn/qqapp/100312990/DE1931D5330620DBD07FB4A5422917B6/41",
        # "figureurl_qq_2":"http://q.qlogo.cn/qqapp/100312990/DE1931D5330620DBD07FB4A5422917B6/100",
        # "is_yellow_vip"："1", 
        # "is_yellow_year_vip":"0",
        # "yellow_vip_level":"6"
        # }

        return result



    @classmethod
    def get_qq_connention(cls,openid):
        """
        dst_appid   必须  string  应用在QQ互联平台接入QQ登录时获得的appid。
        openid:qq 开放平台openid
        http://wiki.open.qq.com/wiki/v3/user/get_qqconnect_openid
        http://kf.qq.com/faq/120322fu63YV130422aqUNJv.html
        """
        """
        正式环境：http://openapi.tencentyun.com/v3/user/get_info 
        测试环境：http://119.147.19.43/v3/user/get_info 
            #APP ID 1105414753 
            #APPKEY FNjsCKrg71ltNG39  #黑洞直播的key
        # TODO: 更换正式环境 
        """
        param_map = {
            "openid":openid,
            #"openkey":"FNjsCKrg71ltNG39",             #"kyiA5PGpf87TU3xc",
            "openkey":"6t6YB9aXKCz2TkGL",
            "dst_appid":"101312588",
            #"appid":"1105414753",                     #"1105152551",
            "appid":"1105884053",
            "format":"json",
            "pf":"qzone",
        }

        sort_param = sorted(
            [(key, unicode(value).encode('utf-8')) for key, value in param_map.iteritems()],
            key=lambda x: x[0]
        )
        content = ''.join([''.join(x) for x in sort_param])

        m = hashlib.md5()
        m.update(content)
        sig = m.hexdigest()

        param_uri = '&'.join(['='.join(x) for x in sort_param])
        param_uri += "&sig=" + sig

        #url = "http://openapi.tencentyun.com/v3/user/get_qqconnect_openid?%s" % param_uri
        url = "http://119.147.19.43/v3/user/get_qqconnect_openid?%s" % param_uri
        data = urllib.urlopen(url).read(url)

        if data:
            result = json.loads(data)
            dst_openid = result.get('dst_openid')
            if not dst_openid:
                raise Exception("获取qqopenid 失败! %s:%s" % (result.get("ret"),result.get("msg")))
            return dst_openid
        else:
            raise Exception("获取qqopenid 失败 null!")


