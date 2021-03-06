# coding=utf-8
import sys
import os.path

import time


PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../..')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../../..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), "", "base", "site-packages")))
sys.path.insert(1, os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), "", "base", "site-packages", "django_admin_bootstrapped")))

from base.settings import load_django_settings
load_django_settings('live_video.base', 'live_video.app')

from app.customer.models import UserHeartBeat, User
from app.customer.models.hotAnchor import Anchor
from app.customer.models.personal_tags import UserTags
from app.customer.models.real_video_verify import RealVideoVerify
from app.customer.models.vip import Vip, UserVip
from app_redis.user.models.user import UserRedis
from app.audio.models import AudioRoomRecord
import json
import random

def pushredis(self):
    now_time = int(time.time())
    #pre_time = now_time - 120
    pre_time = now_time - 3600
    # heartbeats = UserHeartBeat.objects.filter(last_report_time__gte=pre_time)
    stuilabel ="598d7a2418ce423b1222d645" #首推标签id
    usersss = User.objects.filter(is_video_auth = 1,is_block__ne =1).order_by("is_vip")
    stuianchors =[]
    for u in usersss:
        if stuilabel in u.label:
            stuianchors.append(u)
    hots=[]
    users = []
    user_recommed_id = []
    user_recommed_id_all = []
    usermap = {}
    anchors = Anchor.objects.filter().order_by("seq")

    for anchor in anchors:
        user = User.objects.get(id=anchor.sid)
        user_heart = UserHeartBeat.objects.get(user=user)
        if user_heart.last_report_time > pre_time and user.disturb_mode != 1:
            hots.append(user)
    randomstui = []
    for stui in stuianchors:
        user_heart = UserHeartBeat.objects.get(user=stui)
        if user_heart.last_report_time > pre_time and stui.disturb_mode!=1:
            randomstui.append(stui)
    # hot 和 stulist
    # random.shuffle(hots)
    random.shuffle(randomstui)

    hots = hots + randomstui


    for user in hots:
        if user.id in users:
            continue
        users.append(user.id)
        personal_tags = UserTags.get_usertags(user_id=user.id)
        if not personal_tags:
            personal_tags = []

        user_vip = UserVip.objects.filter(user_id=user.id).first()

        # time = int(time.time())
        # pre_time = time - 120
        user_beat = UserHeartBeat.objects.filter(user=user, last_report_time__gte=pre_time).first()
        if user_beat:
            is_online = 1
            # else:
            #     is_online = 0
            user_recommed_id_all.append(user.id)
            roomrecord = AudioRoomRecord.objects.filter(user_id=user.id).order_by("-open_time").first()
            if not user_vip:
                dic = {
                    "user":{
                        "_uid": user.sid,
                        "logo_big":user.image,
                        "nickname":user.nickname,
                        "desc":user.desc
                    },
                    "personal_tags": personal_tags,
                    "is_online": is_online
                }
            else:
                vip = Vip.objects.filter(id=user_vip.vip_id).first()
                dic = {
                    "user":{
                        "_uid": user.sid,
                        "logo_big":user.image,
                        "nickname":user.nickname,
                        "desc":user.desc
                    },
                    "personal_tags": personal_tags,
                    "vip": {
                        "vip_type": vip.vip_type,
                        "icon_url": Vip.convert_http_to_https(vip.icon_url)
                    },
                    "is_online": is_online
                }

            show_video = RealVideoVerify.objects(user_id=user.id, status=1).order_by("-update_time").first()
            if show_video:
                dic["check_real_video"] = show_video.status
            else:
                real_video = RealVideoVerify.objects(user_id=user.id, status__ne=2).order_by("-update_time").first()
                if real_video:
                    dic["check_real_video"] = real_video.status
                else:
                    dic["check_real_video"] = 3

            self.append(user.id)
            usermap[str(user.id)] = json.dumps(dic)
            if not roomrecord or roomrecord.status == 1:
                user_recommed_id.append(user.id)
    deletetui()
    if user_recommed_id:
        UserRedis.add_user_recommed_id_v3(user_recommed_id)
        UserRedis.add_user_recommed_id_all(user_recommed_id_all)
        UserRedis.add_user_recommed_v3(usermap)
    push_index_anchor(self)

def push_index_anchor(self):
    users = []
    usermap = {}
    gaoyanzhi = "597ef92818ce420b6f46ce3f"
    xinggan = "597ef93418ce420b7d46ce17"
    yujie="597ef86b18ce420b6f46ce3c"
    qingcun = "597ef85718ce420b7d46ce11"
    nodisllpay = "59956dfb18ce427fa83c9cec"

    randomvalist1 =[]
    randomvalist2 =[]
    randomvalist3 =[]
    randomvalist4 =[]
    randomvalist5 =[]
    randomvalist6 = []
    index_id_all = []
    anchors = User.objects.filter(is_video_auth = 1,is_block__ne =1).order_by("is_vip")
    for anchor in anchors:
        if gaoyanzhi in anchor.label and xinggan in anchor.label:
            randomvalist1.append(anchor)
        elif gaoyanzhi in anchor.label and qingcun in anchor.label:
            randomvalist2.append(anchor)
        else:
            if xinggan in anchor.label:
                randomvalist3.append(anchor)
            elif qingcun in  anchor.label:
                randomvalist6.append(anchor)
            elif yujie in anchor.label:
                randomvalist4.append(anchor)
            elif not anchor.label:
                randomvalist5.append(anchor)

    random.shuffle(randomvalist1)
    random.shuffle(randomvalist2)
    random.shuffle(randomvalist3)
    random.shuffle(randomvalist4)
    random.shuffle(randomvalist5)
    random.shuffle(randomvalist6)

    valist1 = randomvalist1
    valist2 = randomvalist2
    valist3 = randomvalist3
    valist4 = randomvalist4
    valist5 = randomvalist5
    valist6 = randomvalist6

    index_id = []
    for gaoxing in valist1:
        if gaoxing not in users and gaoxing.disturb_mode ==0 and gaoxing.audio_room_id !="":
            users.append(gaoxing)
    for gaoqing in valist2:
        if gaoqing not in users and gaoqing.disturb_mode ==0 and gaoqing.audio_room_id !="":
            users.append(gaoqing)
    for xing in valist3:
        if xing not in users and xing.disturb_mode ==0 and xing.audio_room_id !="":
            users.append(xing)
    for qing in valist6:
        if qing not in users and qing.disturb_mode ==0 and qing.audio_room_id !="":
            users.append(qing)
    for yu in valist4:
        if yu not in users and yu.disturb_mode ==0 and yu.audio_room_id !="":
            users.append(yu)
    for wu in valist5 :
        if wu not in users and wu.disturb_mode ==0 and wu.audio_room_id !="":
            users.append(wu)
    for user in users:
        #if not user.audio_room_id:
        #   continue
        if user.id == 1 or user.id == 2:
            continue
        try:
            if user.id not in self and nodisllpay not in user.label:
                personal_tags = UserTags.get_usertags(user_id=user.id)
                if not personal_tags:
                    personal_tags = []
                user_vip = UserVip.objects.filter(user_id=user.id).first()

                # 是否在线 查看心跳
                import time
                time = int(time.time())
                pre_time = time - 3600
                user_beat = UserHeartBeat.objects.filter(user=user, last_report_time__gte=pre_time).first()
                roomrecord = AudioRoomRecord.objects.filter(user_id = user.id).order_by("-open_time").first()
                if user_beat and user.disturb_mode != 1:
                    index_id_all.append(user.id)

                    is_online = 1
                    # 视频认证状态
                    real_video = RealVideoVerify.objects(user_id=user.id, status__ne=2).order_by("-update_time").first()
                    show_video = RealVideoVerify.objects(user_id=user.id, status=1).order_by("-update_time").first()

                    if user_vip:
                        vip = Vip.objects.filter(id=user_vip.vip_id).first()
                        dic = {
                            "user": {
                                "_uid": user.sid,
                                "logo_big":user.image,
                                "nickname":user.nickname,
                                "desc":user.desc
                            },
                            "personal_tags": personal_tags,
                            "vip": {
                                "vip_type": vip.vip_type,
                                "icon_url": Vip.convert_http_to_https(vip.icon_url)
                            },
                            "is_online": is_online
                        }
                    else:
                        dic = {
                            "user": {
                                "_uid": user.sid,
                                "logo_big":user.image,
                                "nickname":user.nickname,
                                "desc":user.desc
                            },
                            "personal_tags": personal_tags,
                            "is_online": is_online
                        }

                    if show_video:
                        dic["check_real_video"] = show_video.status
                    else:
                        if real_video:
                            dic["check_real_video"] = real_video.status
                        else:
                            dic["check_real_video"] = 3

                    usermap[str(user.id)] = json.dumps(dic)
                    if not roomrecord or roomrecord.status == 1:
                        index_id.append(user.id)
        except Exception,e:
            print e
            #UserRedis.add_index_anchor(str(user.id),json.dumps(dic))
    deleteanchor()
    UserRedis.add_index_id_v3(index_id)
    UserRedis.add_index_id_all(index_id_all)
    UserRedis.add_index_anchor_v3(usermap)
    print "=============首页数据入redis完毕"

def deletetui():
    UserRedis.delete_user_recommed_v3()
    UserRedis.delete_user_recommed_id_v3()
    UserRedis.delete_user_recommed_id_all()

def deleteanchor():
    UserRedis.delete_index_anchor_v3()
    UserRedis.delete_index_anchor_id_v3()
    UserRedis.delete_index_anchor_id_all()


if __name__ == "__main__":
    RECOMMENTID=[]
    pushredis(RECOMMENTID)