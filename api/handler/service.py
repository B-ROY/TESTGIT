# coding=utf-8

from api.document.doc_tools import *
from api.view.base import *
from app.customer.models.personal_tags import UserTags
from app.customer.models.rank import *
from app.customer.models.share import *
from app.util.messageque.msgsender import MessageSender
from app.customer.models.bottle_message import *
from app.customer.models.tools import *


@handler_define
class RankListCharm(BaseHandler):
    @api_define("day's ranklist", "/service/ranklist",
        [
            Param("type", True, int, 0, 0, "排行榜类型（1，魅力 2， 财富 3， 魅力加财富"),
            Param("interval", False, int, 0,0, "计算周期(0:天，1:周,2：月,3:三天")
        ], description=u"排行榜")
    def get(self):
        list_type = self.arg_int("type", 3)
        interval = self.arg_int("interval", 10)
        if list_type == 3:
            charm_rank_list = CharmRank.get_rank_list(interval=interval, count=30)
            charm_data = []
            for charm_rank in charm_rank_list:
                dic = {}
                dic["user"] = charm_rank.user.get_normal_dic_info()
                dic["charm"] = charm_rank.charm
                dic["change_status"] = charm_rank.change_status
                charm_data.append(dic)
            wealth_rank_list = WealthRank.get_rank_list(interval=interval, count=30)
            wealth_data = []
            for wealth_rank in wealth_rank_list:
                dic = {}
                dic["user"] = wealth_rank.user.get_normal_dic_info()
                dic["wealth"] = wealth_rank.wealth
                dic["change_status"] = wealth_rank.change_status
                wealth_data.append(dic)
            self.write({
                "status": "success",
                "charm_list": charm_data,
                "wealth_list": wealth_data

            })


@handler_define
class BottleMessageSend(BaseHandler):
    @api_define("message_send", "/service/bottle_message",
                [
                    Param("message_content", True, str, "", "this is a message", "消息内容")
                ], description=u"发送漂流瓶")
    @login_required
    def get(self):
        user = self.current_user
        message_content = BottleMessageText.get_one_mesasge_text(0).message
        if user.is_video_auth == 1 and user.disturb_mode == 0:
            status_code = MessageSender.send_bottle_message(user.id, message_content)
            count = UserHeartBeat.get_bottle_users_count()
            if status_code == 200:
                return self.write({"status": "success", "count": count})
            else:
                return self.write({"status": "failed", "error_code": status_code, "error": u"漂流瓶消息发送失败"})
        elif user.is_video_auth != 1:
            self.write({
                "status": "failed",
                "errcode": 30001,
               "error": u"尚未通过视频认证"
            })
        else:
            self.write({
                "status": "failed",
                "errcode": 30002,
                "error": u"勿扰模式下，不能发送漂流瓶"
            })


@handler_define
class TurnDeck(BaseHandler):
    @api_define("turn deck", "/service/turn_deck",
                [], description=u"翻牌子功能")
    def get(self):
        """注释的为按心跳时间取的 现阶段可能取不到改为按照首页取
        # 找到最近1个小时上报心跳的随机三个人
        now_time = int(time.time())
        one_hour_ago = now_time - 3600
        user_heartbeats = UserHeartBeat.objects.filter(last_report_time__lte=now_time, last_report_time__gt=one_hour_ago)
        print "turn deck count is " + str(user_heartbeats.count())
        if user_heartbeats < 3:
            
            pass
        else:
            randoms = random.sample(range(0,user_heartbeats.count()-1), 3)
            data = []
            for num in randoms:
                user_data = {}
                user_data["user"] = user_heartbeats[num].user.get_normal_dic_info()
                user_data["personal_tags"] = UserTags.get_usertags(user_heartbeats[num].id)
                data.append(user_data)
        """

        users = User.objects.filter(is_video_auth=1, gender=2, audio_room_id__ne="", disturb_mode=0).order_by("-current_score")[0:90]
        randoms = random.sample(range(0, users.count() - 1), 3)
        data = []
        for num in randoms:
            user_data = {}
            user_data["user"] = users[num].get_normal_dic_info()
            user_data["personal_tags"] = UserTags.get_usertags(users[num].id)
            data.append(user_data)
        self.write({
            "status": "success",
            "data": data,
        })


@handler_define
class BottleMessageShow(BaseHandler):
    @api_define("bottle message", "/service/bottle/v2_message",
                [], description=u"服务器返回漂流瓶消息v2")
    @login_required
    def get(self):
        count = random.randint(500, 1000)
        message_text = BottleMessageText.get_one_mesasge_text(0)
        return self.write({
            "status": "success",
            "label": message_text.label,
            "message": message_text.message,
            "count": count
        })


@handler_define
class BottleMessageShowV3(BaseHandler):
    @api_define("bottle message", "/service/bottle/message_v3",
                [], description=u"服务器返回漂流瓶消息新版v3")
    @login_required
    def get(self):
        count = random.randint(500, 1000)
        messages = BottleMessageText.get_two_message()
        message_list = []
        if len(messages) > 0:
            for message in messages:
                dic = {
                    "label": message.label,
                    "message": message.message,
                    "gender": message.gender
                }
                message_list.append(dic)

        user_id = int(self.current_user_id)
        tools = Tools.objects.filter(tools_type=1).first()
        tools_count = UserTools.objects.filter(user_id=user_id, tools_id=str(tools.id)).sum("tools_count")

        # 漂流瓶
        tools = Tools.objects.filter(tools_type=1).first()

        data = {
            "message_list": message_list,
            "count": count,
            "tools_count": tools_count,
            "price": tools.price
        }

        return self.write({
            "status": "success",
            "data": data
        })


@handler_define
class BottleMessaegSend_V2(BaseHandler):
    @api_define("bottle message send", "/service/bottle/v2_send",
                [
                    Param("label", True, int, 0, 0, description=u"漂流瓶消息标签"),
                    Param("message", True, str, "", "一轮红日")
                ],description=u"发送漂流瓶消息v2")
    @login_required
    def get(self):
        user = self.current_user
        label = self.arg_int("label")
        #todo 鉴定label 是否和message匹配 将来加上redis的时候做
        message_content = self.arg("message")
        #todo 加上判断
        if user.is_video_auth == 1 and user.disturb_mode == 0:
            status_code = MessageSender.send_bottle_message(user.id, message_content)
            count = UserHeartBeat.get_bottle_users_count()
            if status_code == 200:
                # todo  创建一条 漂流瓶记录
                BottleRecord.create_bottle_record(user.id, label, message_content, 0, count)
                return self.write({"status": "success", "count": count})
            else:
                return self.write({"status": "failed", "error_code": status_code, "error": u"漂流瓶消息发送失败"})
        elif user.is_video_auth != 1:
            self.write({
                "status": "failed",
                "errcode": 30001,
                "error": u"尚未通过视频认证"
            })
        else:
            self.write({
                "status": "failed",
                "errcode": 30002,
                "error": u"勿扰模式下，不能发送漂流瓶"
            })


@handler_define
class BottleMessaegSend_V3(BaseHandler):
    @api_define("bottle message send v3 ", "/service/bottle/v3_send",
                [
                    Param("label", True, int, 0, 0, description=u"漂流瓶消息标签v3"),
                    Param("message", True, str, "", "一轮红日"),
                    Param("gender", True, str, "")
                ],description=u"发送漂流瓶消息v3 新版")
    @login_required
    def get(self):
        user = self.current_user
        label = self.arg_int("label")
        #todo 鉴定label 是否和message匹配 将来加上redis的时候做
        message_content = self.arg("message")
        gender = self.arg_int("gender")

        #todo 加上判断
        if user.disturb_mode == 0:
            status_code = MessageSender.send_bottle_message_v3(user.id, message_content, gender)
            count = UserHeartBeat.get_bottle_users_count()
            if status_code == 200:
                # todo  创建一条 漂流瓶记录
                BottleRecord.create_bottle_record(user.id, label, message_content, 0, count)

                # 消耗道具 或者 消耗余额
                tools = Tools.objects.filter(tools_type=1).first()
                user_tools = UserTools.objects.filter(user_id=user.id, tools_id=str(tools.id)).first()
                if user_tools:
                    # 消耗道具
                    UserTools.reduce_tools(user_id=user.id, tools_id=str(tools.id))
                else:
                    # 消耗余额
                    # 用户账号余额
                    account = Account.objects.filter(user=user).first()
                    # account.last_diamond = account.diamond
                    # account.diamond -= tools.price
                    # account.update_time = datetime.datetime.now()
                    # account.save()
                    account.diamond_trade_out(price=tools.price, desc=u"漂流瓶消耗金额", trade_type=TradeDiamondRecord.TradeTypeBottle)

                return self.write({"status": "success", "count": count})
            else:
                return self.write({"status": "failed", "error_code": status_code, "error": u"漂流瓶消息发送失败"})
        else:
            self.write({
                "status": "failed",
                "errcode": 30002,
                "error": u"勿扰模式下，不能发送漂流瓶"
            })











