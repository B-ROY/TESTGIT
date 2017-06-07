# coding=utf-8

from app.customer.models.tools import *
from app.customer.models.vip import *

class ClearAndSendTools():

    @classmethod
    def clear_send_tools(cls):
        now = datetime.datetime.now()
        yesterday = now - datetime.timedelta(days=1)

        yesterday_start = yesterday.strftime("%Y-%m-%d 00:00:00")
        yesterday_end = yesterday.strftime("%Y-%m-%d 23:59:59")

        now_start = now.strftime("%Y-%m-%d 00:00:00")
        now_end = now.strftime("%Y-%m-%d 23:59:59")

        # # 清空昨天的 限时道具
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

        # 自动发放 会员的 限时道具, 创建道具记录
        user_vips = UserVip.objects.all()
        if user_vips:
            for user_vip in user_vips:
                # 会员发放限时道具
                vip = Vip.objects.filter(id=user_vip.vip_id).first()
                tool_str = vip.tools_data
                tool_dic = eval(tool_str)
                for key, value in tool_dic.items():
                    tools = Tools.objects.filter(id=key).first()  # 道具

                    if key == "592912402040e443ffe9a0c0":  # 千里眼
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

        # 删除会员到期的
        UserVip.objects.filter(end_time__lte=yesterday_end).delete()
