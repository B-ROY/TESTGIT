# coding=utf-8

from app.customer.models.user import User
from app.customer.models.user import VideoManagerVerify
from app.customer.models.user import UserHeartBeat
from app.customer.models.rank import NewAnchorRank
# 新人驾到 定时任务
def new_anchors():

    user_list = []

    # 获取当前时间的前两分钟
    import time
    time = int(time.time())
    pre_time = time - 60 * 5

    verify_list = VideoManagerVerify.objects.filter(status=1).order_by("-verify_time")[0:200]
    for verify in verify_list:
        user = User.objects.filter(id=verify.user_id).first()
        user_beat = UserHeartBeat.objects.filter(user=user, last_report_time__gte=pre_time)
        if user_beat:
            user_list.append(user)
    count = NewAnchorRank.objects.all().count()
    for user in user_list:
        if count == 0:
            anchor = NewAnchorRank()
            anchor.user_id = user.id
            anchor.save()
        else:
            u = NewAnchorRank.objects.filter(user_id=user.id).first()
            if u:
                continue
            else:
                anchor = NewAnchorRank()
                anchor.user_id = user.id
                anchor.save()
            db_anchor = NewAnchorRank.objects.all.first()
            if db_anchor:
                db_anchor.delete()
