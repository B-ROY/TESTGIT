# coding=utf-8
import hmac
import base64
import uuid
import time
import urllib
import hashlib
import copy
from http_request import RequestApi
from twitter import Api

class TwitterAPI(object):
    CONSUMER_KEY = "X4S4OUtSCEGAPpWHBiZFncNI6"
    CONSUMER_SECRET = "WHRLVg2uhipMpQ6Nyjsu0M8ZHxZWo6FFmzDei3bhd3SeXw0hio"
    OAUTH_TOKEN_SECRET = "RNyJVNrDEl9YnioQygEPCdC2NGhULFhveStD6QICVYUyh"

    # {"created_at": "Wed Jun 21 08:05:21 +0000 2017", "default_profile": true, "description": "\ud83d\ude0d",
    #  "followers_count": 1, "friends_count": 30, "id": 877437266544570369, "lang": "zh-cn",
    #  "location": "\u4e2d\u534e\u4eba\u6c11\u5171\u548c\u56fd", "name": "Steve Chao",
    #  "profile_background_color": "F5F8FA",
    #  "profile_banner_url": "https://pbs.twimg.com/profile_banners/877437266544570369/1498039066",
    #  "profile_image_url": "http://pbs.twimg.com/profile_images/877466635807760384/82KVeIi1_normal.jpg",
    #  "profile_link_color": "1DA1F2", "profile_sidebar_fill_color": "DDEEF6", "profile_text_color": "333333",
    #  "screen_name": "safechao",
    #  "status": {"created_at": "Wed Jun 21 08:12:47 +0000 2017", "favorite_count": 1, "hashtags": [],
    #             "id": 877439140987412481, "id_str": "877439140987412481", "lang": "en",
    #             "source": "<a href=\"http://twitter.com\" rel=\"nofollow\">Twitter Web Client</a>",
    #             "text": "new here i love the world!", "urls": [], "user_mentions": []}, "statuses_count": 1}
    @classmethod
    def get_user_info(cls, user_id, access_token, access_token_secret):
        import time
        start_time = int(time.time())
        #access_token = "877437266544570369-3nOyHrXxHLMtpgLjPn1dUuUV3gT996o"
        #access_token = "898153207653740546-VWW0XEnlqlX9HDxZMzIZBEuWEMSfMCo"
        #user_id = 877437266544570369
        api = Api(cls.CONSUMER_KEY, cls.CONSUMER_SECRET, access_token, access_token_secret)
        user = api.GetUser(user_id=user_id)
        end_time = int(time.time())
        user_dict = user.AsDict()
        result = {}
        if "screen_name" in user_dict:
            result['nickname'] = user_dict['screen_name']
        result['sex'] = 1
        if "profile_image_url" in user_dict:
            user_dict['profile_image_url'] = user_dict['profile_image_url'].replace("normal", "400x400") #把小头像换成大图
            result['headimgurl']=user_dict['profile_image_url']
        return result

    #
    # @classmethod
    # def get_user_info(cls, user_id, access_token):
    #     access_token = "898153207653740546-VWW0XEnlqlX9HDxZMzIZBEuWEMSfMCo"
    #
    #     dic = {
    #         "oauth_consumer_key"  : cls.CONSUMER_KEY,
    #         "oauth_nonce": base64.b64encode(str(uuid.uuid1())),
    #         "oauth_signature_method": cls.oauth_signature_method,
    #         "oauth_timestamp ": str(int(time.time())),
    #         "oauth_token": access_token,
    #         "oauth_version": "1.0",
    #     }
    #     param_map = {}
    #     param_map["user_id"] = 898153207653740546
    #     oauth_signature = cls.get_signature(dic, param_map),
    #     dic["oauth_signature"] = oauth_signature
    #     data = RequestApi.get(cls.PATH, param_map, dic, host=cls.Host)
    #     print data
    #
    # @classmethod
    # def get_signature(cls, dic, param_map):
    #     dic1 = copy.copy(dic)
    #     dic1.update(param_map)
    #     sort_param = sorted(
    #         [(key, unicode(value).encode('utf-8')) for key, value in dic1.iteritems()],
    #         key=lambda x: x[0]
    #     )
    #     content = '&'.join(['='.join(x) for x in sort_param])
    #     content = cls.HTTP_Method + "&" + cls.Host + cls.PATH + "&" +content
    #     print content
    #     sigining_key = urllib.quote(cls.CONSUMER_SECRET+"&"+cls.OAUTH_TOKEN_SECRET)
    #
    #     ss = hmac.new(sigining_key, content, hashlib.sha1).hexdigest()
    #
    #     signature = base64.b64encode(ss)
    #
    #     return signature