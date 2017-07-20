# -*- coding: utf-8 -*-
import os
import sys

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../..')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../../..')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../../../..')))

from base.settings import load_django_settings

load_django_settings('live_video.base', 'live_video.app')
from redis_model.queue import Worker


import time
import logging
import datetime
from app.customer.models.vip import *
from app.customer.models.rank import *


# 新人驾到
def new_anchors():
    user_list = []

    # 获取当前时间的前五分钟
    import time
    time = int(time.time())
    pre_time = time - 60 * 5

    verify_list = VideoManagerVerify.objects.filter(status=1).order_by("-verify_time")[0:400]
    for verify in verify_list:
        user = User.objects.filter(id=verify.user_id).first()
        user_beat = UserHeartBeat.objects.filter(user=user, last_report_time__gte=pre_time)
        if user_beat and user.gender == 2 and user.disturb_mode == 0:
            if user not in user_list:
                user_list.append(user)

    NewAnchorRank.drop_collection()

    for user in user_list:
        anchor = NewAnchorRank()
        anchor.user_id = user.id
        anchor.save()
    print "new_anchors success"


# 千里眼定时任务
def clairvoyant_rank():
    user_list = []
    accounts = Account.objects.all().order_by("-diamond")
    # 获取当前时间的前五分钟
    import time
    time = int(time.time())
    pre_time = time - 60 * 5

    for account in accounts:
        user = account.user
        user_beat = UserHeartBeat.objects.filter(user=user, last_report_time__gte=pre_time)
        if user_beat:
            if user.is_video_auth == 1:
                continue

            if len(user_list) == 6:
                break
            else:
                if user.gender == 1:
                    user_list.append(user.id)

    ClairvoyantRank.drop_collection()

    for id in user_list:
        rank = ClairvoyantRank()
        rank.user_id = id
        rank.save()
    print "clairvoyant_rank success"

if __name__ == "__main__":
    new_anchors()
    clairvoyant_rank()