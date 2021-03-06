#coding=utf-8
from api.document.doc_tools import *
from api.view.base import BaseHandler
import time
from api.view.base import *
from app.customer.models.tools import *
from api.convert.convert_user import *
from app.customer.models.activity import *
from app.customer.models.user import VideoManagerVerify
from app.customer.models.vip import Vip, UserVip, VipReceiveRecord
import international


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
            return self.write({"status": "failed", "error_message": _(u"请选择道具") })

        status, message = UserTools.buy_tools(user_id, tools_id)

        if status == 200:
            return self.write({"status": "success"})
        else:
            return self.write({"status": "failed", "error_message": _(message)})


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

        # 此处判断 是否有平台活动
        activity = Activity.objects.filter(status_type=1, join_in_tool_activity=2).first()
        if activity:
            return self.write({"status": "success", "limit_tools": limit_tools, "tools": forver_tools,
                               "activity_url": activity.activity_url})
        else:
            self.write({"status": "success", "limit_tools": limit_tools, "tools": forver_tools})



# 是否可领取道具
@handler_define
class Can_Receive(BaseHandler):
    @api_define("can_receive_tools", "/tools/can_receive_tools",
                [], description=u"是否可领取")
    def get(self):
        user_id = self.current_user_id
        can_receive = 0  # 0:不可领取   1:可领取

        if not user_id:
            return self.write({"status": "success", "can_receive": can_receive})

        user = self.current_user
        now = datetime.datetime.now()

        # 注册24小时以内不可以领取
        days = (now - user.created_at).days
        if days < 1:
            return self.write({"status": "success", "can_receive": can_receive})

        if user.is_video_auth == 1:
            verify = VideoManagerVerify.objects.filter(user_id=user_id).first()
            if not verify:
                return self.write({"status": "failed" })
            verify_time = verify.verify_time
            temp_end_time = verify_time + datetime.timedelta(days=7)
            endtime = temp_end_time.strftime('%Y-%m-%d 23:59:59')

            # 6-22 之前认证的都属于老主播
            compare_time = datetime.datetime(2017, 6, 21)

            if verify_time < compare_time or datetime.datetime.strptime(endtime, "%Y-%m-%d %H:%M:%S") < now:
                # 老主播
                can_receive = get_receive_result(2, now, user.id)

            else:
                # 新主播
                can_receive = get_receive_result(1, now, user.id)

        else:
            can_receive = get_receive_result(3, now, user.id)

        self.write({"status": "success", "can_receive": can_receive})


def get_receive_result(role, date_time, user_id):
    now_str = date_time.strftime('%Y-%m-%d 23:59:59')
    now = datetime.datetime(date_time.year, date_time.month, date_time.day)
    hm = get_hm(date_time)

    activity = ToolsActivity.objects.filter(delete_status=1, role__contains=str(role), end_time__gte=now_str,
                                            start_hms__lte=hm, end_hms__gte=hm).first()
    if not activity:
        return 0

    # 如果存在活动,判断此人是否领取此活动
    activity_id = str(activity.id)
    record = ToolsActivityRecord.objects.filter(date_time=now, user_id=user_id, tools_activity_id=activity_id).first()
    if record:
        return 0
    else:
        return 1


def get_hm(now):
    hour = now.hour
    minute = now.minute

    if hour < 10:
        hour_str = '0'+str(hour)
    else:
        hour_str = str(hour)

    if minute < 10:
        minute_str = '0'+str(minute)
    else:
        minute_str = str(minute)


    return hour_str + ":" + minute_str


# 领取道具
@handler_define
class Receive_Tools(BaseHandler):
    @api_define("receive tools", r'/tools/receive_tools', [
        Param("type", False, str, "", "", u" 1:首页活动领取按钮  2:vip每日赠送"),
    ], description="领取道具")

    @login_required
    def get(self):
        flag = False
        if not flag:
            return self.write({"status": "success", "tools": []})
        user_id = int(self.current_user_id)
        user = self.current_user
        now = datetime.datetime.now()
        now_str = now.strftime('%Y-%m-%d 23:59:59')
        hm = get_hm(now)
        activity_id = ""
        type = self.arg_int("type", "1")
        receive_data = {}

        if user.is_video_auth == 1:
            #  主播
            verify = VideoManagerVerify.objects.filter(user_id=user_id).first()
            if not verify:
                return self.write({"status": "failed", "error_message": "认证主播", })
            verify_time = verify.verify_time
            temp_end_time = verify_time + datetime.timedelta(days=7)
            endtime = temp_end_time.strftime('%Y-%m-%d 23:59:59')

            # 6-22 之前认证的都属于老主播
            compare_time = datetime.datetime(2017, 6, 21)

            if verify_time < compare_time or datetime.datetime.strptime(endtime, "%Y-%m-%d %H:%M:%S") < now:
                # 老主播
                status, activity = check_receive(2, now, user_id)
                if status == 3:
                    receive_data = eval(activity.tools_data)
                    activity_id = str(activity.id)
            else:
                # 新主播
                status, activity = check_receive(1, now, user_id)
                if status == 3:
                    receive_data = eval(activity.tools_data)
                    activity_id = str(activity.id)
        else:
            #  非主播
            status, activity = check_receive(3, now, user_id)
            if status == 3:
                receive_data = eval(activity.tools_data)
                activity_id = str(activity.id)

        # ====================================================================================

        tools_list = []

        create_time = now
        if receive_data:
            for key, value in receive_data.items():
                tools = Tools.objects.filter(tools_type=int(key)).first()  # 道具
                user_tools = UserTools()
                user_tools.user_id = user_id
                user_tools.tools_id = str(tools.id)
                user_tools.tools_count = int(value)
                user_tools.time_type = 0
                user_tools.get_type = 4
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

            activity_record = ToolsActivityRecord()
            activity_record.user_id = user_id
            activity_record.date_time = datetime.datetime(now.year, now.month, now.day)
            activity_record.tools_activity_id = activity_id
            activity_record.save()


        # vip每日赠送领取
        user_vip = UserVip.objects.filter(user_id=user_id).first()
        if user_vip:
            vip = Vip.objects.filter(id=user_vip.vip_id).first()
            tool_str = vip.tools_data
            tool_dic = eval(tool_str)
            for key, value in tool_dic.items():
                tools = Tools.objects.filter(tools_type=int(key)).first()  # 道具
                user_tools = UserTools()
                user_tools.user_id = user_vip.user_id
                user_tools.tools_id = str(tools.id)
                user_tools.tools_count = int(value)
                user_tools.time_type = 0  # 限时
                user_tools.get_type = 1  # 会员自动发放
                invalid_time = now + datetime.timedelta(days=1)
                user_tools.invalid_time = invalid_time
                user_tools.save()

                tools_record = UserToolsRecord()
                tools_record.user_id = user_vip.user_id
                tools_record.tools_id = str(tools.id)
                tools_record.tools_count = int(value)
                tools_record.time_type = 0
                tools_record.oper_type = 3
                tools_record.create_time = now
                tools_record.save()
            receive_record = VipReceiveRecord()
            receive_record.user_id = user_id
            receive_record.vip_id = user_vip.vip_id
            receive_record.create_time = datetime.datetime.now()
            receive_record.save()

        return self.write({"status": "success", "tools": tools_list})


def check_receive(role, date_time, user_id):
    hm = get_hm(date_time)
    now_str = date_time.strftime('%Y-%m-%d 23:59:59')

    activity = ToolsActivity.objects.filter(delete_status=1, role__contains=str(role), end_time__gte=now_str,
                                            start_hms__lte=hm, end_hms__gte=hm).first()
    if not activity:
        return 1, None  # 活动过期
    else:
        date_now = datetime.datetime(date_time.year, date_time.month, date_time.day)
        activity_id = str(activity.id)
        record = ToolsActivityRecord.objects.filter(date_time=date_now, user_id=user_id, tools_activity_id=activity_id).first()
        if record:
            return 2, None  # 已经领取
        return 3, activity


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


