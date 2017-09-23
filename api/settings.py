#coding=utf-8
import os

def load_settings(settings, debug=True, **kwargs):
    pass
def check_settings(settings):
    pass

# before   0f85eb25881ddd5c31f715542ae856c3

cookie_secret = 'a3643412085026643529f7fe032646c8'

def load_tonardo_settings(tonardo_settings={}):
    tonardo_settings.update({
            'cookie_secret': cookie_secret,
    })


class ConstantKey:

    Tools_Entrance_Card = 0  # 门禁卡
    Tools_Bottle = 1  # 漂流瓶
    Tools_Clairvoyant = 2  # 千里眼
    Tools_Watch_Card = 3  # 观影券
    Tools_Watch_Card_Part = 4  # 观影碎片
    Tools_Day_VIP = 5  # 一天VIP
    Tools_Need_Watch_Part_Count = 6  # 一次观看所需碎片个数

    TurnTable_Free_Count = 3  # 大转盘免费抽奖次数
    TurnTable_Share_Count = 3  # 分享免费抽奖次数
    TurnTable_User_Count = 3  # 普通用户分享次数
    TurnTable_VIP_Count = 6  # 高级vip分享次数
    TurnTable_Super_VIP_Count = 9  # 超级vip分享次数
    TurnTable_Gold_Count = 3  # 金币分享次数

