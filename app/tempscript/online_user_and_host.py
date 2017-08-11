#coding=utf-8

from app.customer.models.user import User, UserHeartBeat
import datetime
import time


def compute_user_and_host():
    two_minutes_ago = int(time.time()) - 120
    user_beats = UserHeartBeat.objects.filter(last_report_time__gt=two_minutes_ago)
    host_num = 0
    user_num = 0
    for beat in user_beats:
       if beat.user.is_video_auth == 1:
           host_num += 1
       elif beat.user.gender == 1:
           user_num +=1
    print host_num, user_num






0