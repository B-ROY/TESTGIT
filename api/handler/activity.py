# coding=utf-8


from api.document.doc_tools import *
from api.view.base import *
from app.customer.models.rank import *
from app.customer.models.activity import Activity
from api.convert.convert_user import *


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
        if activity:
            data = {
                "activity": convert_activity(activity)
            }
            return self.write({"status": "success","data": data})
        else:
            return self.write({"status": "success"})



