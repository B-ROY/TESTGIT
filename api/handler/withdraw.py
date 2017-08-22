# coding=utf-8

from api.convert.convert_user import *
from api.document.doc_tools import *
from api.handler.thridpard.sms_code.sms import SMS
from api.handler.thridpard.weixin import WexinAPI
from api.view.base import *
from app.customer.models.account import *
import international

@handler_define
class WithdrawLogin(BaseHandler):
    @api_define("Login", r'/live/withdraw/login', [
        Param('user_key', True, str, "", "123456790", u'code,access_token'),
        Param('openid', True, str, "", "123456790", u'用户唯一标识,[支付宝用户id，微信用户id，微博用户id]'),
        Param("phone", True, str, "", "", u"手机号"),
        Param('sms_code', True, str, "", "", u'短信验证码'),
    ], description=u"H5提现登录接口", protocal="https")
    def get(self):
        access_token = self.arg("user_key")
        openid = self.arg("openid")
        phone = self.arg("phone")
        sms_code = self.arg("sms_code")

        if access_token == "" or openid == "":
            return self.write({"status": "fail", "error": "access_token or openid null!", "message_code": 3, })

        ucpass = SMS()
        result = ucpass.getCacheData(phone)
        ucpass.delSmsCodeCache(phone)

        if result != None:
            createDate = result['createDate']
            user_key = ucpass.get_access_token(phone, openid, createDate)
            if user_key != access_token:
                return self.write({"status": "fail", "error": _(u"非法用户"), "message_code": 3, })
            if sms_code != result['smsCode']:
                return self.write({"status": "fail", "error": _(u"验证码错误，请输入正确的验证码"), "message_code": 2, })
        else:
            return self.write({"status": "fail", "error": _(u"验证码失效"), "message_code": 2, })

        user = User.objects.filter(phone=phone).order_by("created_at").first()

        if not user:
            return self.write({"status": "fail", "error": _(u"未绑定手机号"), "message_code": 4})

        invite_list = UserInviteCode.get_invite_list(invite_id=user.id)

        friend_revenue = 0
        for invite_user in invite_list:
            friend_revenue += invite_user.ticket * 0.1

        month_money = WithdrawRequest.compute_month_has_withdrawed(user.id)
        day_money = WithdrawRequest.compute_day_has_withdrawed(user.id)
        realname_status = RealNameVerify.check_user_verify(user.id)
        ticket_account = TicketAccount.objects.get(user=user)
        user_data = convert_user(user)
        user_data["ticket"] = ticket_account.total_ticket
        data = {
            "user": user_data,
            "total_revenue": ticket_account.total_ticket,
            "my_revenue": ticket_account.call_ticket + ticket_account.gift_ticket,
            "friend_revenue": ticket_account.friend_benifit_ticket + ticket_account.friend_charge_ticket,
            "withdraw_money": int(ticket_account.money - ticket_account.money_withdrawed-ticket_account.money_requesting),
            "month_limit": WithdrawRequest.class_MONTH_MONEY_TAX_LIMIT,
            "day_limit": WithdrawRequest.class_DAY_MONEY_LIMIT,
            "month_has_withdrawed":month_money,
            "day_has_withdrawed":day_money,
            "realname_status": realname_status,
        }
        self.auth_login(user.id)

        return self.write({"status": "success", "data": data, })


# 提现个人主页显示接口
@handler_define
class WithdrawInfo(BaseHandler):
    @api_define("withdraw info", r'/live/user/withdraw/info', [], description=u"提现个人主页显示")
    @login_required
    def get(self):
        user = self.current_user
        """ 原有代码作为参考

        invite_list = UserInviteCode.get_invite_list(invite_id=user.id)

        friend_revenue = 0
        for invite_user in invite_list:
            account = Account.objects.get(user=invite_user)
            friend_revenue += (invite_user.ticket-invite_user.ticket_bonus) * 0.1 + account.charge*0.1

        data = {
            "total_revenue": user.ticket + friend_revenue,
            "my_revenue": user.ticket,
            "friend_revenue": friend_revenue,
            "withdraw_money": (user.ticket + friend_revenue) * 0.6 - WithdrawRequest.get_withdraw_money(user_id=user.id),
        }
        """

        ticket_account = TicketAccount.objects.get(user=user)

        data = {
            "total_revenue": int(ticket_account.total_ticket),
            "my_revenue": int(ticket_account.call_ticket + ticket_account.gift_ticket),
            "friend_revenue": int(ticket_account.friend_benifit_ticket + ticket_account.friend_charge_ticket),
            "withdraw_money": int(ticket_account.money - ticket_account.money_requesting - ticket_account.money_withdrawed)
        }


        return self.write({"status": "success", "data": data})

# 提现记录查询
@handler_define
class WithdrawRecord(BaseHandler):
    @api_define("withdraw record", r'/live/user/withdraw/record', [], description=u"提现记录查询")
    @login_required
    def get(self):
        user = self.current_user
        records = WithdrawRequest.objects.filter(user_id=user.id).order_by("-request_time")

        data = []
        sum = 0
        for record in records:
            dic = record.normal_info()
            if record.status == 2:
                sum += record.request_money
            data.append(dic)

        return self.write({"status": "success", "data": data, "sum": sum, })

# 提现好友查询
@handler_define
class WithdrawFriends(BaseHandler):
    @api_define("withdraw friends", r'/live/user/withdraw/friends', [], description=u"提现好友查询")
    @login_required
    def get(self):
        user = self.current_user
        invite_list = UserInviteCode.get_invite_list(invite_id=user.id)

        data = []

        """ 原有代码 留作参考
        for invite_user in invite_list:
            account = Account.objects.get(user=invite_user)
            dic = {
                "user": convert_user(invite_user),
                "charge": account.charge*0.1,
                "friend_total_revenue": (invite_user.ticket-invite_user.ticket_bonus) * 0.1 + account.charge * 0.1,
                "friend_revenue": (invite_user.ticket - invite_user.ticket_bonus) * 0.1,
            }
            data.append(dic)
        """
        for invite_user in invite_list:
            ticket_account = TicketAccount.objects.get(user=invite_user)
            account = Account.objects.get(user=invite_user)
            dic ={
                "user": convert_user(invite_user),
                "charge": account.charge * 0.1,
                "friend_total_revenue": (ticket_account.call_ticket + ticket_account.gift_ticket) * 0.1 + account.charge * 0.1,
                "friend_revenue": (ticket_account.call_ticket + ticket_account.gift_ticket) * 0.1,
            }
            data.append(dic)

        return self.write({"status": "success", "data": data, })


@handler_define
class H5WithDrawRequest(BaseHandler):
    @api_define("withdraw request", r"/live/withdraw/h5_request", [
        Param("user_id", True, str, "", "", u"用户id"),
        Param("money", True, str, "", "", u"提现金额"),
        Param("code", True, str, "", "", u"code"),
    ], description=u"H5提现申请")
    def get(self):
        try:
        #user = self.current_user
            user_id = self.arg("user_id")
            user = User.objects.get(id=int(user_id))
            ip = self.user_ip
            user_agent = self.request.headers.get('User-Agent')
            money = self.arg_int("money")

            code = self.arg("code")


            """ 原有代码 留作参考
            invite_list = UserInviteCode.get_invite_list(invite_id=user.id)

            friend_revenue = 0
            for invite_user in invite_list:
                friend_revenue += invite_user.ticket * 0.1

            money_available = (user.ticket + friend_revenue) * 0.6 - WithdrawRequest.get_total_withdraw_money(user.id)
            """
            ticket_account = TicketAccount.objects.get(user=user)
            money_available = ticket_account.money - ticket_account.money_withdrawed - ticket_account.money_requesting

            if money > money_available:
                return self.write({"status": "fail", "error": _(u"余额不足"),})
                # 检查实名认证状态
            realname_status = RealNameVerify.check_user_verify(user_id)
            if realname_status != 1:
                return self.write({"status": "fail", "error": _(u"尚未进行实名认证，请返回聊啪客户端进行实名认证")})
            openid = WexinAPI.get_open_id_h5(code=code)

            status = WithdrawRequest.create_withdraw_request(user_id=user_id, request_money=money,
                                                             user_agent=user_agent, openid=openid, ip=ip)
            if not status:
                return self.write({"status": "fail", "error": _(u"创建提现请求失败"), })
            else:
                return self.write({"status": "success", "request_money": money})
        except Exception,e:
            logging.error("h5_request error %s" % str(e))
            return self.write({"status": "fail"})

@handler_define
class WithdrawList(BaseHandler):
    @api_define("withdraw page", r"/live/withdraw/info_list", [
    ],description=u"提现申请页面信息")
    @login_required
    def get(self):
        user = self.current_user
        ticket_account = TicketAccount.objects.get(user=user)
        moneys = WithdrawRequest.get_money_list()
        month_money = WithdrawRequest.compute_month_has_withdrawed(user.id)
        day_money = WithdrawRequest.compute_day_has_withdrawed(user.id)
        realname_status = RealNameVerify.check_user_verify(user.id)
        data = {
            "total_revenue": ticket_account.total_ticket,
            "my_revenue": ticket_account.call_ticket + ticket_account.gift_ticket,
            "friend_revenue": ticket_account.friend_benifit_ticket + ticket_account.friend_charge_ticket,
            "withdraw_money": int(
                ticket_account.money - ticket_account.money_withdrawed - ticket_account.money_requesting),
            "month_limit": WithdrawRequest.class_MONTH_MONEY_TAX_LIMIT,
            "day_limit": WithdrawRequest.class_DAY_MONEY_LIMIT,
            "month_has_withdrawed": month_money,
            "day_has_withdrawed": day_money,
            "realname_status": realname_status,
            "money_list": moneys,
            "tax_rate": WithdrawRequest.class_TAX_RATE
        }

        return self.write({"status":"success", "data": data})

@handler_define
class WithdrawRequestHandler(BaseHandler):
    @api_define("withdraw request", r"/live/withdraw/request", [
        Param("money", True, str, "", "", u"提现金额"),
        Param("openid", True, str, "", "", u"提现openid")
    ], description=u"提现申请")
    @login_required
    def get(self):
        try:
            user_id = self.current_user.id
            user = User.objects.get(id=int(user_id))
            ip = self.user_ip
            user_agent = self.request.headers.get('User-Agent')
            money = self.arg_int("money")
            openid = self.arg("openid")
            if money not in WithdrawRequest.WITHDRAW_MONEY_LIST:
                return self.write({"status":"fail", "error": _(u"金额不支持")})
            #检查实名认证状态
            realname_status = RealNameVerify.check_user_verify(user_id)

            if realname_status != 1:
                return self.write({"status": "fail", "error": _(u"尚未进行实名认证，请返回聊啪客户端进行实名认证")})
            """ 原有代码 留作参考
            invite_list = UserInviteCode.get_invite_list(invite_id=user.id)

            friend_revenue = 0
            for invite_user in invite_list:
                friend_revenue += invite_user.ticket * 0.1

            money_available = (user.ticket + friend_revenue) * 0.6 - WithdrawRequest.get_total_withdraw_money(user.id)
            """
            ticket_account = TicketAccount.objects.get(user=user)
            money_available = ticket_account.money - ticket_account.money_withdrawed - ticket_account.money_requesting

            if money > money_available:
                return self.write({"status": "fail", "error": _(u"余额不足"),})

            status = WithdrawRequest.create_withdraw_request(user_id=user_id, request_money=money,
                                                             user_agent=user_agent, openid=openid, ip=ip)
            if not status:
                return self.write({"status": "fail", "error": _(u"创建提现请求失败"), })
            else:
                return self.write({"status": "success", "request_money": money})
        except Exception,e:
            logging.error("h5_request error %s" % str(e))
            return self.write({"status": "fail", "error": str(e)})