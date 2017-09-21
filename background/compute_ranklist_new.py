# -*- coding: utf-8 -*-
import os
import sys

import datetime
PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../push_util')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../..')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../../..')))

from base.settings import load_django_settings

load_django_settings('live_video.base', 'live_video.app')

from app.customer.models.account import *
from app.customer.models.rank import CharmRankNew, WealthRankNew
from operator import attrgetter
from app.customer.models.gift import GiftRecord, Gift


def compute_7_rank_list_first():
    CharmRankNew.objects.filter(type=1).delete()
    WealthRankNew.objects.filter(type=1).delete()

    now_time = datetime.datetime.now()
    now_date = datetime.datetime(now_time.year, now_time.month, now_time.day)
    start_date = now_date - datetime.timedelta(days=7)
    end_date = now_date - datetime.timedelta(days=1)
    start_time = start_date.strftime("%Y-%m-%d 00:00:00")
    end_time = end_date.strftime('%Y-%m-%d 23:59:59')

    gifts = Gift.objects.filter(gift_type__in=[1, 2])
    gift_dict = {}
    charm_value = 0
    wealth_value = 0
    for gift in gifts:
        gift_id = str(gift.id)
        if gift.charm_value:
            charm_value = gift.charm_value
        if gift.wealth_value:
            wealth_value = gift.wealth_value
        data = {}
        data["charm"] = charm_value
        data["wealth"] = wealth_value
        gift_dict[gift_id] = data

    records = GiftRecord.objects.filter(create_time__gte=start_time, create_time__lt=end_time)

    charm_rank_list = {}
    wealth_rank_list = {}

    # 循环计算榜单
    for record in records:
        gift_id = record.gift_id
        user_id = int(record.to_id)
        if gift_id not in gift_dict:
            continue
        if not user_id:
            continue
        user = User.objects.filter(id=user_id).first()
        if not user:
            continue

        if user.is_block == 1:
            continue

        charm = gift_dict[gift_id]["charm"] * record.gift_count
        wealth = gift_dict[gift_id]["wealth"] * record.gift_count

        if user.is_video_auth == 1:
            if user_id in charm_rank_list:
                charm_rank_list[user_id].charm = charm_rank_list[user_id].charm + charm
            else:
                charm_rank = CharmRankNew(user=user, charm=charm, type=1)
                charm_rank_list[user_id] = charm_rank

        if user_id in wealth_rank_list:
            wealth_rank_list[user_id].wealth = wealth_rank_list[user_id].wealth + wealth
        else:
            wealth_rank = WealthRankNew(user=user, wealth=wealth, type=1)
            wealth_rank_list[user_id] = wealth_rank

    charmlist = charm_rank_list.values()
    wealthlist = wealth_rank_list.values()

    charmlist.sort(key=attrgetter("charm"), reverse=True)
    wealthlist.sort(key=attrgetter("wealth"), reverse=True)

    for i in range(0, len(charmlist)):
        if i > 29:
            break

        charmlist[i].rank = i + 1
        charmlist[i].change_status = 0

        charmlist[i].save()

    for i in range(0, len(wealthlist)):
        if i > 29:
            break
        wealthlist[i].rank = i + 1
        wealthlist[i].change_status = 0
        wealthlist[i].save()


def compute_7_rank_list_delta():

    now_time = datetime.datetime.now()
    now_date = datetime.datetime(now_time.year, now_time.month, now_time.day)
    start_date = now_date - datetime.timedelta(days=7)
    end_date = now_date - datetime.timedelta(days=1)
    start_time = start_date.strftime("%Y-%m-%d 00:00:00")
    end_time = end_date.strftime('%Y-%m-%d 23:59:59')

    gifts = Gift.objects.filter(gift_type__in=[1, 2])
    gift_dict = {}
    charm_value = 0
    wealth_value = 0
    for gift in gifts:
        gift_id = str(gift.id)
        if gift.charm_value:
            charm_value = gift.charm_value
        if gift.wealth_value:
            wealth_value = gift.wealth_value

        data = {}
        data["charm"] = charm_value
        data["wealth"] = wealth_value
        gift_dict[gift_id] = data

    records = GiftRecord.objects.filter(create_time__gte=start_time, create_time__lt=end_time)

    charm_rank_list = {}
    wealth_rank_list = {}

    # 循环计算榜单
    for record in records:
        gift_id = record.gift_id
        user_id = int(record.to_id)
        if gift_id not in gift_dict:
            continue
        if not user_id:
            continue
        user = User.objects.filter(id=user_id).first()
        if not user:
            continue
        if user.is_block == 1:
            continue
        charm = gift_dict[gift_id]["charm"] * record.gift_count
        wealth = gift_dict[gift_id]["wealth"] * record.gift_count

        if user.is_video_auth == 1:
            if user_id in charm_rank_list:
                charm_rank_list[user_id].charm = charm_rank_list[user_id].charm + charm
            else:
                charm_rank = CharmRankNew(user=user, charm=charm, type=1)
                charm_rank_list[user_id] = charm_rank

        if user_id in wealth_rank_list:
            wealth_rank_list[user_id].wealth = wealth_rank_list[user_id].wealth + wealth
        else:
            wealth_rank = WealthRankNew(user=user, wealth=wealth, type=1)
            wealth_rank_list[user_id] = wealth_rank

    charmlist = charm_rank_list.values()
    wealthlist = wealth_rank_list.values()

    charmlist.sort(key=attrgetter("charm"), reverse=True)
    wealthlist.sort(key=attrgetter("wealth"), reverse=True)

    # 上周user_list
    old_charm_user_ids = {}
    old_wealth_user_ids = {}

    old_charm_ranks = CharmRankNew.objects.filter(type=1)
    old_wealth_ranks = WealthRankNew.objects.filter(type=1)
    for old_charm in old_charm_ranks:
        old_charm_user_ids[old_charm.user.id] = old_charm.rank

    for old_wealth in old_wealth_ranks:
        old_wealth_user_ids[old_wealth.user.id] = old_wealth.rank

    CharmRankNew.objects.filter(type=1).delete()
    WealthRankNew.objects.filter(type=1).delete()

    for i in range(0, len(charmlist)):
        if i > 29:
            break
        rank = i + 1
        u_id = charmlist[i].user.id
        charmlist[i].rank = rank
        db_charm = charmlist[i].save()
        db_charm.update(set__change_status=0)
        if int(u_id) not in old_charm_user_ids:
            db_charm.update(set__change_status=1)
        else:
            old_rank = old_charm_user_ids[u_id]
            if old_rank > rank:
                db_charm.update(set__change_status=1)
            elif old_rank < rank:
                db_charm.update(set__change_status=2)


    for i in range(0, len(wealthlist)):
        if i > 29:
            break
        rank = i + 1
        wealthlist[i].rank = rank
        u_id = wealthlist[i].user.id
        db_wealth = wealthlist[i].save()
        db_wealth.update(set__change_status=0)
        if u_id not in old_wealth_user_ids:
            db_wealth.update(set__change_status=1)
        else:
            old_rank = old_wealth_user_ids[u_id]
            if old_rank > rank:
                db_wealth.update(set__change_status=1)
            elif old_rank < rank:
                db_wealth.update(set__change_status=2)


def compute_1_rank_list_first():

    CharmRankNew.objects.filter(type=2).delete()
    WealthRankNew.objects.filter(type=2).delete()

    now_time = datetime.datetime.now()
    now_date = datetime.datetime(now_time.year, now_time.month, now_time.day)
    start_date = now_date - datetime.timedelta(days=1)

    start_time = start_date.strftime("%Y-%m-%d 00:00:00")
    end_time = start_date.strftime('%Y-%m-%d 23:59:59')

    gifts = Gift.objects.filter(gift_type__in=[1, 2])
    gift_dict = {}
    charm_value = 0
    wealth_value = 0
    for gift in gifts:
        gift_id = str(gift.id)
        if gift.charm_value:
            charm_value = gift.charm_value
        if gift.wealth_value:
            wealth_value = gift.wealth_value
        data = {}
        data["charm"] = charm_value
        data["wealth"] = wealth_value
        gift_dict[gift_id] = data

    records = GiftRecord.objects.filter(create_time__gte=start_time, create_time__lt=end_time)

    charm_rank_list = {}
    wealth_rank_list = {}

    # 循环计算榜单
    for record in records:
        gift_id = record.gift_id
        user_id = int(record.to_id)
        if gift_id not in gift_dict:
            continue
        if not user_id:
            continue
        user = User.objects.filter(id=user_id).first()
        if not user:
            continue

        if user.is_block == 1:
            continue

        charm = gift_dict[gift_id]["charm"] * record.gift_count
        wealth = gift_dict[gift_id]["wealth"] * record.gift_count

        if user.is_video_auth == 1:
            if user_id in charm_rank_list:
                charm_rank_list[user_id].charm = charm_rank_list[user_id].charm + charm
            else:
                charm_rank = CharmRankNew(user=user, charm=charm, type=2)
                charm_rank_list[user_id] = charm_rank

        if user_id in wealth_rank_list:
            wealth_rank_list[user_id].wealth = wealth_rank_list[user_id].wealth + wealth
        else:
            wealth_rank = WealthRankNew(user=user, wealth=wealth, type=2)
            wealth_rank_list[user_id] = wealth_rank

    charmlist = charm_rank_list.values()
    wealthlist = wealth_rank_list.values()

    charmlist.sort(key=attrgetter("charm"), reverse=True)
    wealthlist.sort(key=attrgetter("wealth"), reverse=True)

    for i in range(0, len(charmlist)):
        if i > 29:
            break

        charmlist[i].rank = i + 1
        charmlist[i].change_status = 0

        charmlist[i].save()

    for i in range(0, len(wealthlist)):
        if i > 29:
            break
        wealthlist[i].rank = i + 1
        wealthlist[i].change_status = 0
        wealthlist[i].save()


def compute_1_rank_list_delta():

    now_time = datetime.datetime.now()
    now_date = datetime.datetime(now_time.year, now_time.month, now_time.day)
    start_date = now_date - datetime.timedelta(days=1)

    start_time = start_date.strftime("%Y-%m-%d 00:00:00")
    end_time = start_date.strftime('%Y-%m-%d 23:59:59')

    gifts = Gift.objects.filter(gift_type__in=[1, 2])
    gift_dict = {}
    charm_value = 0
    wealth_value = 0
    for gift in gifts:
        gift_id = str(gift.id)
        if gift.charm_value:
            charm_value = gift.charm_value
        if gift.wealth_value:
            wealth_value = gift.wealth_value

        data = {}
        data["charm"] = charm_value
        data["wealth"] = wealth_value
        gift_dict[gift_id] = data

    records = GiftRecord.objects.filter(create_time__gte=start_time, create_time__lt=end_time)

    charm_rank_list = {}
    wealth_rank_list = {}

    # 循环计算榜单
    for record in records:
        gift_id = record.gift_id
        user_id = int(record.to_id)
        if gift_id not in gift_dict:
            continue
        if not user_id:
            continue
        user = User.objects.filter(id=user_id).first()
        if not user:
            continue

        if user.is_block == 1:
            continue

        charm = gift_dict[gift_id]["charm"] * record.gift_count
        wealth = gift_dict[gift_id]["wealth"] * record.gift_count

        if user.is_video_auth == 1:
            if user_id in charm_rank_list:
                charm_rank_list[user_id].charm = charm_rank_list[user_id].charm + charm
            else:
                charm_rank = CharmRankNew(user=user, charm=charm, type=2)
                charm_rank_list[user_id] = charm_rank

        if user_id in wealth_rank_list:
            wealth_rank_list[user_id].wealth = wealth_rank_list[user_id].wealth + wealth
        else:
            wealth_rank = WealthRankNew(user=user, wealth=wealth, type=2)
            wealth_rank_list[user_id] = wealth_rank

    charmlist = charm_rank_list.values()
    wealthlist = wealth_rank_list.values()

    charmlist.sort(key=attrgetter("charm"), reverse=True)
    wealthlist.sort(key=attrgetter("wealth"), reverse=True)

    # 上周user_list
    old_charm_user_ids = {}
    old_wealth_user_ids = {}

    old_charm_ranks = CharmRankNew.objects.filter(type=2)
    old_wealth_ranks = WealthRankNew.objects.filter(type=2)
    for old_charm in old_charm_ranks:
        old_charm_user_ids[old_charm.user.id] = old_charm.rank

    for old_wealth in old_wealth_ranks:
        old_wealth_user_ids[old_wealth.user.id] = old_wealth.rank

    CharmRankNew.objects.filter(type=2).delete()
    WealthRankNew.objects.filter(type=2).delete()

    for i in range(0, len(charmlist)):
        if i > 29:
            break
        rank = i + 1
        u_id = charmlist[i].user.id
        charmlist[i].rank = rank
        db_charm = charmlist[i].save()
        db_charm.update(set__change_status=0)
        if int(u_id) not in old_charm_user_ids:
            db_charm.update(set__change_status=1)
        else:
            old_rank = old_charm_user_ids[u_id]
            if old_rank > rank:
                db_charm.update(set__change_status=1)
            elif old_rank < rank:
                db_charm.update(set__change_status=2)


    for i in range(0, len(wealthlist)):
        if i > 29:
            break
        rank = i + 1
        wealthlist[i].rank = rank
        u_id = wealthlist[i].user.id
        db_wealth = wealthlist[i].save()
        db_wealth.update(set__change_status=0)
        if u_id not in old_wealth_user_ids:
            db_wealth.update(set__change_status=1)
        else:
            old_rank = old_wealth_user_ids[u_id]
            if old_rank > rank:
                db_wealth.update(set__change_status=1)
            elif old_rank < rank:
                db_wealth.update(set__change_status=2)


if __name__ == '__main__':
    compute_7_rank_list_first()
    compute_1_rank_list_first()

    now = datetime.datetime.now()
    week_num = now.weekday()
    if int(week_num) == 0:
        compute_7_rank_list_delta()

    compute_1_rank_list_delta()
