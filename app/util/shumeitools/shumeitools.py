# -*- coding: utf-8 -*-

import json
import time
import urllib2

PIC_CHANNEL = [
    (1,"IMAGE", "图像（默认值）"),
    (2,"HEAD_IMG", "用户头像"),
    (3,"CHAT_IMG", "聊天图片"),
]

TEXT_CHANNEL = [
    (1, "NICKNAME"),
    (2, "MESSAGE"),
    (3, "PROFILE")
]

ACCESS_KEY = "IBIIH3VkFvqAEmGC3YpJ"
TEXT_TYPE = "SOCIAL"
PIC_TYPE = "AD_PORN"

def shumei_image_detect(pic_url, timeout,user_id,channel,sex,phone):
    channel_desc = "IMAGE"
    if channel==1:
        channel_desc = "IMAGE"
    elif channel == 2:
        channel_desc = "HEAD_IMGE"
    elif channel == 3:
        channel_desc = "CHAT_IMG"
    data = {"img": pic_url, "tokenId": str(user_id), "channel": channel_desc}
    playload = {"accessKey": ACCESS_KEY, "type": PIC_TYPE, "data": data, "sex":sex, "age":0, "phone":phone}
    body = json.dumps(playload)
    shumei_url = "http://api.fengkongcloud.com/v2/saas/anti_fraud/img"
    start_time = int(time.time()*1000)
    request = urllib2.Request(shumei_url, body)
    shumei_result = urllib2.urlopen(request, timeout=timeout).read()
    end_time = int(time.time()*1000)
    duration = end_time - start_time
    encode_result = json.loads(shumei_result)
    print encode_result
    if (encode_result["code"] == 1100):
        risk_level = encode_result["riskLevel"]
        detail = encode_result["detail"]
    elif (encode_result["code"] == 1902):
        # 参数不合法
        pass
    elif (encode_result["code"] == 1903):
        # 服务失败
        pass
    elif (encode_result["code"] == 9100):
        # 余额不足
        pass
    elif (encode_result["code"] == 9101):
        # 无权限操作
        pass
    else:
        # 不明错误
        pass
    return encode_result, duration


def shumei_text_spam(text, timeout, user_id, channel, nickname,phone,ip):
    channel_desc = ""
    if channel == 1:
        channel_desc = "IMAGE"
    elif channel == 2:
        channel_desc = "HEAD_IMG"
    elif channel == 3:
        channel_desc = "CHAT_IMG"
    data = {"text": text, "tokenId": str(user_id), "channel": channel_desc, "nickname": nickname, "phone":phone, "ip":ip, }
    playload = {"accessKey": ACCESS_KEY, "type": TEXT_TYPE, "data": data}
    body = json.dumps(playload)
    shumei_url = "http://api.fengkongcloud.com/v2/saas/anti_fraud/text"
    request = urllib2.Request(shumei_url, body)
    start_time = int(time.time()*1000)
    shumei_result = urllib2.urlopen(request, timeout=timeout).read()
    end_time = int(time.time()*1000)
    duration = end_time - start_time
    encode_result = json.loads(shumei_result)
    #shumei_result = requests.post(shumei_url, data=body, timeout=timeout)
    #encode_result = json.loads(shumei_result.text)
    return encode_result, duration