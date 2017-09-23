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
    qingcun = "597ef85718ce420b7d46ce11"
    gaoqing = "59c61e3718ce4216c1c87ab9"
    usersss = User.objects.filter(is_video_auth = 1,is_block__ne =1).order_by("is_vip")
    firstsort = []
    stuiqingchunanchors =[]
    for u in usersss:
        if stuilabel in u.label and qingcun in u.label and gaoqing in u.label:
            firstsort.append(u)
        elif stuilabel in u.label and qingcun in u.label:
            stuiqingchunanchors.append(u)
    users = []
    user_recommed_id = []
    user_recommed_id_all = []
    usermap = {}

    stuiqingchunanchors = firstsort + stuiqingchunanchors
    randomstui = []
    for stui in stuiqingchunanchors:
        user_heart = UserHeartBeat.objects.get(user=stui)
        if user_heart.last_report_time > pre_time and stui.disturb_mode!=1:
            randomstui.append(stui)
    for user in randomstui:
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
                dic["check_real_video"] = 1
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
                dic["check_real_video"] = 1

            self.append(user.id)
            usermap[str(user.id)] = json.dumps(dic)
            user_recommed_id.append(user.id)

    deletetui()
    print "===================self",self
    if user_recommed_id:
        UserRedis.add_user_recommed_id_pure(user_recommed_id)
        UserRedis.add_user_recommed_id_all_pure(user_recommed_id_all)
        UserRedis.add_user_recommed_pure(usermap)
    push_index_anchor(self)

def push_index_anchor(self):
    users = []
    usermap = {}
    qingcun = "597ef85718ce420b7d46ce11"

    randomvalist1 =[]
    index_id_all = []
    anchors = User.objects.filter(is_video_auth = 1,is_block__ne =1).order_by("is_vip")
    for anchor in anchors:
       if qingcun in  anchor.label:
           randomvalist1.append(anchor)

    index_id = []
    for qingcun in randomvalist1:
        if qingcun not in users :
            users.append(qingcun)

    zaixianbururao = []
    zaixiancall =[]
    zaixianwurao = []
    lixian = []
    for user in users:
        if user.id == 1 or user.id == 2:
            continue
        import time
        time = int(time.time())
        pre_time = time - 3600
        user_beat = UserHeartBeat.objects.filter(user=user, last_report_time__gte=pre_time).first()
        if user_beat:
            if user.audio_status == 2:
                if user.disturb_mode == 0:
                    zaixianbururao.append(user)
                else:
                    zaixianwurao.append(user)
            else:
                zaixiancall.append(user)
        else:
            lixian.append(user)
    finalusers = zaixianbururao + zaixiancall + zaixianwurao
    for user in finalusers:
        if user.id not in self:
            index_id_all.append(user.id)
            personal_tags = UserTags.get_usertags(user_id=user.id)
            if not personal_tags:
                personal_tags = []
            user_vip = UserVip.objects.filter(user_id=user.id).first()

            is_online = 1
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
                dic["check_real_video"] = 1
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
                dic["check_real_video"] = 1
            usermap[str(user.id)] = json.dumps(dic)
            index_id.append(user.id)
    for user in lixian:
        if user.id not in self:
            index_id_all.append(user.id)
            personal_tags = UserTags.get_usertags(user_id=user.id)
            if not personal_tags:
                personal_tags = []
            user_vip = UserVip.objects.filter(user_id=user.id).first()

            is_online = 0
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
                dic["check_real_video"] = 1
            usermap[str(user.id)] = json.dumps(dic)
            index_id.append(user.id)
    deleteanchor()
    print "==================index_id",index_id
    UserRedis.add_index_id_pure(index_id)
    UserRedis.add_index_id_all_pure(index_id_all)
    UserRedis.add_index_anchor_pure(usermap)
    print "=============首页清纯数据入redis完毕"

def deletetui():
    UserRedis.delete_user_recommed_pure()
    UserRedis.delete_user_recommed_id_pure()
    UserRedis.delete_user_recommed_id_all_pure()

def deleteanchor():
    UserRedis.delete_index_anchor_pure()
    UserRedis.delete_index_anchor_id_pure()
    UserRedis.delete_index_anchor_id_all_pure()


if __name__ == "__main__":
    RECOMMENTID=[]
    pushredis(RECOMMENTID)