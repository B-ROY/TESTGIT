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
from app.customer.models.rank import *
from operator import attrgetter


def compute_7_rank_list_first():

    CharmRank.drop_collection()
    WealthRank.drop_collection()
    now_time = datetime.datetime.now()

    end_time = datetime.datetime(now_time.year, now_time.month, now_time.day, 3,0,0)
    start_time = end_time - datetime.timedelta(days=7)
    # 现在只是送礼的时候增加魅力
    charm_record_list = TradeTicketRecord.objects.filter(created_time__gte=start_time, created_time__lt=end_time,
                                                         trade_type=TradeTicketRecord.TradeTypeGift)
    wealth_record_list = TradeDiamondRecord.objects.filter(created_time__gte=start_time, created_time__lt=end_time,
                                                           trade_type=TradeDiamondRecord.TradeTypeGift)

    charm_rank_list = {}
    wealth_rank_list = {}

    #循环计算榜单
    for charm_record in charm_record_list:
        if charm_record.user.id in charm_rank_list:
            charm_rank_list[charm_record.user.id].charm = charm_rank_list[charm_record.user.id].charm +charm_record.ticket/10
        else:
            charm_rank = CharmRank(user=charm_record.user, charm=charm_record.ticket/10)
            charm_rank_list[charm_record.user.id] = charm_rank

    for wealth_record in wealth_record_list:
        if wealth_record.user.id in wealth_rank_list:
            wealth_rank_list[wealth_record.user.id].wealth = wealth_rank_list[wealth_record.user.id].wealth + wealth_record.diamon/10
        else:
            wealth_rank = WealthRank(user=wealth_record.user, wealth=wealth_record.diamon/10)
            wealth_rank_list[wealth_record.user.id] = wealth_rank

    charmlist = charm_rank_list.values()
    wealthlist = wealth_rank_list.values()

    charmlist.sort(key=attrgetter("charm"), reverse=True)
    wealthlist.sort(key=attrgetter("wealth"), reverse=True)

    for i in range(0, len(charmlist)):
        if i > 29:
            break
        print charmlist[i].rank

        charmlist[i].rank = i + 1
        charmlist[i].change_status = 0
        print type(charmlist[i].rank)

        charmlist[i].save()

    for i in range(0, len(wealthlist)):
        if i > 29:
            break
        wealthlist[i].rank = i + 1
        wealthlist[i].change_status = 0
        wealthlist[i].save()


def compute_7_rank_list_delta():
    now_time = datetime.datetime.now()
    end_time = datetime.datetime(now_time.year, now_time.month, now_time.day, 3,0,0)
    start_time = end_time - datetime.timedelta(days=7)
    # 现在只是送礼的时候增加魅力
    charm_record_list = TradeTicketRecord.objects.filter(created_time__gte=start_time, created_time__lt=end_time,
                                                         trade_type=TradeTicketRecord.TradeTypeGift)
    wealth_record_list = TradeDiamondRecord.objects.filter(created_time__gte=start_time, created_time__lt=end_time,
                                                           trade_type=TradeDiamondRecord.TradeTypeGift)
    charm_rank_list = {}
    wealth_rank_list = {}

    #循环计算榜单
    for charm_record in charm_record_list:
        if charm_record.user.id in charm_rank_list:
            charm_rank_list[charm_record.user.id].charm = charm_rank_list[charm_record.user.id].charm +charm_record.ticket/10
        else:
            charm_rank = CharmRank(user=charm_record.user, charm=charm_record.ticket/10)
            charm_rank_list[charm_record.user.id] = charm_rank

    for wealth_record in wealth_record_list:
        if wealth_record.user.id in wealth_rank_list:
            wealth_rank_list[wealth_record.user.id].wealth = wealth_rank_list[wealth_record.user.id].wealth + wealth_record.diamon/10
        else:
            wealth_rank = WealthRank(user=wealth_record.user, wealth=wealth_record.diamon/10)
            wealth_rank_list[wealth_record.user.id] = wealth_rank

    charmlist = charm_rank_list.values()
    wealthlist = wealth_rank_list.values()

    charmlist.sort(key=attrgetter("charm"), reverse=True)
    wealthlist.sort(key=attrgetter("wealth"), reverse=True)

    # 上周user_list
    old_charm_user_ids = {}
    old_wealth_user_ids = {}

    old_charm_ranks = CharmRank.objects.all()
    old_wealth_ranks = WealthRank.objects.all()
    for old_charm in old_charm_ranks:
        old_charm_user_ids[old_charm.user.id] = old_charm.rank

    for old_wealth in old_wealth_ranks:
        old_wealth_user_ids[old_wealth.user.id] = old_wealth.rank

    CharmRank.drop_collection()
    WealthRank.drop_collection()
    print old_charm_user_ids

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
    # compute_7_rank_list_first()
    compute_7_rank_list_delta()
