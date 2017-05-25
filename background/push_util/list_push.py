# -*- coding: utf-8 -*-
from array import array

from igt_push import *
from igetui.template import *
from igetui.template.igt_base_template import *
from igetui.template.igt_transmission_template import *
from igetui.template.igt_link_template import *
from igetui.template.igt_notification_template import *
from igetui.template.igt_notypopload_template import *
from igetui.template.igt_apn_template import *
from igetui.igt_message import *
from igetui.igt_target import *
from igetui.template import *
from BatchImpl import *
from payload.APNPayload import *

# toList接口每个用户返回用户状态开关,true：打开 false：关闭
os.environ['needDetails'] = 'true'

# http的域名
HOST = 'http://sdk.open.api.igexin.com/apiex.htm';
# https的域名
# HOST = 'https://api.getui.com/apiex.htm';

# 测试环境
#APPID = "UXlIM2A1MK96z1EUN02s72"
#APPKEY = "SEXejZEdUX8TB61k0PfjQ4"
#APPSECRET = "2xEc02ip9M84hF5aGmiN5"
#MASTERSECRET = "Z7AICFYLtyA4DrhGQ0pgkA"
#Alias = '请输入别名'
#DEVICETOKEN = ""

# 正式环境
APPID = "2uEkP51DHz89EAyjk8wtr1"
APPKEY = "TuqMW8mRfz6vh0dLBX4kE"
APPSECRET = "3ssS4dq64D8hh2feuFfGg4"
MASTERSECRET = "3JJxNDQg4bAjTcryCGK8W9"
Alias = '请输入别名'
DEVICETOKEN = ""

# iwalaCo测试环境
#APPID_CO = "8t61daJcER8aIOcYqol9I8"
#APPKEY_CO = "yYQhkPsnxo5bYc3pcbDN18"
#APPSECRET_CO = "OAfxWMrLww90zLCGKl3b27"
#MASTERSECRET_CO = "nsNlM8mdCC6GE9BxMJy53"
#Alias_CO = '请输入别名'
#DEVICETOKEN_CO = ""

# iwalaCo正式环境
APPID_CO = "2uEkP51DHz89EAyjk8wtr1"
APPKEY_CO = "TuqMW8mRfz6vh0dLBX4kE"
APPSECRET_CO = "3ssS4dq64D8hh2feuFfGg4"
MASTERSECRET_CO = "3JJxNDQg4bAjTcryCGK8W9"
Alias_CO = '请输入别名'
DEVICETOKEN_CO = ""



GETUI_CONSTANT = {
    "liaoai":{
        "APPID":"2uEkP51DHz89EAyjk8wtr1",
        "APPKEY": "TuqMW8mRfz6vh0dLBX4kE",
        "APPSECRET": "3ssS4dq64D8hh2feuFfGg4",
        "MASTERSECRET": "3JJxNDQg4bAjTcryCGK8W9",
        "Alias": '请输入别名',
        "DEVICETOKEN": ""
    },

    "liaoai_lwm": {
        "APPID": "QNsCzqQYGJ6zymzKYJB213",
        "APPKEY": "m6d4KHBkkn9bav0iNlpO18",
        "APPSECRET": "nk1VKZNIaX7x0JWTjzxsJ1",
        "MASTERSECRET": "HJivDgmDIl5mRoMLXMrYe5",
        "Alias": '请输入别名',
        "DEVICETOKEN": ""

    },


    "liaoai_lizhen": {
        "APPID": "N8lkTV68XJ6RyhPdgIKXk3",
        "APPKEY": "a6j1jmOAJF7hNeXUoQRuv",
        "APPSECRET": "RFxEQe44tW7358I8LTE8k5",
        "MASTERSECRET": "JyoZYsSOZMAZ2AEDD5EMQ8",
        "Alias": '请输入别名',
        "DEVICETOKEN": ""
    },

    "liaoai_biwei": {
        "APPID": "INYKFaWNSl8V6FVdaAO0x9",
        "APPKEY": "KM0rT9jee17pQ0O6hVe1q1",
        "APPSECRET": "Gw5WNz25OQ85a3KL91UR11",
        "MASTERSECRET": "7C8zAJOVas5uLOxEUlusAA",
        "Alias": '请输入别名',
        "DEVICETOKEN": ""

    },
    "liaoai_teyue": {
        "APPID": "EqzGu67IngAk66kLW7UyU3",
        "APPKEY": "dtSyBAeMSp5FgefhxCf1Q9",
        "APPSECRET": "UjIoJgCbKh9p2vkXFTKaZ5",
        "MASTERSECRET": "wZyhoTidIU6f10NRS7EhY1",
        "Alias": '请输入别名',
        "DEVICETOKEN": ""

    },


    "chatpa": {
        "APPID": "ynQsQmDn4SAGEN0tpJ1ER9",
        "APPKEY": "QTvEFPaUNQ6TvZHfcrhSm4",
        "APPSECRET": "DYuHPNamBL9AYJvk0llDV",
        "MASTERSECRET": "t0LEhXrvtL9LydXQ6MHTY4",
        "Alias": '请输入别名',
        "DEVICETOKEN": ""
    }

}




""""______________________________新老代码分割线________________________________________ """


def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


@singleton
class PushMessageGeTui(object):
    def __init__(self):
        self.push = {}

    def get_push(self, app_name):
        if self.push.get(app_name):
            return self.push.get(app_name)
        else :
            self.push[app_name] = IGeTui(HOST, GETUI_CONSTANT[app_name]["APPKEY"], GETUI_CONSTANT[app_name]["MASTERSECRET"])
            return self.push[app_name]

pushMessageObject = PushMessageGeTui()


def push_message_to_list(title, desc, content, client_id, app_name, platform, osver):

    if platform == 0:  # Android
        template = NotificationTemplateAndroid(title, desc, content,app_name)
    elif platform == 1:  # ios
        if osver < "8.2":
            template = NotificationTemplateIOS(title, desc, content,app_name)
        else:
            template = NotificationTemplateIOS82(title, desc, content,app_name)
    else:
        return
    push = pushMessageObject.get_push(app_name=app_name)
    message = IGtListMessage()
    message.data = template
    message.isOffline = True
    message.offlineExpireTime = 1000 * 60 * 10
    message.pushNetWorkType = 0
    contentId = push.getContentId(message)
    target = Target()
    target.clientId = client_id
    target.appId = GETUI_CONSTANT[app_name]["APPID"]
    targets =[target]
    ret = push.pushMessageToList(contentId, targets)
    return ret







""" 之前代码， 留作参考
@singleton
class PushMessageGeTui(object):

    def __init__(self):
        self.push = ""

    def get_android_push(self):
        if self.push:
            return self.push
        else:
            self.push = IGeTui(HOST, APPKEY, MASTERSECRET)
            return self.push

    def get_ios_push(self):
        if self.push:
            return self.push
        else:
            self.push = IGeTui(HOST, APPKEY, MASTERSECRET)
            return self.push
pushMessageObject = PushMessageGeTui()
"""

@singleton
class PushMessageGeTuiCo(object):

    def __init__(self):
        self.push = ""

    def get_android_push(self):
        if self.push:
            return self.push
        else:
            self.push = IGeTui(HOST, APPKEY_CO, MASTERSECRET_CO)
            return self.push

    def get_ios_push(self):
        if self.push:
            return self.push
        else:
            self.push = IGeTui(HOST, APPKEY_CO, MASTERSECRET_CO)
            return self.push
pushMessageObjectCo = PushMessageGeTuiCo()

def test_target_list(client_ids,platform,osver):
    arrAndroid = []
    arrIos = []
    arrIos82 = []
    platform = int(platform)
    for client_id in client_ids:
        target = Target()
        if client_id:
            target.clientId = client_id
            target.appId = APPID
            if platform == 0:
                arrAndroid.append(target)
            elif platform == 1:
                if osver < "8.2":
                    arrIos.append(target)
                else:
                    arrIos82.append(target)
    return arrAndroid, arrIos, arrIos82

def target_list(users):
    arrAndroid = []
    arrIos = []
    arrIos82 = []
    for user in users:
        target = Target()
        if user.cid:
            target.clientId = user.cid
            target.appId = APPID
            if user.platform == 0:
                arrAndroid.append(target)
            elif user.platform == 1:
                if user.osver < "8.2":
                    arrIos.append(target)
                else:
                    arrIos82.append(target)
    return arrAndroid, arrIos, arrIos82

def target_list_co(users):
    arrAndroid = []
    arrIos = []
    arrIos82 = []
    for user in users:
        target = Target()
        if user.cid:
            target.clientId = user.cid
            target.appId = APPID_CO
            if user.platform == 0:
                arrAndroid.append(target)
            elif user.platform == 1:
                if user.osver < "8.2":
                    arrIos.append(target)
                else:
                    arrIos82.append(target)
    return arrAndroid, arrIos, arrIos82

def pushMessageToList(title, desc, content, arr,_type='android'):

    # 消息模版： 
    # TransmissionTemplate:透传功能模板

    if _type == 'android':
        push = pushMessageObject.get_android_push()
        template = NotificationTemplateAndroid(title, desc, content)
    else:
        push = pushMessageObject.get_ios_push()
        if _type == 'ios':
            template = NotificationTemplateIOS(title, desc, content)
        else:
            template = NotificationTemplateIOS82(title, desc, content)

    message = IGtListMessage()
    message.data = template
    message.isOffline = True
    message.offlineExpireTime = 1000 * 60 * 10
    message.pushNetWorkType = 0

    contentId = push.getContentId(message)
    while len(arr) >999:
        ret = push.pushMessageToList(contentId, arr[:999])
        arr = arr[999:]
    ret = push.pushMessageToList(contentId, arr)
    return ret

def pushMessageToListCo(title, desc, content, arr,_type='android'):

    if _type == 'android':
        push = pushMessageObjectCo.get_android_push()
        template = NotificationTemplateAndroidCo(title, desc, content)
    else:
        push = pushMessageObjectCo.get_ios_push()
        if _type == 'ios':
            template = NotificationTemplateIOSCo(title, desc, content)
        else:
            template = NotificationTemplateIOS82Co(title, desc, content)

    message = IGtListMessage()
    message.data = template
    message.isOffline = True
    message.offlineExpireTime = 1000 * 60 * 10
    message.pushNetWorkType = 0

    contentId = push.getContentId(message)
    while len(arr) > 999:
        ret = push.pushMessageToList(contentId, arr[:999])
        arr = arr[999:]
    ret = push.pushMessageToList(contentId, arr)
    return ret

def get_transmission_template(content,app_name):
    template = TransmissionTemplate()
    template.transmissionType = 2
    template.transmissionContent = content
    template.appId = GETUI_CONSTANT[app_name]["APPID"]
    template.appKey = GETUI_CONSTANT[app_name]["APPKEY"]
    return template

def get_transmission_template_co(content,app_name):
    template = TransmissionTemplate()
    template.transmissionType = 2
    template.transmissionContent = content
    template.appId = GETUI_CONSTANT[app_name]["APPID"]
    template.appKey = GETUI_CONSTANT[app_name]["APPKEY"]
    return template

def get_notification_template(title,desc,content,app_name):
    template = NotificationTemplate()
    template.transmissionType = 2
    template.transmissionContent = content
    template.title = title
    template.text = desc
    template.logo = "icon.png"
    template.logoURL = ""
    template.isRing = True
    template.isVibrate = True
    template.isClearable = True
    return template

def NotificationTemplateAndroid(title=u"标题", desc=u"说明", content="", app_name=""):
    template = get_transmission_template(content,app_name)
    return template

def NotificationTemplateAndroidCo(title=u"标题", desc=u"说明", content="",app_name=""):
    template = get_transmission_template_co(content,app_name)
    return template

def NotificationTemplateIOS(title=u"标题", desc=u"说明", content="",app_name=""):
    template = get_transmission_template(content,app_name)

    # 设置APNS信息
    apnpayload = APNPayload()
    apnpayload.badge = 1
    # apnpayload.sound = "test1.wav"
    apnpayload.contentAvailable = 1
    apnpayload.category = "ACTIONABLE"
    # # 简单类型如下设置
    # alertMsg = SimpleAlertMsg()
    # alertMsg.alertMsg = desc
    #字典类型如下设置
    alertMsg = DictionaryAlertMsg()
    alertMsg.body = desc
    alertMsg.actionLocKey = 'actionLockey'
    alertMsg.locKey = desc.encode("utf-8")
    alertMsg.locArgs=['loc-args']
    alertMsg.launchImage = 'launchImage'
    # IOS8.2以上版本支持
    alertMsg.title = title
    #alertMsg.titleLocArgs = ['TitleLocArg']
    #alertMsg.titleLocKey = 'TitleLocKey'
    #可以设置字典类型AlertMsg和简单类型AlertMsg其中之一
    apnpayload.alertMsg = alertMsg
    apnpayload.addCustomMsg("result", content)
    template.setApnInfo(apnpayload)
    return template

def NotificationTemplateIOSCo(title=u"标题", desc=u"说明", content="",app_name=""):
    template = get_transmission_template_co(content.app_name)

    # 设置APNS信息
    apnpayload = APNPayload()
    apnpayload.badge = 1
    # apnpayload.sound = "test1.wav"
    apnpayload.contentAvailable = 1
    apnpayload.category = "ACTIONABLE"
    # # 简单类型如下设置
    # alertMsg = SimpleAlertMsg()
    # alertMsg.alertMsg = desc
    #字典类型如下设置
    alertMsg = DictionaryAlertMsg()
    alertMsg.body = desc
    alertMsg.actionLocKey = 'actionLockey'
    alertMsg.locKey = desc.encode("utf-8")
    alertMsg.locArgs=['loc-args']
    alertMsg.launchImage = 'launchImage'
    # IOS8.2以上版本支持
    alertMsg.title = title
    #alertMsg.titleLocArgs = ['TitleLocArg']
    #alertMsg.titleLocKey = 'TitleLocKey'
    #可以设置字典类型AlertMsg和简单类型AlertMsg其中之一
    apnpayload.alertMsg = alertMsg
    apnpayload.addCustomMsg("result", content)
    template.setApnInfo(apnpayload)
    return template

def NotificationTemplateIOS82(title=u"标题", desc=u"说明", content="",app_name=""):
    template = get_transmission_template(content,app_name)
    # 设置APNS信息
    apnpayload = APNPayload()
    apnpayload.badge = 1
    # apnpayload.sound = "test1.wav"
    apnpayload.contentAvailable = 1
    apnpayload.category = "ACTIONABLE"
    # # 简单类型如下设置
    # alertMsg = SimpleAlertMsg()
    # alertMsg.alertMsg = desc
    #字典类型如下设置
    alertMsg = DictionaryAlertMsg()
    alertMsg.body = desc
    alertMsg.actionLocKey = 'actionLockey'
    alertMsg.locKey = desc.encode("utf-8")
    alertMsg.locArgs=['loc-args']
    alertMsg.launchImage = 'launchImage'
    # IOS8.2以上版本支持
    alertMsg.title = title
    #alertMsg.titleLocArgs = ['TitleLocArg']
    #alertMsg.titleLocKey = 'TitleLocKey'
    #可以设置字典类型AlertMsg和简单类型AlertMsg其中之一
    apnpayload.alertMsg = alertMsg
    apnpayload.addCustomMsg("result", content)
    template.setApnInfo(apnpayload)
    return template

def NotificationTemplateIOS82Co(title=u"标题", desc=u"说明", content="",app_name=""):
    template = get_transmission_template_co(content,app_name)
    # 设置APNS信息
    apnpayload = APNPayload()
    apnpayload.badge = 1
    # apnpayload.sound = "test1.wav"
    apnpayload.contentAvailable = 1
    apnpayload.category = "ACTIONABLE"
    # # 简单类型如下设置
    # alertMsg = SimpleAlertMsg()
    # alertMsg.alertMsg = desc
    #字典类型如下设置
    alertMsg = DictionaryAlertMsg()
    alertMsg.body = desc
    alertMsg.actionLocKey = 'actionLockey'
    alertMsg.locKey = desc.encode("utf-8")
    alertMsg.locArgs=['loc-args']
    alertMsg.launchImage = 'launchImage'
    # IOS8.2以上版本支持
    alertMsg.title = title
    #alertMsg.titleLocArgs = ['TitleLocArg']
    #alertMsg.titleLocKey = 'TitleLocKey'
    #可以设置字典类型AlertMsg和简单类型AlertMsg其中之一
    apnpayload.alertMsg = alertMsg
    apnpayload.addCustomMsg("result", content)
    template.setApnInfo(apnpayload)
    return template

