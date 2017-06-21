# -*- coding: utf-8 -*-
import os
import sys

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../..')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../../..')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../../../..')))

from base.settings import load_django_settings

load_django_settings('live_video.base', 'live_video.app')
from redis_model.queue import Worker


import time
import logging
import datetime
from app.customer.models.tools import *
from app.customer.models.vip import *
from app.customer.models.block_user_device import *

def clear_send_tools():
    now = datetime.datetime.now()
    yesterday = now - datetime.timedelta(days=1)

    yesterday_start = yesterday.strftime("%Y-%m-%d 00:00:00")
    yesterday_end = yesterday.strftime("%Y-%m-%d 23:59:59")

    now_start = now.strftime("%Y-%m-%d 00:00:00")
    now_end = now.strftime("%Y-%m-%d 23:59:59")

    # 清空昨天的 限时道具
    old_tools = UserTools.objects.filter(time_type=0, invalid_time__gte=now_start, invalid_time__lte=now_end)
    if old_tools:
        for old in old_tools:
            # 创建 销毁记录, 删除用户道具
            record = UserToolsRecord()
            record.user_id = old.user_id
            record.tools_id = old.tools_id
            record.tools_count = old.tools_count
            record.time_type = 0
            record.oper_type = 1
            record.create_time = now

            old.delete()
    print "old_tools deleted ...."

    # 自动发放 会员的 限时道具, 创建道具记录
    user_vips = UserVip.objects.all()
    if user_vips:
        for user_vip in user_vips:
            # 会员发放限时道具
            vip = Vip.objects.filter(id=user_vip.vip_id).first()
            tool_str = vip.tools_data
            tool_dic = eval(tool_str)
            for key, value in tool_dic.items():
                tools = Tools.objects.filter(tools_type=int(key)).first()  # 道具

                if int(key) == 2:  # 千里眼
                    continue

                # 限时的
                user_tools = UserTools()
                user_tools.user_id = user_vip.user_id
                user_tools.tools_id = str(tools.id)
                user_tools.tools_count = int(value)
                user_tools.time_type = 0  # 限时
                user_tools.get_type = 1  # 会员自动发放
                invalid_time = now + datetime.timedelta(days=1)
                user_tools.invalid_time = invalid_time
                user_tools.save()

                # 道具记录
                tools_record = UserToolsRecord()
                tools_record.user_id = user_vip.user_id
                tools_record.tools_id = str(tools.id)
                tools_record.tools_count = int(value)
                tools_record.time_type = 0
                tools_record.oper_type = 3
                tools_record.create_time = now
                tools_record.save()
    print "tools send success..."

    # 删除会员到期的
    UserVip.objects.filter(end_time__lte=yesterday_end).delete()


def add_block_record():
    BlockUserRecord.write_record_daily()

if __name__ == "__main__":
    clear_send_tools()
    add_block_record()