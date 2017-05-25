#coding=utf-8


from app.customer.models import UserHeartBeat
from app.customer.models import User
import time


def gen_user_heart():
    users = User.objects.all()
    for user in users:
        user_heart_beat = UserHeartBeat()
        user_heart_beat.user = user
        user_heart_beat.last_report_time = user.id
        user_heart_beat.save()

