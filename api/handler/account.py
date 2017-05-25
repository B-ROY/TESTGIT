#coding=utf-8
from api.document.doc_tools import *
from api.view.base import *
from app.live.models import *
from django.conf import settings
from api.convert.convert_user import *
import time
import tempfile
from app.customer.models.follow import *
from app.customer.models.user import *
from app.customer.models.account import *
from app.customer.models.gift import *

@handler_define
class PayRules(BaseHandler):
    custom_list = ["800001", "800002", "800003", "800023", "800024", "800018", "800019"]
    @api_define("PayRules", r'/live/pay/rules', [
        Param('platform', True, int, "str", "1", u"平台：(1, u'Android'),(2, u'IOS'),(3, u'WP'),(4, u'其他')"),
        Param('tradetype', False, int, "str", "1", u"类型：(0, u'支付宝'),(1, u'微信'),(2, u'苹果'),(3, u'微信JSAPI'),(4, u'银联'),(5, u'其他'),(6, u'后台添加')"),
    ], description=u"购买规则列表[50引力币=100元]")
    @login_required
    def get(self):
        platform = self.arg_int('platform')
        ttype = self.arg_int('tradetype',default=-1)
        ua = self.request.headers.get('User-Agent')
        try:
            uas = ua.split(";")
            if uas[2] == "iPhone" or uas[2] == "iPad":
                channel = "AppStore"
            else:
                channel = uas[5]
        except Exception as e:
            channel = ""

        #Old version
        if ttype == -1:
            if platform == 2:
                rules = TradeBalanceRule.objects.filter(platform=platform, trade_type=2, channel__ne__in=self.custom_list).order_by("-activity_desc", "money")
            if platform == 1:
                if channel in self.custom_list:
                    rules = TradeBalanceRule.objects.filter(platform=platform, trade_type=1,
                                                            channel=channel).order_by("-activity_desc", "money")
                else:
                    rules = TradeBalanceRule.objects.filter(platform=platform,trade_type=1,channel__nin=self.custom_list).order_by("-activity_desc", "money")
        else: #New version
            if channel in self.custom_list:
                rules = TradeBalanceRule.objects.filter(platform=platform, trade_type=ttype,
                                                        channel=channel).order_by("-activity_desc", "money")
            else:
                rules = TradeBalanceRule.objects.filter(platform=platform, trade_type=ttype,
                                                        channel__nin=self.custom_list).order_by("-activity_desc",
                                                                                                   "money")

        if not rules:
            return self.write({'status':"fail","error": u"获取列表失败"})

        results = []
        for rule in rules or []:
            results.append(rule.normal_info())

        self.write({'status': "success", "results":results})
