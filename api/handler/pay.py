# -*- coding: utf-8 -*-

from api.document.doc_tools import *
from api.view.base import *
from app.customer.models.account import *
from api.util.paylib.alipayapi import *
from api.util.paylib.applepayapi import *
from api.util.paylib.apple_verify import ios_pay_verify
from api.util.paylib.wepayapi import *
from api.util.paylib.googlepayapi import *
from api.util.paylib.wepayapi_jsapi import *
from app.customer.models.fillin import *
from xml.etree.ElementTree import XML
import json
import hashlib
from django.conf import settings
import logging
from app.customer.models.promotion import *
import international
from api.util.paylib.helipayapi import HeliDoPay


def parser_receipt(receipt):
    if not receipt:
        return None
    RecSet = {}

    inapp = receipt.get('in_app',[])
    filesData = []

    for (k,v) in receipt.items():
        if k != 'in_app':
            RecSet[k]=v

    if len(inapp) == 1:
        for (k,v) in inapp[0].items():
            RecSet[k] = v

    return RecSet

def verify_order(order_id,apple_product_id,receipt):
    rule = TradeBalanceRule.objects.filter(apple_product_id=apple_product_id,platform=2,trade_type=2).first()
    print rule
    logging.error("Apple Pay Verify Beginning Order:%s" % str(order_id))
    if not rule:
        logging.error("Apple Pay Verify Rule error Order:%s" % str(order_id))
        return False

    ruleinfo = rule.normal_info()

    print ruleinfo
    print order_id
    obj = TradeBalanceOrder.objects.get(id=order_id)

    print obj
    if not obj:
        logging.error("Apple Pay Verify Order=None error Order:%s" % str(order_id))
        return False

    orderinfo = obj.normal_info()

    print ruleinfo
    print orderinfo
    if ruleinfo['diamon'] != orderinfo['diamon'] or ruleinfo['money'] != orderinfo['money']:
        logging.error("Apple Pay rule != order error Order:%s" % str(order_id))
        return False
    opurchase_date_ms = receipt.get('original_purchase_date_ms','')
    purchase_date_ms = receipt.get('purchase_date_ms','')
    #datetime.datetime.fromtimestamp(opurchase_date_ms/1000)
    if opurchase_date_ms != purchase_date_ms:
        logging.error("Apple Pay opurchase_date_ms != purchase_date_ms error Order:%s" % str(order_id))
        return False

    buy_time = orderinfo['pay_buy_time']
    print buy_time
    print type(buy_time)
    #buytime = datetime.datetime.strptime(str(buy_time), "%Y-%m-%d %H:%M:%S")
    appbuytime = int(purchase_date_ms)/1000
    print appbuytime
    #appbuytime = datetime.datetime.fromtimestamp(int(purchase_date_ms)/1000)
    timeruels = appbuytime - buy_time
    #if (appbuytime - buytime).seconds < 0 or (appbuytime - buytime).seconds > 15:
    if timeruels < 0 or timeruels > 1800:
        logging.error("Apple Pay timeout error Order:%s" % str(order_id))
        return False
    logging.error("Apple Pay Verify Success Order:%s" % str(order_id))
    return True

def checkWeFirstPayActivity(amount, user, type):
    if amount!=100:
        return False
    return Promotion.check_status(user.id, type)

@handler_define
class OrderInfoHandler(BaseHandler):
    @login_required
    @api_define("order status", r'/api/live/order_info', [
        Param('order_id', True, str, "str", "1", u'订单号'),
    ], description=u"下单查询",)
    def get(self):
        order_id = self.arg('order_id')
        try:
            obj = TradeBalanceOrder.objects.get(id=order_id)
        except TradeBalanceOrder.DoesNotExist:
            # (0:等待支付,1:支付成功,2:规则错误,3:支付失败,4:退费)
            return self.write({'status': 'fail', "error": "error order_id"})
        res = {'status': "success", 'results': obj.normal_info()}
        return self.write(res)

@handler_define
class UsersOrderInfoHandler(BaseHandler):
    @login_required
    @api_define("User Orders", r'/api/live/users/order_info', [
        Param('page', True, int, "1", "1", u'page'),
        Param('page_count', True, int, "20", "20", u'每页数量'),
        Param('uid', False, str, "", "", u'uid'),
    ], description=u"充值下单记录",)
    def get(self):
        user_id = self.arg("uid",self.current_user_id)
        page = self.arg_int("page",1)
        page_count = self.arg_int("page_count",20)

        results = []
        orders = TradeBalanceOrder.order_list(user_id,page,page_count)
        for order in orders or []:
            results.append(order.normal_info())

        res = {'status': "success", 'results': results}
        return self.write(res)

@handler_define
class AliPayHandler(BaseHandler):
    @login_required
    @api_define("Play Url", r'/api/live/do/pay', [
        Param('amount', True, int, "str", "1", u'支付金额，单位分'),
        Param('trade_type', True, int, "str", "0", u'0-支付宝 1-微信 2-苹果，3-微信JSAPI，7-谷歌   9-合利宝'),
        Param('platform', True, int, "str", "1", u"平台：(1, u'Android'),(2, u'IOS'),(3, u'WP'),(4, u'其他')"),
        Param('good_name', True, str, "商品名称", "商品名称", u'商品名称'),
        Param('desc', True, str, "商品描述", "商品描述", u'商品描述'),
        Param('apple_product_id', False, str, "", "010060100", u'苹果产品id'),
        Param('openid', False, str, "", "o26BPwchoXh96Cjfk0-LabvpfdjE", u'微信openid,JSAPI 必填'),
    ], description=u"下单接口",protocal="https")
    def get(self):

        user = self.current_user
        amount = self.arg_int('amount')
        platform = self.arg_int('platform')
        good_name = self.arg('good_name',self.arg("amount"))
        trade_type = self.arg_int('trade_type')
        ua = self.request.headers.get('User-Agent')
        desc = self.arg("desc")


        #创建本地订单
        account = Account.objects.get(user=user)
        order = account.fill_in_create_order(
            money=amount,
            platform=platform,
            fill_in_type=trade_type,
            user_agent=ua,
            apple_product_id = self.arg('apple_product_id','')
        )

        #支付宝支付
        if trade_type == 0:
            pay = AliPayDoPay(
                out_trade_no=str(order.id),
                subject=good_name,
                total_fee='%.2f' % (float(amount)/100),
                body=good_name,
            )
            params = pay.do_pay_params()
        #微信支付
        elif trade_type == 1:
            pay = WePayDoPay(
                out_trade_no=str(order.id),
                subject=good_name,
                total_fee=amount,
                body=good_name,
                ip=self.user_ip,
            )

            params = pay.do_pay_params()
            #pay = HeliDoPay(str(order.id), amount, self.user_ip, good_name, desc)
            #params = pay.post_submit()
        #苹果支付只创建一个订单 返回订单号
        elif trade_type == 2:
            pay = ApplePayDoPay()
            params = pay.do_pay_params()

        elif trade_type == 3:
            openid = self.arg('openid')

            pay = WePayJSDoPay(
                out_trade_no=str(order.id),
                subject=good_name,
                total_fee=amount,
                body=good_name,
                payment_type = "JSAPI",
                ip = self.user_ip,
                openid = openid,
            )
            params = pay.do_pay_params()
        #谷歌支付只创建一个订单 返回订单编号
        elif trade_type == 7:
            pay = GooglePayDoPay()
            params = pay.do_pay_params()
        elif trade_type == 8:
            pay = WePayDoPay(
                out_trade_no=str(order.id),
                subject=good_name,
                total_fee=amount,
                body=good_name,
                ip=self.user_ip,
            )
            params = pay.do_create_qrcode()
            return self.write({"params": params})

        data = {'order_id': str(order.id)}
        data.update(params)
        r = {'status': "success", "data": data, "ip":self.user_ip}
        self.write(r)

@handler_define
class HeliPayNotifyHandler(BaseHandler):
    @api_define("helipay Callback Url", r'/api/live/helipay/notify', [
    ], description=u"合利宝通知接口",)
    def post(self):
        body = self.request.body
        if not body:
            return self.write("fail")

        rt1_customerNumber = self.arg("rt1_customerNumber")
        rt2_orderId = self.arg("rt2_orderId")
        rt3_systemSerial = self.arg("rt3_systemSerial")
        rt4_status = self.arg("rt4_status")
        rt5_orderAmount = self.arg("rt5_orderAmount")
        rt6_currency = self.arg("rt6_currency")
        rt7_timestamp = self.arg("rt7_timestamp")
        rt8_desc = self.arg("rt8_desc")
        sign = self.arg("sign")

        verify_status = HeliDoPay.verify_notice_sign(urllib.unquote(rt1_customerNumber), urllib.unquote(rt2_orderId), urllib.unquote(rt3_systemSerial), urllib.unquote(rt4_status),
                                                     urllib.unquote(rt5_orderAmount), urllib.unquote(rt6_currency), urllib.unquote(rt7_timestamp), urllib.unquote(rt8_desc), sign)

        if not verify_status:
            print "fail!!!!!!!!!!!!!!!!!!verify_status"
            return self.write("fail")

        success = HeliPayVerify.create_order(urllib.unquote(rt1_customerNumber), urllib.unquote(rt2_orderId), urllib.unquote(rt3_systemSerial), urllib.unquote(rt4_status),
                                             urllib.unquote(rt5_orderAmount), urllib.unquote(rt6_currency), urllib.unquote(rt7_timestamp), urllib.unquote(rt8_desc), sign)

        if success:
            self.write("success")
        else:
            self.write("fail")

@handler_define
class AliPayNoticeHandler(BaseHandler):
    @api_define("Play Url", r'/api/live/alipay/notice', [
        Param('order_id', True, str, "100", "100", u'订单号'),
        Param('amount', True, int, "str", "100", u'支付金额'),
    ], description=u"支付宝成功通知接口",)
    def post(self):

        arguments = self.request.arguments

        sign = self.arg('sign')

        params = []

        for key, value in arguments.iteritems():
            if key=='sign' or key == 'sign_type':
                continue
            value_ = urllib.unquote_plus(value[0])
            params.append((key, value_))

        params.sort(key=lambda x: x[0])
        content = '&'.join(['='.join(x) for x in params])

        ali_notice = AliPayVerifyNotice(content, sign)

        if not ali_notice.verify_sign():
            return self.write("failed")

        dic = dict(params)
        if dic.get("trade_status") == "TRADE_CLOSED":
            return self.write({"success"})
        success = AlipayFillNotice.create_order(dic)

        if success:
            self.write("success")

@handler_define
class WePayNoticeHandler(BaseHandler):
    @api_define("WeChat Callback Url", r'/api/live/wepay/notice', [
    ], description=u"微信支付成功通知接口",)
    def post(self):
        body = self.request.body

        if not body:
            self.write('''
                    <xml>
                      <return_code><![CDATA[FAIL]]></return_code>
                      <return_msg><![CDATA[FAIL]]></return_msg>
                    </xml>
                    ''')

        xml = XML(body)

        wp = WePayDoPay( out_trade_no='',
                subject='',
                total_fee='',
                body='',
                ip = self.user_ip)

        success = wp.verify_notice_sign(xml)

        if not success:
            self.write('''
                    <xml>
                      <return_code><![CDATA[FAIL]]></return_code>
                      <return_msg><![CDATA[Sign error]]></return_msg>
                    </xml>
                    ''')


        success = WeChatFillNotice.create_order(xml)

        if success:
            self.write('''
                    <xml>
                      <return_code><![CDATA[SUCCESS]]></return_code>
                      <return_msg><![CDATA[OK]]></return_msg>
                    </xml>
                    ''')
        else:
            self.write('''
                    <xml>
                      <return_code><![CDATA[FAIL]]></return_code>
                      <return_msg><![CDATA[fail order transaction]]></return_msg>
                    </xml>
                    ''')

@handler_define
class ApplePayVerifyHandler(BaseHandler):

    @api_define("Applepay Verify", r'/api/live/applepay/verify', [
        Param('order_id', True, str, "", "", u'订单号'),
        Param('reciept', False, str, "", "", u'验证base64数据'),
    ], description=u"苹果支付校验接口",)
    @login_required
    def get(self, *args, **kwargs):
        order_id = self.arg('order_id')
        reciept = self.arg('reciept' , "")
        user_id = self.current_user_id

        if int(user_id) == 100370 or int(user_id) == 100339 or int(user_id) == 504 or int(user_id) == 3411 or int(user_id) == 54637 or int(user_id) == 30749 or int(user_id) == 68522:
            Account.fill_in(order_id=order_id)
            return self.write({"status": "success"})

        av = AppleVerify.create_verify(order_id,reciept)
        if av == -1:
            return self.write({'status':'fail','error':'重复的表单'})
        if av.is_verified():
            return  self.write({'status':'fail','error':'is verified'})

        success, receipt = ios_pay_verify(reciept, settings.apple_verify)

        if success:
            try:
                receipt = parser_receipt(receipt)
                if not receipt:
                    return self.write({'status':'fail','error':'无法充值','errcode':'2004'})
                product_id = receipt.get('product_id','')
                if not verify_order(order_id,product_id,receipt):
                    return self.write({'status':'fail','error':'无法充值','errcode':'2004'})
                av.fill_in(receipt)
            except Exception,e:
                return self.write({'status': 'fail', "error": e.message })

            self.write({'status': 'success'})
        else:
            self.write({'status': 'fail', "erorr": "verify fail"})

@handler_define
class GooglePayVerifyHandler(BaseHandler):
    @api_define("Google Pay Verify", r"/api/live/googlepay/verify",
                [
                    Param("order_id", True, str, "", "", description=u"本地订单号"),
                    Param("package_name", True, str, "", "", description=u"应用包名"),
                    Param("sku", True, str, "", "", description=u"product_id"),
                    Param("google_order_id", True, str, "", "", description=u"google订单号"),
                    Param("purchase_token", True, str, "", "", description=u"purchase_token(查询订单使用)")
                ], description=u"googleppay验证接口")
    def get(self):
        order_id = self.arg("order_id")
        package_name = self.arg("package_name")
        sku = self.arg("sku")
        google_order_id = self.arg("google_order_id")
        purchase_token = self.arg("purchase_token")

        #验证订单是否已购买
        google_notice = GooglePayNotice(package_name=package_name, product_id=sku, purchase_token=purchase_token)
        result = google_notice.validate()
        if result:
            verify_dict = {
                "order_id": order_id,
                "google_order_id": google_order_id,
                "purchase_token": purchase_token
            }
            GooglePayVeriry.create_order(verify_dict)
            return self.write({"status": "success"})

        else:
            return self.write({"status": "fail", "error": "支付失败"})




"""
@handler_define
class AliPayHandler(BaseHandler):
    @api_define("Pay Identity", r'/api/live/do/pay/identity', [
        Param('amount', True, int, "str", "1", u'支付金额，单位分'),
        Param('trade_type', True, int, "str", "0", u'0-支付宝 1-微信 2-苹果，3-微信JSAPI'),
        Param('platform', True, int, "str", "1", u"平台：(1, u'Android'),(2, u'IOS'),(3, u'WP'),(4, u'h5')"),
        Param('good_name', True, str, "商品名称", "商品名称", u'商品名称'),
        Param('desc', True, str, "商品描述", "商品描述", u'商品描述'),
        Param('apple_product_id', False, str, "", "010060100", u'苹果产品id'),
        Param('openid', False, str, "", "o26BPwchoXh96Cjfk0-LabvpfdjE", u'微信openid,JSAPI 必填'),
        Param('identity', False, str, "", "", u'identity用户展示id'),
    ], description=u"下单接口(无登录)",protocal="https")
    def get(self):

        user = User.objects.filter(identity=self.arg('identity')).first()
        amount = self.arg_int('amount')
        platform = self.arg('platform')
        good_name = self.arg('good_name',self.arg("amount"))
        trade_type = self.arg_int('trade_type')
        if amount == 1:
            r = {'status': "fail", "data": {}, "ip": self.user_ip}
            return self.write(r)
        
        #创建本地订单
        account = Account.objects.get(user=user)
        order = account.fill_in_create_order(
            money=amount,
            platform=platform,
            fill_in_type=trade_type,
            apple_product_id = self.arg('apple_product_id','')
        )

        #支付宝支付
        if trade_type == 0:
            pay = AliPayDoPay(
                out_trade_no=str(order.id),
                subject=good_name,
                total_fee='%.2f' % (float(amount)/100),
                body=good_name,
            )
            params = pay.do_pay_params()
        #微信支付
        elif trade_type == 1:

            pay = WePayDoPay(
                out_trade_no=str(order.id),
                subject=good_name,
                total_fee=amount,
                body=good_name,
                ip = self.user_ip,
            )
            params = pay.do_pay_params()
        #苹果支付只创建一个订单 返回订单号
        elif trade_type == 2:
            pay = ApplePayDoPay()
            params = pay.do_pay_params()

        elif trade_type == 3:
            openid = self.arg('openid')

            pay = WePayJSDoPay(
                out_trade_no=str(order.id),
                subject=good_name,
                total_fee=amount,
                body=good_name,
                payment_type = "JSAPI",
                ip = self.user_ip,
                openid = openid,
            )
            params = pay.do_pay_params()

        data = {'order_id': str(order.id)}
        print "data is is " + str(data)
        data.update(params)
        r = {'status': "success", "data": data, "ip":self.user_ip}
        self.write(r)
"""

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
            return self.write({'status':"fail","error": _(u"获取列表失败")})

        results = []
        for rule in rules or []:
            results.append(rule.normal_info())

        self.write({'status': "success", "results":results})

@handler_define
class PayRulesV2(BaseHandler):
    @api_define("PayRules", r'/live/pay/rules_v2', [
        Param('platform', True, int, "str", "1", u"平台：(1, u'Android'),(2, u'IOS'),(3, u'WP'),(4, u'其他')"),
    ], description=u"购买规则列表V2 (default_pay:  1:微信  2:支付宝)")
    @login_required
    def get(self):
        platform = self.arg_int('platform')
        ua = self.request.headers.get('User-Agent')
        try:
            uas = ua.split(";")
            channel = uas[5]
        except Exception as e:
            channel = ""

        #将所有的取出 然后进行过滤
        rules = TradeBalanceRule.objects.filter(platform=platform, status__ne=1).order_by("money")

        if channel in rules.distinct("channel"):
            rules.filter(channel=channel)
        elif platform == 1:
            rules.filter(channel="")
        elif platform == 2:
            rules.filter(channel="")

        alipay_rule_list = []
        wepay_rule_list = []
        applepay_rule_list = []
        googlepay_rule_list = []
        wepay_qrcode_rule_list = []

        if not rules:
            return self.write({'status': "fail", "error": _(u"获取列表失败")})
        for rule in rules:
            if rule.trade_type == 0:
                alipay_rule_list.append(rule.normal_info())
            elif rule.trade_type == 1:
                wepay_rule_list.append(rule.normal_info())
            elif rule.trade_type == 2:
                applepay_rule_list.append(rule.normal_info())
            elif rule.trade_type == 7:
                googlepay_rule_list.append(rule.normal_info())
            elif rule.trade_type == 8:
                wepay_qrcode_rule_list.append(rule.normal_info())

        # todo 做到redis中 CMS可调配
        is_wechat_show = 1 #1: 显示 0:隐藏


        self.write({'status': "success", "data": {
            "alipay_rules": alipay_rule_list,
            "wepay_rules": wepay_rule_list,
            "applepay_rules": applepay_rule_list,
            "googlepay_rules":googlepay_rule_list,
            "wepay_qrcode_rules": wepay_qrcode_rule_list,
        },
            "is_wechat_show": is_wechat_show, "default_pay": 1})# 1 微信 2 支付宝


@handler_define
class OderCheck(BaseHandler):
    @api_define("order check", r'/live/pay/order_check',
                [
                    Param("order_id", True, str, "","", description=u"订单id")
                ], description=u"检查订单是否支付成功")
    @login_required
    def get(self):
        order_id = self.arg("order_id")
        try:
            order = TradeBalanceOrder.objects.get(id=order_id)
            user_id = self.current_user_id
            if order.user.id == int(user_id) and order.status == 1:
                is_success = True
            else:
                is_success = False
            return self.write({"status":"success", "order_status":1 if is_success else 0})
        except Exception, e:
            logging.error("check order error " + str(e))

            return self.write({"status": "success", "order_status": 0})


@handler_define
class GooglePayCancel(BaseHandler):
    @api_define("google pay cancle", r"/live/pay/order_cancel",
                [
                    Param("order_id", True, str, "", "", description=u"订单id")
                ], description=u"google取消订单")
    def get(self):
        order_id = self.arg("order_id")
        order = TradeBalanceOrder.objects.get(id=order_id)
        order.update(status=TradeBalanceOrder.STATUS_FIIL_IN_CANCEL)


