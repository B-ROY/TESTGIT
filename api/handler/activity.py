# coding=utf-8


from api.document.doc_tools import *
from api.view.base import *
from app.customer.models.rank import *
from app.customer.models.activity import Activity
from api.convert.convert_user import *
from app.customer.models.vip import *

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
        return self.write({"status": "success","data": data})









