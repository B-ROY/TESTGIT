#coding=utf-8
from api.document.doc_tools import *
from api.view.base import BaseHandler
import time
from api.view.base import *
import international
from app.customer.models.game import TurnTable
from app.customer.models.account import Account


@handler_define
class TurnTableValue(BaseHandler):
    @api_define("get turntable info ", r'/game/turn_tabl_info', [
    ], description=u"大转盘信息")
    @login_required
    def get(self):
        user_id = int(self.current_user_id)
        user = self.current_user
        info_list = TurnTable.get_list()
        data = {}
        data["info_list"] = []
        for info in info_list:
            dict = TurnTable.normal_info(info)
            data["info_list"].append(dict)

        account = Account.objects.filter(user=user).first()
        gold = 0
        if account.gold:
            gold = account.gold
        data["user_gold"] = gold
        price = 1000

        free_used_count, free_total_count, gold_used_count, gold_total_count, free_upper_limit, can_share = TurnTable.get_user_count(user_id)

        data["price"] = price

        data["free_used_count"] = free_used_count
        data["free_total_count"] = free_total_count
        data["gold_used_count"] = gold_used_count
        data["gold_total_count"] = gold_total_count
        data["free_upper_limit"] = free_upper_limit
        data["can_share"] = can_share

        self.write({"status": "success", "data": data})


@handler_define
class TurnTableValue(BaseHandler):
    @api_define("get reward id", r'/game/luck_draw', [
        Param('type', False, str, "", "", u'类型  1:免费  2:金币')
    ], description="试试手气")
    @login_required
    def get(self):
        price = 1000
        user_id = self.current_user_id
        type = self.arg_int("type", 1)

        is_can, error = TurnTable.check_is_can(type, user_id, price)
        if is_can != 1:
            return self.write({"status": "success", "msg": _(error)})

        user = self.current_user
        reward_id = TurnTable.get_reward_id()
        TurnTable.save_reward(reward_id, user, type)
        return self.write({"status": "success", "reward_id": reward_id})


@handler_define
class TurnTableShare(BaseHandler):
    @api_define("get reward id", r'/game/share_moment', [
        Param('turn_table_id', False, str, "", "", u'id'),
        Param('picture_urls', False, str, "", "", u'id'),
    ], description="抽奖分享")
    @login_required
    def get(self):
        user_id = self.current_user_id
        turn_table_id = self.arg("turn_table_id")
        picture_urls = self.arg("picture_urls")
        TurnTable.share_moment(user_id, turn_table_id, picture_urls)
        self.write({"status": "success"})







