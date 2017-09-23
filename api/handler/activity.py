# coding=utf-8


from api.document.doc_tools import *
from api.view.base import *
from app.customer.models.rank import *
from app.customer.models.activity import Activity
from api.convert.convert_user import *
from app.customer.models.vip import UserVip, Vip, VipReceiveRecord
from app.customer.models.tools import ToolsActivityRecord, ToolsActivity, UserTools, Tools, UserToolsRecord
import datetime

@handler_define
class InviteRankList(BaseHandler):
    @api_define("invite ranklist", "/activity/invite_ranklist",
                [], description=u"排行榜")
    def get(self):
        invite_ranklist = InviteRankTwo.get_top_5()
        data = []
        for invite_rank in invite_ranklist:
            rank = {}
            rank["head_image"] = invite_rank.head_image
            rank["nick_name"] = invite_rank.nickname
            rank["uid"] = invite_rank.uid
            rank["invite_count"] = invite_rank.invite_num
            rank["rank"] = invite_rank.rank
            data.append(rank)

        self.write({"status": "success",
                   "data": data})

@handler_define
class InviteRankList1(BaseHandler):
    @api_define("invite ranklist1", "/activity/invite_ranklist1",
                [], description=u"排行榜")
    def get(self):
        invite_ranklist = InviteRank.get_top_5()
        data = []
        for invite_rank in invite_ranklist:
            rank = {}
            rank["head_image"] = invite_rank.head_image
            rank["nick_name"] = invite_rank.nickname
            rank["uid"] = invite_rank.uid
            rank["invite_count"] = invite_rank.invite_num
            rank["rank"] = invite_rank.rank
            data.append(rank)

        self.write({"status": "success",
                   "data": data})

# 活动页
@handler_define
class GetActivity(BaseHandler):
    @api_define("get activity", "/activity/get_activity",
                [], description=u"活动图")
    def get(self):
        activity = Activity.objects.filter(status_type=1).order_by("-create_time").first()
        data = {}
        if activity:
            data["activity"] = convert_activity(activity)
        user_id = self.current_user_id
        now = datetime.datetime.now()
        is_dialog = 0
        starttime = now.strftime("%Y-%m-%d 00:00:00")
        endtime = now.strftime('%Y-%m-%d 23:59:59')
        tools_list = []

        if user_id:
            user_vip = UserVip.objects.filter(user_id=int(user_id)).first()
            if user_vip:
                record = VipReceiveRecord.objects.filter(user_id=int(user_id), create_time__gte=starttime,
                                                         create_time__lte=endtime).first()
                if not record:
                    is_dialog = 1
                    vip = Vip.objects.filter(id=user_vip.vip_id).first()
                    tool_str = vip.tools_data
                    tool_dic = eval(tool_str)
                    for key, value in tool_dic.items():
                        tools = Tools.objects.filter(tools_type=int(key)).first()  # 道具
                        # 组装数据
                        temp_tool = Tools.objects.filter(id=str(tools.id)).first()
                        tool_info = convert_tools(temp_tool)
                        dic = {
                            "tool": tool_info,
                            "count": int(value)
                        }
                        tools_list.append(dic)

        data["is_dialog"] = is_dialog
        data["tools_list"] = tools_list
        data["high_vip_video_count"] = 2
        data["super_vip_video_count"] = 6
        if is_dialog:
            send_vip_tools(user_vip, user_id)
        return self.write({"status": "success", "data": data})

def send_vip_tools(user_vip, user_id):
    now = datetime.datetime.now()
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






