#coding=utf-8
import urllib
import os,sys
import time

from api.handler.thridpard.http_request import RequestApi
from api.util.tencenttools.signature import gen_signature
from django.conf import settings
import json
import datetime


class QCloudIM(object):


    def __init__(self):
        pass


    @classmethod
    def account_import(self, user):
        """
        这里用户注册的时候需要同步用户信息，
        用户更新的时候需要同步用户信息，到腾讯云
        """
        app_id = settings.QCLOUD_LIVE_SDK_APP_ID
        sig = gen_signature(app_id, "admin")

        uri = "/v4/im_open_login_svc/account_import?usersig=%s&identifier=admin&sdkappid=%s&contenttype=json" % (sig,app_id)
        body = {
                "Identifier":user.sid,
                "Nick":user.nickname,
                "FaceUrl": user.user_logo,
              }
        body = json.dumps(body)
        data = RequestApi.post_body_request(uri, body, headers={}, host='console.tim.qq.com')
        result = json.loads(data)
        #print data

        if result.get("ActionStatus") == "ok":
            return True , None
        else:
            return False, "%s:%s"  % (result.get("ErrorInfo",""),result.get("ErrorCode",""))

        #         {
        #    "ActionStatus":"OK",
        #    "ErrorInfo":"",
        #    "ErrorCode":0
        # }


    @classmethod
    def portrait_set(self, user):
        """
        这里用户注册的时候需要同步用户信息，
        用户更新的时候需要同步用户信息，到腾讯云
        """
        app_id = settings.QCLOUD_LIVE_SDK_APP_ID
        sig = gen_signature(app_id, "admin")

        uri = "/v4/profile/portrait_set?usersig=%s&identifier=admin&sdkappid=%s&contenttype=json" % (sig,app_id)
        body= {
                 "From_Account":user.sid,
                 "ProfileItem":
                 [
                     {
                        "Tag":"Tag_Profile_IM_Nick", 
                        "Value":user.nickname,
                     }
                 ]
              }
        body = json.dumps(body)
        data = RequestApi.post_body_request(uri, body, headers={}, host='console.tim.qq.com')
        result = json.loads(data)
        #print data

        if result.get("ActionStatus") == "ok":
            return True , None
        else:
            return False, "%s:%s"  % (result.get("ErrorInfo",""),result.get("ErrorCode",""))


    @classmethod
    def portrait_get(self, user):
        """
        """
        app_id = settings.QCLOUD_LIVE_SDK_APP_ID
        sig = gen_signature(app_id, "admin")

        uri = "/v4/profile/portrait_get?usersig=%s&identifier=admin&sdkappid=%s&contenttype=json" % (sig,app_id)
        body= {
                "To_Account":[user.sid], 
                "TagList":
                [
                    "Tag_Profile_IM_Nick"    
                ]
              }

        body = json.dumps(body)
        data = RequestApi.post_body_request(uri, body, headers={}, host='console.tim.qq.com')
        result = json.loads(data)
        return result


    @classmethod
    def friend_import(self, user, to_user,platform):
        """
        这里用户注册的时候需要同步用户信息，
        用户更新的时候需要同步用户信息，到腾讯云
        """
        app_id = settings.QCLOUD_LIVE_SDK_APP_ID
        sig = gen_signature(app_id, "admin")


        uri = "/v4/sns/friend_import?usersig=%s&identifier=admin&sdkappid=%s&contenttype=json" % (sig,app_id)
        body= {
                    "From_Account":user.sid,
                    "AddFriendItem":
                    [
                        {
                            "To_Account":to_user.sid, 
                            "Remark":to_user.nickname,
                            "RemarkTime": int(time.time()),
                            "GroupName":[u"好友"], 
                            "AddSource":"AddSource_Type_%s" % platform,
                            "AddWording":u"请加我为好友，我是你好友",
                            "AddTime":int(time.time()),
                        },
                    ]
              }
        body = json.dumps(body)
        data = RequestApi.post_body_request(uri, body, headers={}, host='console.tim.qq.com')
        result = json.loads(data)
        #print data

        if result.get("ActionStatus") == "ok":
            return True , None
        else:
            return False, "%s:%s"  % (result.get("ErrorInfo",""),result.get("ErrorCode",""))


    @classmethod
    def friend_delete(self, user, to_user):
        """
        这里用户注册的时候需要同步用户信息，
        用户更新的时候需要同步用户信息，到腾讯云
        """
        app_id = settings.QCLOUD_LIVE_SDK_APP_ID
        sig = gen_signature(app_id, "admin")

        uri = "/v4/sns/friend_delete?usersig=%s&identifier=admin&sdkappid=%s&contenttype=json" % (sig,app_id)
        body= {
                    "From_Account":user.sid,
                    "To_Account":[to_user.sid],
                    "DeleteType":"Delete_Type_Both",
              }


        body = json.dumps(body)
        data = RequestApi.post_body_request(uri, body, headers={}, host='console.tim.qq.com')
        result = json.loads(data)
        print data

        if result.get("ActionStatus") == "ok":
            return True , None
        else:
            return False, "%s:%s"  % (result.get("ErrorInfo",""),result.get("ErrorCode",""))



    @classmethod
    def friend_check(self, user, to_user,platform):
        """
        这里用户注册的时候需要同步用户信息，
        用户更新的时候需要同步用户信息，到腾讯云
        """
        app_id = settings.QCLOUD_LIVE_SDK_APP_ID
        sig = gen_signature(app_id, "admin")

        uri = "/v4/sns/friend_check?usersig=%s&identifier=admin&sdkappid=%s&contenttype=json" % (sig,app_id)
        body= {
                    "From_Account":user.sid,
                    "To_Account":[to_user.sid],
                    "DeleteType":"CheckResult_Type_BothWay",
              }
        body = json.dumps(body)
        data = RequestApi.post_body_request(uri, body, headers={}, host='console.tim.qq.com')
        result = json.loads(data)
        #print data

        for i in result.get('CheckItem',[]):
            if i.get("Relation") == "CheckResult_Type_BothWay":
                return True

        return False


    @classmethod
    def friend_list(self, user):
        """
        这里用户注册的时候需要同步用户信息，
        用户更新的时候需要同步用户信息，到腾讯云
        """
        app_id = settings.QCLOUD_LIVE_SDK_APP_ID
        sig = gen_signature(app_id, "admin")

        uri = "/v4/sns/friend_get_all?usersig=%s&identifier=admin&sdkappid=%s&contenttype=json" % (sig,app_id)
        body= {
                    "From_Account":user.sid,
                    "StartIndex":0,
                    "TagList":
                    [
                        "Tag_Profile_IM_Nick"
                    ],
                    "GetCount":100
              }
        body = json.dumps(body)
        data = RequestApi.post_body_request(uri, body, headers={}, host='console.tim.qq.com')
        result = json.loads(data)

        return result
    

    @classmethod
    def push_all(self, message):
        """
        这里用户注册的时候需要同步用户信息，
        用户更新的时候需要同步用户信息，到腾讯云
        """
        app_id = settings.QCLOUD_LIVE_SDK_APP_ID
        sig = gen_signature(app_id, "admin")

        uri = "/v4/openim/push?usersig=%s&identifier=admin&sdkappid=%s&contenttype=json" % (sig,app_id)
        body= {
                    "MsgRandom": int(time.time()),
                    "MsgBody": [
                        {
                            "MsgType": "TIMTextElem",
                            "MsgContent": {
                                "Text": message,
                            }
                        }
                    ]
              }

        body = json.dumps(body)
        data = RequestApi.post_body_request(uri, body, headers={}, host='console.tim.qq.com')
        result = json.loads(data)

        if result.get("ActionStatus") == "ok":
            return True , result.get("TaskId")
        else:
            return False, "%s:%s"  % (result.get("ErrorInfo",""),result.get("ErrorCode",""))


    @classmethod
    def query_push_status(self, task_id):
        """
        这里用户注册的时候需要同步用户信息，
        用户更新的时候需要同步用户信息，到腾讯云
        """
        app_id = settings.QCLOUD_LIVE_SDK_APP_ID
        sig = gen_signature(app_id, "admin")

        uri = "/v4/openim/get_push_report?usersig=%s&identifier=admin&sdkappid=%s&contenttype=json" % (sig,app_id)
        body=  [
                    {
                        "TaskId": task_id,
                    }
                ]

        body = json.dumps(body)
        data = RequestApi.post_body_request(uri, body, headers={}, host='console.tim.qq.com')
        result = json.loads(data)

        return result


    @classmethod
    def set_user_tag(self, user, tag_dict):
        """
        tag_dict:
                "0": "男",
                "1": "深圳"
        """

        
        app_id = settings.QCLOUD_LIVE_SDK_APP_ID
        sig = gen_signature(app_id, "admin")

        uri = "/v4/openim/set_tag?usersig=%s&identifier=admin&sdkappid=%s&contenttype=json" % (sig,app_id)
        body=  [
                    {
                        "To_Account": user.sid,
                        "Tags": tag_dict
                    },
                ]

        body = json.dumps(body)
        data = RequestApi.post_body_request(uri, body, headers={}, host='console.tim.qq.com')
        result = json.loads(data)

        if result.get("ActionStatus") == "ok":
            return True , None
        else:
            return False, "%s:%s"  % (result.get("ErrorInfo",""),result.get("ErrorCode",""))


    @classmethod
    def delete_user_tag(self, user, tags):
        """
        tag_dict:
                 0,
                 1
        """

        
        app_id = settings.QCLOUD_LIVE_SDK_APP_ID
        sig = gen_signature(app_id, "admin")

        uri = "/v4/openim/remove_tag?usersig=%s&identifier=admin&sdkappid=%s&contenttype=json" % (sig,app_id)
        body=  [
                    {
                        "To_Account": user.sid,
                        "Tags": tag_dict
                    },
                ]

        body = json.dumps(body)
        data = RequestApi.post_body_request(uri, body, headers={}, host='console.tim.qq.com')
        result = json.loads(data)

        if result.get("ActionStatus") == "ok":
            return True , None
        else:
            return False, "%s:%s"  % (result.get("ErrorInfo",""),result.get("ErrorCode",""))


    @classmethod
    def user_tag_list(self, user):
        """
        tag_dict:
                 0,
                 1
        """

        
        app_id = settings.QCLOUD_LIVE_SDK_APP_ID
        sig = gen_signature(app_id, "admin")

        uri = "/v4/openim/get_tag?usersig=%s&identifier=admin&sdkappid=%s&contenttype=json" % (sig,app_id)
        body=  {
                        "To_Account": [ user.sid],
                }
                

        body = json.dumps(body)
        data = RequestApi.post_body_request(uri, body, headers={}, host='console.tim.qq.com')
        result = json.loads(data)

        return result

    @classmethod
    def openim_dirty_words_get(self, wordarr):
        """
        查询自定义脏字
        """
        app_id = settings.QCLOUD_LIVE_SDK_APP_ID
        sig = gen_signature(app_id, "admin")

        uri = "/v4/openim_dirty_words/get?usersig=%s&identifier=admin&sdkappid=%s&contenttype=json" % (sig,app_id)
        body=  {}


        body = json.dumps(body)
        data = RequestApi.post_body_request(uri, body, headers={}, host='console.tim.qq.com')
        result = json.loads(data)

        return result

    @classmethod
    def openim_dirty_words_add(self, wordarr):
        """
        添加自定义脏字
        """
        app_id = settings.QCLOUD_LIVE_SDK_APP_ID
        sig = gen_signature(app_id, "admin")

        uri = "/v4/openim_dirty_words/add?usersig=%s&identifier=admin&sdkappid=%s&contenttype=json" % (sig,app_id)
        body=  {
                    "DirtyWordsList": wordarr
               }

        body = json.dumps(body)
        data = RequestApi.post_body_request(uri, body, headers={}, host='console.tim.qq.com')
        result = json.loads(data)

        return result

    @classmethod
    def openim_dirty_words_delete(self, wordarr):
        """
        删除自定义脏字
        """
        app_id = settings.QCLOUD_LIVE_SDK_APP_ID
        sig = gen_signature(app_id, "admin")

        uri = "/v4/openim_dirty_words/delete?usersig=%s&identifier=admin&sdkappid=%s&contenttype=json" % (sig,app_id)
        body=  {
                    "DirtyWordsList": wordarr
               }

        body = json.dumps(body)
        data = RequestApi.post_body_request(uri, body, headers={}, host='console.tim.qq.com')
        result = json.loads(data)

        return result

    @classmethod
    def check_online(self, user):
        """
        检查用户是否在线
        """
        app_id = settings.QCLOUD_LIVE_SDK_APP_ID
        sig = gen_signature(app_id, "admin")

        uri = "/v4/openim/querystate?usersig=%s&identifier=admin&sdkappid=%s&contenttype=json" % (sig, app_id)

        body = {
                    "To_Account": user
               }

        body = json.dumps(body)
        data = RequestApi.post_body_request(uri, body, headers={}, host='console.tim.qq.com')
        result = json.loads(data)

        if result.get("ActionStatus") == "OK":
            return True, result.get("QueryResult")
        else:
            return False, "%s:%s"  % (result.get("ErrorInfo",""),result.get("ErrorCode",""))

    @classmethod
    def change_friends_allow_type(self, user):
        """
        更改好友申请权限(默认为自动添加，改为需要认证)
        """
        app_id = settings.QCLOUD_LIVE_SDK_APP_ID
        sig = gen_signature(app_id, "admin")

        uri = "/v4/profile/portrait_set?usersig=%s&identifier=admin&sdkappid=%s&contenttype=json" % (sig, app_id)

        body = {
            "From_Account": user.sid,
            "ProfileItem":
            [
                {
                    "Tag":"Tag_Profile_IM_AllowType",
                    "Value":"AllowType_Type_NeedConfirm"
                }
            ]
        }

        body = json.dumps(body)
        data = RequestApi.post_body_request(uri, body, headers={}, host='console.tim.qq.com')
        result = json.loads(data)

        if result.get("ActionStatus") == "OK":
            return True, result
        else:
            return False, "%s:%s" % (result.get("ErrorInfo", ""), result.get("ErrorCode", ""))

    @classmethod
    def message_in_bottle(self, user, to_list, random_int, desc):
        """
        发送漂流瓶消息
        """
        app_id = settings.QCLOUD_LIVE_SDK_APP_ID
        sig = gen_signature(app_id, "admin")

        uri = "/v4/openim/batchsendmsg?usersig=%s&identifier=admin&sdkappid=%s&contenttype=json" % (sig, app_id)

        num = 0
        #todo 改成异步
        while len(to_list)>num:

            body = {
                # "From_Account": user.sid,
                # "To_Account": to_list,
                "SyncOtherMachine": 2,
                "From_Account": user.sid,
                "To_Account": to_list[num:num+500],
                "MsgRandom": random_int,
                "MsgBody": [
                    {
                        "MsgType": "TIMTextElem",
                        "MsgContent": {
                            "Text": desc,
                        }
                    },
                    {
                        "MsgType": "TIMTextElem",
                        "MsgContent": {
                            "Text": user.sid,
                        }
                    },
                ],
                "OfflinePushInfo": {
                    "PushFlag": 1,
                }
            }

            body = json.dumps(body)
            data = RequestApi.post_body_request(uri, body, headers={}, host='console.tim.qq.com')
            result = json.loads(data)
            num += 500

        if result.get("ActionStatus") == "OK":
            return True, result
        else:
            return False, "%s:%s" % (result.get("ErrorInfo", ""), result.get("ErrorCode", ""))

    @classmethod
    def voice_in_bottle(self, user, to_list, random_int, listen_url, url_duration):
        """
        发送漂流瓶语音
        """
        app_id = settings.QCLOUD_LIVE_SDK_APP_ID
        sig = gen_signature(app_id, "admin")

        uri = "/v4/openim/batchsendmsg?usersig=%s&identifier=admin&sdkappid=%s&contenttype=json" % (sig, app_id)

        message = {"messageTypeKey": 301, "listen_url": listen_url, "seconds": url_duration, }
        message_body = json.dumps(message)

        body = {
            # "From_Account": user.sid,
            # "To_Account": to_list,
            "SyncOtherMachine": 2,
            "From_Account": user.sid,
            "To_Account": ["43"],
            "MsgRandom": random_int,
            "MsgBody": [
                {
                    "MsgType": "TIMTextElem",
                    "MsgContent": {
                        "Text": listen_url,
                    }
                },
                {
                    "MsgType": "TIMCustomElem",
                    "MsgContent": {
                        "Data": message_body,
                        "Desc": user.sid,
                        # "Ext": "url"
                    }
                },
            ],
            "OfflinePushInfo": {
                "PushFlag": 1,
            },
        }

        body = json.dumps(body)
        data = RequestApi.post_body_request(uri, body, headers={}, host='console.tim.qq.com')
        result = json.loads(data)

        if result.get("ActionStatus") == "OK":
            return True, result
        else:
            return False, "%s:%s" % (result.get("ErrorInfo", ""), result.get("ErrorCode", ""))

    @classmethod
    def send_system_message(cls, user_id, desc):
        app_id = settings.QCLOUD_LIVE_SDK_APP_ID
        sig = gen_signature(app_id, "admin")
        random_int = int(time.mktime(datetime.datetime.now().timetuple()))
        uri = "/v4/openim/sendmsg?usersig=%s&identifier=admin&sdkappid=%s&random=%s&contenttype=json" % (sig, app_id,random_int)
        message = {"messageTypeKey": 500, "content": '<html><h1>你已满足认证条件，快去进行视频聊天赚钱吧</h1><img src="https://hdlive-10048692.image.myqcloud.com/activity_1493192518">beauty</img></html>'}

        body = {
            # "From_Account": user.sid,
            # "To_Account": to_list,
            "SyncOtherMachine": 2,
            "From_Account": "1",
            "To_Account": user_id,
            "MsgRandom": random_int,
            "MsgBody": [
                {

                    "MsgType": "TIMCustomElem",
                    "MsgContent": {
                        "Data": json.dumps(message),
                        "Desc": user_id,
                    }
                }
            ]
        }

        body = json.dumps(body)
        data = RequestApi.post_body_request(uri, body, headers={}, host='console.tim.qq.com')
        result = json.loads(data)

        if result.get("ActionStatus") == "OK":
            return True, result
        else:
            return False, "%s:%s" % (result.get("ErrorInfo", ""), result.get("ErrorCode", ""))
