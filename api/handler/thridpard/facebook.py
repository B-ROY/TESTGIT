#coding=utf-8

import facebook


class FacebookAPI(object):

    @classmethod
    def get_user_info(cls, access_token):
        graph = facebook.GraphAPI(access_token=access_token, version='2.7')
        user_info = graph.get_object('me')
        print user_info

        result = {
            "nickname": user_info.first_name,
            "headimgurl" : user_info.cover,
            "gender": user_info.gender,
        }

        return result