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


INTERVAL_DAYS = 3

#todo 以后可改为差值计算
def compute_3_rank_list_first():

    CharmRank.drop_collection()
    WealthRank.drop_collection()
    now_time = datetime.datetime.now()

    end_time = datetime.datetime(now_time.year, now_time.month, now_time.day, 3,0,0)
    start_time = end_time - datetime.timedelta(days=INTERVAL_DAYS)
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
        print charmlist[i].rank

        charmlist[i].rank = i + 1
        charmlist[i].change_status = 0
        print type(charmlist[i].rank)

        charmlist[i].save()

    for i in range(0, len(wealthlist)):
        wealthlist[i].rank = i + 1
        wealthlist[i].change_status = 0
        wealthlist[i].save()


def compute_3_rank_list_delta():
    # todo 存储逻辑修改
    now_time = datetime.datetime.now()
    end_time = datetime.datetime(now_time.year, now_time.month, now_time.day, 3, 0, 0)
    start_time = end_time - datetime.timedelta(days=INTERVAL_DAYS)

    end_time_last = end_time - datetime.timedelta(days=1)
    start_time_last = start_time - datetime.timedelta(days=1)

    # 魅力增量计算

    ticket_record_list_minus = TradeTicketRecord.objects.filter(created_time__gte=start_time_last, created_time__lt=start_time,
                                                                trade_type = TradeTicketRecord.TradeTypeGift)

    ticket_record_list_plus = TradeTicketRecord.objects.filter(created_time__gte=end_time_last, created_time__lt=end_time,
                                                                trade_type=TradeTicketRecord.TradeTypeGift)
    charm_rank_list = {}

    for ticket_record in ticket_record_list_minus:
        if ticket_record.user.id in charm_rank_list:
            charm_rank_list[ticket_record.user.id].charm = charm_rank_list[ticket_record.user.id].charm - ticket_record.ticket/10
        else:
            charm_rank = CharmRank(user=ticket_record.user, charm=-ticket_record.ticket/10)
            charm_rank_list[ticket_record.user.id] = charm_rank

    for ticket_record in ticket_record_list_plus:
        if ticket_record.user.id in charm_rank_list:
            charm_rank_list[ticket_record.user.id].charm = charm_rank_list[ticket_record.user.id].charm +ticket_record.ticket/10
        else:
            charm_rank = CharmRank(user=ticket_record.user, charm=ticket_record.ticket/10)
            charm_rank_list[ticket_record.user.id] = charm_rank

    charm_rank_last_list = CharmRank.objects.all()

    for charm_rank in charm_rank_last_list:
        if charm_rank.user.id in charm_rank_list:
            charm_rank_list[charm_rank.user.id].charm = charm_rank_list[charm_rank.user.id].charm + charm_rank.charm
        else:
            charm_rank_list[charm_rank.user.id] = charm_rank


    # 财富增量计算

    diamond_record_list_minus = TradeDiamondRecord.objects.filter(created_time__gte=start_time_last,
                                                                  created_time__lt=start_time,
                                                                  trade_type=TradeDiamondRecord.TradeTypeGift)

    diamond_record_list_plus = TradeDiamondRecord.objects.filter(created_time__gte=end_time_last,
                                                                 created_time__lt=end_time,
                                                                 trade_type=TradeDiamondRecord.TradeTypeGift)
    wealth_rank_list = {}

    for diamond_record in diamond_record_list_minus:
        if diamond_record.user.id in wealth_rank_list:
            wealth_rank_list[diamond_record.user.id].wealth = wealth_rank_list[
                                                                 diamond_record.user.id].wealth - diamond_record.diamon / 10
        else:
            wealth_rank = WealthRank(user=diamond_record.user, wealth=-diamond_record.diamon / 10)
            wealth_rank_list[diamond_record.user.id] = wealth_rank

    for diamond_record in diamond_record_list_plus:
        if diamond_record.user.id in wealth_rank_list:
            wealth_rank_list[diamond_record.user.id].wealth = wealth_rank_list[
                                                               diamond_record.user.id].wealth + diamond_record.diamon / 10
        else:
            wealth_rank = WealthRank(user=diamond_record.user, wealth=diamond_record.diamon / 10)
            wealth_rank_list[diamond_record.user.id] = wealth_rank

    wealth_rank_last_list = WealthRank.objects.all()

    for wealth_rank in wealth_rank_last_list:
        if wealth_rank.user.id in wealth_rank_list:
            wealth_rank_list[wealth_rank.user.id].wealth = wealth_rank_list[wealth_rank.user.id].wealth + wealth_rank.wealth
            wealth_rank_list[wealth_rank.user.id].rank = wealth_rank.rank
        else:
            wealth_rank_list[wealth_rank.user.id] = wealth_rank

    charmlist = charm_rank_list.values()
    wealthlist = wealth_rank_list.values()
    charmlist.sort(key=attrgetter("charm"), reverse=True)
    wealthlist.sort(key=attrgetter("wealth"), reverse=True)

    # todo 现在是删了再存 想改成不删直接存的

    for i in range(0, len(charmlist)):
        if i+1 > charmlist[i].rank:
            charmlist[i].change_status = 2
        elif i+1 < charmlist[i].rank:
            charmlist[i].change_status = 1
        else:
            charmlist[i].change_status = 0

        charmlist[i].rank = i + 1
        charmlist[i].save()

    for i in range(0, len(wealthlist)):
        if i+1 > wealthlist[i].rank:
            wealthlist[i].change_status = 2
        elif i+1 < wealthlist[i].rank:
            wealthlist[i].change_status = 1
        else:
            wealthlist[i].change_status = 0

        wealthlist[i].rank = i + 1
        wealthlist[i].save()



def compute_total_ranklist_first():
    wealth_users = User.objects.filter(is_block__ne=1).order_by("-wealth_value")[0:30]
    charm_users = User.objects.filter(is_block__ne=1).order_by("-charm_value")[0:30]

    CharmRank.drop_collection()
    WealthRank.drop_collection()

    print wealth_users.count()

    for i in range(0, wealth_users.count()):
        wealth_rank = WealthRank(user=wealth_users[i], wealth=wealth_users[i].wealth_value*10, rank=i+1, change_status=0)
        wealth_rank.save()

    for i in range(0, charm_users.count()):
        charm_rank = CharmRank(user=charm_users[i], charm=charm_users[i].charm_value, rank=i+1, change_status=0)
        charm_rank.save()


def compute_total_ranklist_delta():
    wealth_users = User.objects.filter(is_block__ne=1).order_by("-wealth_value")[0:30]
    charm_users = User.objects.filter(is_block__ne=1).order_by("-charm_value")[0:30]

    wealth_ranks = WealthRank.objects.all()
    charm_ranks = CharmRank.objects.all()

    wealth_dict={}
    charm_dict = {}

    for rank in wealth_ranks:
        if rank.user in wealth_users:
            wealth_dict[rank.user.id] = rank
        else:
            rank.delete()
    for i,user in enumerate(wealth_users):
        if user.id in wealth_dict:
            rank = wealth_dict[user.id]
            if rank.rank > i + 1:
                rank.change_status = 1
            elif rank.rank == i + 1:
                rank.change_status = 0
            else:
                rank.change_status = 2
            rank.rank = i + 1
            rank.wealth = rank.user.wealth_value * 10
        else:
            rank = WealthRank()
            rank.user = user
            rank.change_status = 1
            rank.wealth = user.wealth_value * 10
            rank.rank = i + 1
            wealth_dict[rank.user.id] = rank

    for rank in charm_ranks:
        if rank.user in charm_users:
            charm_dict[rank.user.id] = rank
        else:
            rank.delete()
    for i, user in enumerate(charm_users):
        if user.id in charm_dict:
            rank = charm_dict[user.id]
            if rank.rank > i+1:
                rank.change_status = 1
            elif rank.rank == i+1:
                rank.change_status =0
            else:
                rank.change_status =2
            rank.rank = i+1
            rank.charm = rank.user.charm_value
        else:
            rank = CharmRank()
            rank.user = user
            rank.change_status = 1
            rank.charm = user.charm_value
            rank.rank = i+1
            charm_dict[rank.user.id] = rank


    for key in charm_dict:
        charm_dict[key].save()
    for key in wealth_dict:
        wealth_dict[key].save()

if __name__ == '__main__':
    compute_total_ranklist_delta()











