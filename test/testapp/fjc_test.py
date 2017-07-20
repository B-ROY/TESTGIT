# coding=utf-8

import datetime
# from app.customer.models.tools import *
from app.customer.models.first_charge_activity import *
from app.customer.models.account import *
from app.customer.models.user import *


# now = datetime.datetime.now()
# date = now.strftime('%Y年%m月%d日')
# print date

def test():

    order = TradeBalanceOrder.objects.filter(id="58b52d4471bc820dc0188bb6").first()
    user = order.user

    # 首充活动
    act = FirstChargeActivity.objects.filter(temp_activity_type=1).first()
    now = datetime.datetime.now()

    #  判断是否活动有效
    if act:
        end_time = act.end_time
        days = (end_time - now).days
        if days < 0:
            return True

    #  判断是否是后台充值
    if order.fill_in_type == 6:
        return True

    #判断首充
    starttime = now.strftime("%Y-%m-%d 00:00:00")
    endtime = now.strftime('%Y-%m-%d 23:59:59')
    order_count = TradeBalanceOrder.objects.filter(status='1', user=user, buy_time__gte=starttime,
                                                   buy_time__lte=endtime,).count()
    if order_count > 1:
        return True

    money = order.money
    FirstChargeActivity.create_reward(user, money)


# dic1 = {
#     "master_key": "2",
#     "bottle": "2",
#     "clairvoyant": "5"
# }
#
# s = str(dic1)
# print s
# d1 = eval(s)
# print d1.get("bottle")
# print s

# now = datetime.datetime.now()
# end_time = now + datetime.timedelta(days=30)
# print end_time

# TOOLS_TYPE = (
#     (0, u'万能钥匙'),
#     (1, u'漂流瓶'),
#     (2, u'千里眼'),
# )
# print TOOLS_TYPE[2][0]

# now = datetime.datetime.now()
# yesterday = now - datetime.timedelta(days=1)
# yesterday_start = yesterday.strftime("%Y-%m-%d 00:00:00")
# yesterday_end = yesterday.strftime("%Y-%m-%d 23:59:59")
#
# print yesterday_start
# print yesterday_end

# def init_activity():
#     s = "2017-07-03 00:00:00"
#     e = "2017-07-10 23:59:59"
#     s_time = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
#     e_time = datetime.datetime.strptime(e, "%Y-%m-%d %H:%M:%S")
#     activity = ToolsActivity()
#     activity.tools_data = "{u'1': u'1', u'0': u'1'}"
#     activity.name = "test2"
#     activity.create_time = datetime.datetime.now()
#     activity.delete_status = 1
#     activity.start_time = s_time
#     activity.end_time = e_time
#     activity.start_hms = "14:00:00"
#     activity.end_hms = "15:59:59"
#     activity.role = "1,2,3,"  #1: 新主播 2：老主播 3：用户(多个逗号分隔)
#     activity.save()

# now = datetime.datetime.now()
# hour = now.hour
# minute = now.minute
# second = now.second
#
# if hour < 10:
#     hour_str = '0'+str(hour)
# else:
#     hour_str = str(hour)
#
# if minute < 10:
#     minute_str = '0'+str(minute)
# else:
#     minute_str = str(minute)
#
# if second < 10:
#     second_str = '0'+str(second)
# else:
#     second_str = str(second)
#
# print hour_str + ":" + minute_str + ":" + second_str

# from app.customer.models.index_column import *
# def init():
#     column = IndexColumn()
#     column.name = "推荐"
#     column.column_type = 1
#     column.delete_status = 1
#     column.save()
#
#     column2 = IndexColumn()
#     column2.name = "新人驾到"
#     column2.column_type = 2
#     column2.delete_status = 1
#     column2.save()

import time

def time_test():
    date_time = datetime.datetime(2017, 7, 8)
    print get_time(date_time)


def get_time(date_time):
    now = datetime.datetime.now()
    second = time.mktime(now.timetuple()) - time.mktime(date_time.timetuple())

    if second <= 0:
        second = 0

    #  微信格式
    if second == 0:
        interval = "刚刚"
    elif second < 30:
        interval = str(second) + "秒以前"
    elif second >= 30 and second < 60:
        interval = "半分钟前"
    elif second >= 60 and second < 60 * 60:  #  大于1分钟 小于1小时
        minute = int(second / 60)
        interval = str(minute) + "分钟前"
    elif second >= 60 * 60 and second < 60 * 60 * 24:  #  大于1小时 小于24小时
        hour = int((second / 60) / 60)
        interval = str(hour) + "小时前"
    elif second >= 60 * 60 * 24 and second <= 60 * 60 * 24 * 2: #  大于1D 小于2D
        interval = "昨天" + date_time.strftime('%Y-%m-%d %H:%M')
    elif second >= 60 * 60 * 24 * 2 and second <= 60 * 60 * 24 * 7:  #  大于2D小时 小于 7天
        day = int(((second / 60) / 60) / 24)
        interval = str(day) + "天前"
    elif second <= 60 * 60 * 24 * 365 and second >= 60 * 60 * 24 * 7:  #  大于7天小于365天
        interval = date_time.strftime('%Y-%m-%d %H:%M:%S')
    elif second >= 60 * 60 * 24 * 365:  #  大于365天
        interval = date_time.strftime('%Y-%m-%d %H:%M:%S')
    else:
        interval = "0"
    return interval






