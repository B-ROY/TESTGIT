# -*- coding: utf-8 -*-
import os
import sys

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../push_util')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../..')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../../..')))

from base.settings import load_django_settings

load_django_settings('live_video.base', 'live_video.app')

from app.util.messageque.msgsender import MessageSender

from app.customer.models.account import TradeBalanceOrder
import datetime
import random

def push_fake_charge_message(num):

    now_time = datetime.datetime.now()

    twelve_hours_ago = now_time - datetime.timedelta(hours=12)

    balance_orders = TradeBalanceOrder.objects.filter(status=1, filled_time__lte=now_time, filled_time__gte=twelve_hours_ago)

    count = balance_orders.count()

    if num > count:
        num = count
    print count
    indexes = random.sample(range(0, count), num)

    for i in indexes:
        order = balance_orders[i]

        MessageSender.send_charge_info_message(order.user.sid, order.user.nickname, order.money)


if __name__ == '__main__':
    num = random.randint(1, 4)
    push_fake_charge_message(num)
