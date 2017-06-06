# coding=utf-8

from app.customer.models.user import User
from app.customer.models.user import VideoManagerVerify
from app.customer.models.user import UserHeartBeat
from app.customer.models.account import *
from app.customer.models.vip import *
from app.customer.models.rank import *


# 新人驾到 定时任务
def new_anchors():

    user_list = []

    # 获取当前时间的前两分钟
    import time
    time = int(time.time())
    pre_time = time - 60 * 10

    verify_list = VideoManagerVerify.objects.filter(status=1).order_by("-verify_time")[0:200]
    for verify in verify_list:
        user = User.objects.filter(id=verify.user_id).first()
        user_beat = UserHeartBeat.objects.filter(user=user, last_report_time__gte=pre_time)
        if user_beat:
            user_list.append(user)

    NewAnchorRank.drop_collection()

    for user in user_list:
            anchor = NewAnchorRank()
            anchor.user_id = user.id
            anchor.save()


# 千里眼 定时任务
def clairvoyant_rank():
    user_list = []

    accounts = Account.objects.all().order_by("-diamond")

    # 获取当前时间的前两分钟
    import time
    time = int(time.time())
    pre_time = time - 60 * 60 * 10

    for account in accounts:
        user = account.user
        user_beat = UserHeartBeat.objects.filter(user=user, last_report_time__gte=pre_time)
        if user_beat:
            if len(user_list) == 5:
                break
            else:
                user_list.append(user.id)

    ClairvoyantRank.drop_collection()

    for id in user_list:
        rank = ClairvoyantRank()
        rank.user_id = id
        rank.save()



