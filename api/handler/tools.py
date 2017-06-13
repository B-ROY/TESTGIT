#coding=utf-8
from api.document.doc_tools import *
from api.view.base import BaseHandler
import time
from api.view.base import *
from app.customer.models.tools import *
from api.convert.convert_user import *


@handler_define
class Buy_Tools(BaseHandler):
    @api_define("buy tools", r'/tools/buy_tools', [
        Param("tools_id", True, str, "", "", u"tools_id"),
    ], description="购买道具")

    # 判断余额,  添加用户道具, 道具记录

    @login_required
    def get(self):
        user_id = int(self.current_user_id)
        user = self.current_user

        tools_id = self.arg("tools_id", "")
        if tools_id == "":
            return self.write({"status": "failed", "error_message": "请选择道具", })

        status, message = UserTools.buy_tools(user_id, tools_id)

        if status == 200:
            return self.write({"status": "success"})
        else:
            return self.write({"status": "failed", "error_message": message})


@handler_define
class My_Tools(BaseHandler):
    @api_define("my tools", r'/tools/my_tools', [], description="我的道具")

    @login_required
    def get(self):
        user_id = int(self.current_user_id)
        user = self.current_user

        tools = Tools.objects.all().order_by("price")
        limit_tools = []
        forver_tools = []
        for tool in tools:
            tools_id = str(tool.id)
            # 限时道具
            limit_count = UserTools.objects.filter(user_id=user_id, tools_id=tools_id, time_type=0).sum("tools_count")

            forver_count = UserTools.objects.filter(user_id=user_id, tools_id=tools_id, time_type=1).sum("tools_count")

            limit_dic = {
                "tool": convert_tools(tool),
                "count": limit_count
            }
            forver_dic = {
                "tool": convert_tools(tool),
                "count": forver_count
            }
            limit_tools.append(limit_dic)
            forver_tools.append(forver_dic)

        self.write({"status": "success", "limit_tools": limit_tools, "tools": forver_tools})



# 是否可领取道具
@handler_define
class Can_Receive(BaseHandler):
    @api_define("can_receive_tools", "/tools/can_receive_tools",
                [], description=u"是否可领取")
    def get(self):
        current_user_id = self.current_user_id

        can_receive = 0  # 0:不可领取   1:可领取

        """
        if today_receive_tools:  # 如果今日有可领取的这个活动, 暂时默认有可领取
            if user_id:
                now = datetime.datetime.now()
            invite_date = now + datetime.timedelta(days=1)
            starttime = invite_date.strftime("%Y-%m-%d 00:00:00")
            endtime = invite_date.strftime('%Y-%m-%d 23:59:59')
            user_tools = UserTools.objects.filter(invalid_time__gte=starttime, invalid_time__lte=endtime, get_type=0).first()
            if not user_tools:
                is_receive = 1
        """

        # 如果有活动:
        # tools_activity = ToolsActivity.objects.filter(delete_status=1).order_by("-create_time").first()
        # if tools_activity:
        if current_user_id:
            user_id = int(current_user_id)
            now = datetime.datetime.now()
            create_time = now
            starttime = create_time.strftime("%Y-%m-%d 00:00:00")
            endtime = create_time.strftime('%Y-%m-%d 23:59:59')
            # print "starttime", starttime
            # print "endtime", endtime
            record = UserToolsRecord.objects.filter(user_id=user_id, time_type=0, create_time__gte=starttime, create_time__lte=endtime, oper_type=4).first()
            if not record:
                # print "user_id......", user_id
                can_receive = 1

        self.write({"status": "success", "can_receive": can_receive})


# 领取道具
@handler_define
class Receive_Tools(BaseHandler):
    @api_define("receive tools", r'/tools/receive_tools', [], description="领取道具")

    @login_required
    def get(self):
        user_id = int(self.current_user_id)
        user = self.current_user
        now = datetime.datetime.now()
        receive_data = {'0': '1', '1': '1', '2': '1'}

        tools_list = []

        create_time = now
        starttime = create_time.strftime("%Y-%m-%d 00:00:00")
        endtime = create_time.strftime('%Y-%m-%d 23:59:59')
        record = UserToolsRecord.objects.filter(user_id=user_id, time_type=0, create_time__gte=starttime, create_time__lte=endtime, oper_type=4).first()
        if record:
            return self.write({"status": "failed", "error_message": "已经领取道具", })

        # tools_activity = ToolsActivity.objects.filter(delete_status=1).order_by("-create_time").first()
        # receive_data = eval(tools_activity.tools_data)


        for key, value in receive_data.items():

            tools = Tools.objects.filter(tools_type=int(key)).first()  # 道具

            user_tools = UserTools()
            user_tools.user_id = user_id
            user_tools.tools_id = str(tools.id)
            user_tools.tools_count = int(value)
            user_tools.time_type = 0
            user_tools.get_type = 0
            invalid_time = now + datetime.timedelta(days=1)
            user_tools.invalid_time = invalid_time
            user_tools.save()

            tools_record = UserToolsRecord()
            tools_record.user_id = user_id
            tools_record.tools_id = str(tools.id)
            tools_record.tools_count = 1
            tools_record.time_type = 0
            tools_record.oper_type = 4
            tools_record.create_time = now
            tools_record.save()

            # 组装数据
            temp_tool = Tools.objects.filter(id=str(tools.id)).first()
            tool_info = convert_tools(temp_tool)
            dic = {
                "tool": tool_info,
                "count": int(value)
            }

            tools_list.append(dic)

        self.write({"status": "success", "tools": tools_list})


@handler_define
class UserClairvoyantCount(BaseHandler):
    @api_define("receive tools", r'/tools/clairvoyant_count', [], description="用户道具个数(千里眼)")

    def get(self):
        current_user_id = self.current_user_id
        tool = Tools.objects.filter(tools_type=2).first()
        if not current_user_id:
            return self.write({"status": "success", "tool": convert_tools(tool), "count": 0})
        else:
            user_id = int(self.current_user_id)
            count = UserTools.objects.filter(user_id=user_id, tools_id=str(tool.id)).sum("tools_count")
            return self.write({"status": "success", "tool": convert_tools(tool), "count": count})


