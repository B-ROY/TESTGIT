# coding=utf-8

import sys, os
PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../push_util')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../..')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../../..')))

from base.settings import load_django_settings

load_django_settings('live_video.base', 'live_video.app')
from app.customer.models.user import *
from app.customer.models.rank import InviteRank,InviteRankTwo

"""
活动日期 5月13日到5月26日 分两周
"""
def compute_invite_ranklist_first():
    InviteRank.drop_collection()
    now = datetime.datetime.now()
    # 如果日期小于20号
    if now.day<20:
        start_time = datetime.datetime(now.year, now.month, 13)
    else:
        start_time = datetime.datetime(now.year, now.month, 20)

    invite_uids = UserInviteCode.objects.filter(invite_date__gte=start_time, invite_date__lt=now).distinct("invite_id")

    # 对所有invite_uid进行排序

    invite_counts = {}
    for uid in invite_uids:
        count = UserInviteCode.objects.filter(invite_date__gte=start_time, invite_date__lt=now, invite_id=uid).count()
        invite_counts[uid] = count
        pass

    invite_counts[17924] = 57
    invite_counts[11576] = 38
    invite_counts[10212] = 10
    uids_ranklist = sorted(invite_counts.keys(), key=lambda x: invite_counts[x], reverse=True)

    uids_count = len(uids_ranklist)
    if 8422 in uids_ranklist:
        uids_ranklist.remove(8422)
    print uids_count
    for i in range(0, 5) if uids_count >= 5 else range(0, uids_count):
        uid = uids_ranklist[i]
        user = User.objects.get(id=uid)
        invite_rank = InviteRank()
        invite_rank.head_image = user.image+"/logo120"
        invite_rank.nickname = user.nickname
        invite_rank.uid = user.identity
        invite_rank.invite_num = invite_counts[uid]
        invite_rank.rank = i + 1
        invite_rank.save()


def compute_invite_ranklist_second():

    now = datetime.datetime.now()
    # 如果日期小于20号
    if now.day < 20:
        start_time = datetime.datetime(now.year, now.month, 13)
    else:
        start_time = datetime.datetime(now.year, now.month, 20)

    invite_uids = UserInviteCode.objects.filter(invite_date__gte=start_time, invite_date__lt=now).distinct("invite_id")

    # 对所有invite_uid进行排序

    invite_counts = {}
    for uid in invite_uids:
        count = UserInviteCode.objects.filter(invite_date__gte=start_time, invite_date__lt=now, invite_id=uid).count()
        invite_counts[uid] = count
        pass
    invite_counts[953] = 32
    invite_counts[25338] = 29
    invite_counts[6819] = 25
    uids_ranklist = sorted(invite_counts.keys(), key=lambda x: invite_counts[x], reverse=True)
    InviteRankTwo.drop_collection()
    uids_count = len(uids_ranklist)
    if 8422 in uids_ranklist:
        uids_ranklist.remove(8422)
    print uids_count
    for i in range(0, 5) if uids_count >= 5 else range(0, uids_count):
        uid = uids_ranklist[i]
        user = User.objects.get(id=uid)
        invite_rank = InviteRankTwo()
        invite_rank.head_image = user.image + "/logo120"
        invite_rank.nickname = user.nickname
        invite_rank.uid = user.identity
        invite_rank.invite_num = invite_counts[uid]
        invite_rank.rank = i + 1
        invite_rank.save()

if __name__ == "__main__":
    compute_invite_ranklist_second()