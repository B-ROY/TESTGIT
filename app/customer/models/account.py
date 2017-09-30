# coding=utf-8

import calendar

from api.apiexceptions.apiexception import *
from app.customer.models.benifit import TicketAccount
from app.customer.models.promotion import *
from app.customer.models.userok import OkUser
from app.util.messageque.msgsender import MessageSender
from app.util.paylib.wempayapi import WeMPay
from base.settings import CHATPAMONGO
from mongoengine import *
from wi_model_util.imodel import attach_foreignkey
from app_redis.user.models.user import *


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class Account(Document):
    user = GenericReferenceField("User", verbose_name=u'用户')
    diamond = IntField(verbose_name=u'余额', default=0)
    diamond_bonus = IntField(verbose_name=u'赠送的钱', default=0)
    real_diamond = IntField(verbose_name=u"充值的剩下的钱",default=0)
    charge = IntField(verbose_name=u"用户总充值")
    last_diamond = IntField(verbose_name=u'最后消费之前的余额', default=0)
    update_time = DateTimeField(verbose_name=u"最后更新时间", default=datetime.datetime.now())


    class Meta:
        app_label = "customer"
        verbose_name = u"用户账户"
        verbose_name_plural = verbose_name

    def diamond_trade_in(self, diamond, diamond_bonus, desc, trade_type):
        """
        +加引力币
        """
        tar = TradeDiamondRecord(user=self.user)
        tar.before_balance = self.diamond
        tar.after_balance = self.diamond + diamond
        tar.desc = desc
        tar.diamon = diamond + diamond_bonus
        tar.trade_type = trade_type
        tar.created_time = datetime.datetime.now()
        tar.save()

        TicketAccount.add_inviter_charge_ticket(self.user.id, diamond)

        self.last_diamond = self.diamond
        self.diamond += diamond + diamond_bonus
        self.charge += diamond
        self.update_time = datetime.datetime.now()
        self.save()
        #发送充值漂流瓶
        if diamond >= 1:
            MessageSender.send_charge_bottle_message(self.user.id)
            MessageSender.send_charge_info_message(self.user.id, self.user.nickname, diamond)

        #如果总充值超过200 则将其标记为目标用户
        # if  self.charge >= 20000 and self.charge < 20000 + diamond:
        #     result = UserRedis.add_target_user(self.user.id)
        #     if result != 1 :
        #         logging.error("target user error: user_id " + str(self.user.id) + " times " + str(result))

        if self.charge >= 5000:
            olduser = UserRedis.is_target_user(self.user.id)
            if not olduser:
                okuser = OkUser.objects.filter(user_id = self.user.id).first()
                if not okuser:
                    OkUser.create(self.user.id)
                else:
                    okuser.update(set__created_time = datetime.datetime.now())
    def diamond_trade_out(self, price, desc, trade_type):

        """
        -减钱
        """
        if self.diamond < price:
            raise AccountException(
                ACCOUNT_INSUFFICIENT_BALANCE
            )


        tar = TradeDiamondRecord(
            user=self.user,
            before_balance=self.diamond,
            after_balance=self.diamond - price,
            diamon=price,
            desc=desc,
            created_time=datetime.datetime.now(),
            trade_type=trade_type,
        )
        tar.save()

        # 如果账号余额小于 当前价格 抛出异常

        self.update(set__last_diamond = self.diamond,
                    dec__diamond=price,
                    set__update_time=datetime.datetime.now(),
                    )



    def ticket_trade_in(self, price, desc, trade_type, ):
        """
        +加粒子数
        """
        tar = TradeTicketRecord(user=self.user)
        tar.before_balance = self.user.ticket
        tar.after_balance = self.user.ticket + price
        tar.desc = desc
        tar.ticket = price
        tar.trade_type = trade_type
        tar.created_time = datetime.datetime.now()
        tar.save()

        TicketAccount.add_ticket(user=self.user, trade_type=trade_type, ticket=price)

        # todo 删除下面下面的
        self.user.ticket += price
        self.update_time = datetime.datetime.now()
        self.user.save()

    def ticket_trade_out(self, price, desc, trade_type):

        """
        -减粒子数
        """
        tar = TradeTicketRecord(user=self.user)

        # 如果账号余额小于 当前价格 抛出异常
        if self.user.ticket < price:
            raise AccountException(
                ACCOUNT_INSUFFICIENT_BALANCE
            )

        tar.before_balance = self.user.ticket
        tar.after_balance = self.user.ticket - price
        tar.desc = desc
        tar.ticket = price
        tar.trade_type = trade_type
        tar.created_time = datetime.datetime.now()
        tar.save()

        self.user.ticket -= price
        self.update_time = datetime.datetime.now()
        self.user.save()

    ####################################################
    #                    创建支付订单                    #
    ####################################################
    # 创建充值订单,1，创建支付订单，2. 支付成功回调 fill_in
    def fill_in_create_order(self, money, platform, fill_in_type, user_agent, apple_product_id=None):

        if apple_product_id and fill_in_type == 2:
            rule = TradeBalanceRule.objects.filter(apple_product_id=apple_product_id, platform=platform,
                                                   trade_type=fill_in_type).first()
            # print rule,apple_product_id
            if not rule:
                logging.error("rule 规则为空")
                return False
        else:
            rule = TradeBalanceRule.get_rule(money=money, platform=platform, tradetype=fill_in_type)
            if not rule:
                logging.error("rule 规则为空")
                return False

        order = TradeBalanceOrder()
        order.user = User.objects.get(id=self.user.id)
        order.desc = u"充值创建订单"
        order.rule = rule
        order.buy_time = datetime.datetime.now()
        order.trade_type = TradeBalanceOrder.TradeType_IN
        order.diamon = rule.diamon
        order.status = TradeBalanceOrder.STATUS_FILL_IN_WAIT_PAY
        order.money = money
        order.fill_in_type = fill_in_type
        order.platform = platform
        order.user_agent = user_agent
        order.save()
        return order

    @classmethod
    def fill_in(cls, order_id):
        from app.customer.models.vip import UserVip, Vip
        order = TradeBalanceOrder.objects.filter(id=order_id).first()
        if not order:
            logging.error(u"order not exist %s" % order_id)
            print "order not exist"
            return False
        elif order.status == TradeBalanceOrder.STATUS_FILL_IN_PAYED:
            logging.warn(u"order has filled in")
            return True
        elif order.status == TradeBalanceOrder.STATUS_FILL_IN_WAIT_PAY:

            print "order_id is " + order_id
            order.status = TradeBalanceOrder.STATUS_FILL_IN_PAYED
            order.filled_time = datetime.datetime.now()
            order.save()

            user = order.user
            user_vip = UserVip.objects.filter(user_id=user.id).first()
            diamond_bonus = 0
            if user_vip:
                vip = Vip.objects.filter(id=user_vip.vip_id).first()
                if vip.vip_type == 2:
                    diamond_bonus = order.rule.free_diamon
                    order.update(set__free_diamon=diamond_bonus)

            account = Account.objects.get(user=user)
            account.diamond_trade_in(order.diamon, diamond_bonus, u"充值", TradeDiamondRecord.TradeTypeExchange)

            # try:
            #     # 首充活动
            #     act = FirstChargeActivity.objects.filter(temp_activity_type=1).first()
            #     now = datetime.datetime.now()
            #
            #     #  判断是否活动有效
            #     if act:
            #         end_time = act.end_time
            #         days = (end_time - now).days
            #         if days < 0:
            #             return True
            #
            #     #  判断是否是后台充值
            #     if order.fill_in_type == 6:
            #         return True
            #
            #     #判断首充
            #     starttime = now.strftime("%Y-%m-%d 00:00:00")
            #     endtime = now.strftime('%Y-%m-%d 23:59:59')
            #     order_count = TradeBalanceOrder.objects.filter(status='1', user=user, buy_time__gte=starttime,
            #                                                    buy_time__lte=endtime,).count()
            #     if order_count > 1:
            #         return True
            #
            #     money = order.money
            #     FirstChargeActivity.create_reward(user, money)
            #
            # except Exception, e:
            #     logging.error(" FirstChargeActivity  error:{0}".format(e))

            return True
        elif order.status == TradeBalanceOrder.STATUS_FIIL_IN_CANCEL:
            logging.warn(u"order is cancelled " + str(order_id))
            return False
        else:
            logging.error("order status " + str(order.status))
            return False

    @classmethod
    def fill_out(cls, order_id):
        """
        退费(预留接口)
        """
        order = TradeBalanceOrder.objects.filter(id=order_id,
                                                 status=TradeBalanceOrder.STATUS_FILL_IN_PAYED).first()
        if not order:
            logging.error(u"order not exist %s" % order_id)
            print "order not exist"
            return False

        order.status = TradeBalanceOrder.STATUS_FILL_IN_BACK
        order.filled_time = datetime.datetime.now()
        order.save()
        order.user.account.diamond_trade_out(order.diamon, u"充值退还", TradeBalanceOrder.TradeType_OUT)

        return True

    ####################################################
    #                    创建提现订单                    #
    ####################################################
    #def withdraw_out_create_order(self, alipay_acccount, name, phone, ticket, money, harvest, platform, fill_in_type=1,
    #                              trade_type=1):

        # 判断余额
    #    if self.user.ticket < ticket:
    #        raise AccountException(
    #            ACCOUNT_INSUFFICIENT_BALANCE
    #        )
    #    order = WithdrawBalanceOrder()
    #    order.alipay_acccount = alipay_acccount
    #    order.name = name
    #    order.phone = phone
    #    order.user = self.user
    #    order.ticket = ticket
    #    order.money = money
    #    order.harvest = harvest
    #    order.desc = u"申请提现"
    #    order.platform = platform
    #    order.fill_in_type = fill_in_type
    #    order.trade_type = trade_type
    #    order.save()

        # 减粒子数
    #    self.ticket_trade_out(order.ticket, u"提现", WithdrawBalanceOrder.TradeType_PRE)
    #    return True

    #def withdraw_out_order_pass(self, order, alipay_order_id, alipay_order_image):
    #    """
    #    提现订单通过
    #    """
    #    if not order:
    #        return False

    #    return self.withdraw_out(order, alipay_order_id, alipay_order_image)

    #def withdraw_out_order_dismiss(self, order, dismiss_reason=""):
    #    """
    #    提现订单驳回
    #    """
    #    if not order:
    #        return False
    #    order.status = WithdrawBalanceOrder.STATUS_FILL_IN_DISMISS
    #    if dismiss_reason:
    #        order.dismiss_reason = dismiss_reason
    #    order.save()

        # 退粒子数
    #    self.ticket_trade_in(order.ticket, u"提现驳回", WithdrawBalanceOrder.TradeType_BACK)
    #    return True

    # TODO: 没法保证微信成功后，改函数一定被执行了
    # @transaction.commit_on_success
    # def withdraw_out(self, order, withdraw_callback):
    #def withdraw_out(self, order, alipay_order_id, alipay_order_image):
    #    if not order:
    #        return False
    #    if not alipay_order_id:
    #        raise Exception("支付宝订单号为空")
    #    if not alipay_order_image:
    #        raise Exception("支付宝支付截图为空")

    #    order.alipay_order_id = alipay_order_id
    #    order.alipay_order_image = alipay_order_image
    #    order.status = WithdrawBalanceOrder.STATUS_FILL_IN_SUCCESS
    #    order.filled_time = datetime.datetime.now()
    #    order.save()

    #    order.user.locked_ticket -= order.ticket
    #    order.user.save()

    #    return True


##################################################
#               系统内部引力币交易流水                #
##################################################
class TradeDiamondRecord(Document):
    TradeTypeExchange = 0  # 兑换(买引力币)
    TradeTypeGift = 1  # 购买礼物
    TradeTypeAudio = 2  # 语音聊天
    TradeTypePicture = 3  # 图片解锁
    TradeTypeSignin = 4  # 每日签到
    TradeTypeShare = 5  # 分享
    TradeTypeMessage = 6  # 消息门槛送礼
    TradeTypeVideo = 7  # 视频聊天
    TradeTypeTools = 8  # 购买道具
    TradeTypeBottle = 9  # 漂流瓶消耗余额
    TradeTypeVIP = 10  # 购买会员
    TradeTypeClairvoyant = 11  # 千里眼消耗金额
    TradeTypePrivateVideo = 12  # 千里眼消耗金额

    TradeType = [
        (0, u'兑换'),
        (1, u'购买礼物'),
        (2, u'语音聊天'),
        (3, u'图片解锁'),
        (4, u'每日签到'),
        (5, u'分享'),
        (6, u'消息门槛送礼'),
        (7, u'视频聊天'),
        (8, u'购买道具'),
        (9, u'漂流瓶消耗余额'),
        (10, u'购买会员'),
        (11, u'千里眼消耗金额'),
        (12, u'购买私房视频'),
    ]

    user = GenericReferenceField("User", verbose_name=u'用户')
    before_balance = IntField(verbose_name=u'交易前余额')
    after_balance = IntField(verbose_name=u'交易后余额')
    diamon = IntField(verbose_name=u'交易引力币')
    desc = StringField(verbose_name=u"描述", max_length=256, default='')
    created_time = DateTimeField(verbose_name=u"购买时间", default=datetime.datetime.now())
    trade_type = IntField(verbose_name=u'交易类型', choices=TradeType)

    class Meta:
        app_label = "customer"
        verbose_name = u"充值交易记录"
        verbose_name_plural = verbose_name


class TradeTicketRecord(Document):
    TradeTypeGift = 0  # 购买礼物
    TradeTypeExchange = 1  # 兑换
    TradeTypeAudio = 2  # 语音聊天
    TradeTypePicture = 3  # 图片解锁
    TradeTypeSignin = 4  # 每日签到
    TradeTypeShare = 5  # 分享
    TradeTypeMessage = 6  # 消息门槛送礼
    TradeTypeVideo = 7  # 视频聊天
    TradeTypePrivateVideo = 8  # 私房视频购买


    TradeType = [
        (0, u'购买礼物'),
        (1, u'兑换'),
        (2, u'语音聊天'),
        (3, u'图片解锁'),
        (4, u'每日签到'),
        (5, u'分享'),
        (6, u'消息门槛送礼'),
        (7, u'视频聊天'),
        (8, u'私房视频购买'),
    ]

    user = GenericReferenceField("User", verbose_name=u'用户')
    before_balance = IntField(verbose_name=u'交易前余额')
    after_balance = IntField(verbose_name=u'交易后余额')
    ticket = IntField(verbose_name=u'交易ticket')
    desc = StringField(verbose_name=u"描述", max_length=256, default='')
    created_time = DateTimeField(verbose_name=u"购买时间", default=datetime.datetime.now())
    trade_type = IntField(verbose_name=u'交易类型', choices=TradeType)

    class Meta:
        app_label = "customer"
        verbose_name = u"ticket交易记录"
        verbose_name_plural = verbose_name


##################################################
#               系统内部引力币交易&流水               #
##################################################

class TradeBalanceRule(Document):
    PLATFORM = [
        (1, u'Android'),
        (2, u'IOS'),
        (3, u'WP'),
        (4, u'其他')
    ]
    PLATFORM_AND = 1
    PLATFORM_IOS = 2
    PLATFORM_H5 = 3
    PLATFORM_OTH = 4

    TRADETYPE = [
        (0, u'支付宝'),
        (1, u'微信'),
        (2, u'苹果'),
        (3, u'微信JSAPI'),
        (4, u'银联'),
        (5, u'其他'),
        (6, u'后台添加'),
        (7, u'google pay'),
        (8, u'扫码支付'),
        (9, u'helipay'),
        (10, u'官方代充'),
    ]


    money = IntField(verbose_name=u'人民币')
    diamon = IntField(verbose_name=u'引力币', default=0)
    free_diamon = IntField(verbose_name=u'赠送多少引力币', default=0)
    desc = StringField(verbose_name=u"描述", max_length=20, default='')
    platform = IntField(verbose_name=u'平台', choices=PLATFORM)
    apple_product_id = StringField(verbose_name=u"苹果产品id", max_length=20, default='')
    update_time = DateTimeField(verbose_name=u"最后更新时间", default=datetime.datetime.now())
    trade_type = IntField(verbose_name=u'支付方式', choices=TRADETYPE)
    activity_desc = StringField(verbose_name=u"活动说明", max_length=256, default=None)
    channel = StringField(verbose_name=u"分渠道展示价格特殊价格", default="chatpa")
    google_product_id = StringField(verbose_name=u"google产品id")
    status = IntField(verbose_name=u'状态', default=0)

    class Meta:
        app_label = "customer"
        verbose_name = u"充值规则"
        verbose_name_plural = verbose_name

    def normal_info(self):
        return {
            "money": self.money,
            "diamon": self.diamon,
            "free_diamon": self.free_diamon,
            "desc": self.desc,
            "apple_product_id": self.apple_product_id,
            "platform": self.platform,
            "trade_type": self.trade_type,
            "google_product_id": self.google_product_id
        }

    @classmethod
    def do_invalid(cls, id):
        cls.objects.filter(id=id).delete()

    @classmethod
    def get_list(cls):
        return cls.objects.filter(status__ne=1).order_by("-activity_desc", "money")

    @classmethod
    def get_rule(cls, money, platform, tradetype):
        return cls.objects.filter(money=money, platform=platform, trade_type=tradetype).first()

    @classmethod
    def create(cls, money, diamon, free_diamon, desc, apple_product_id, trade_type, activity_desc,
               platform=PLATFORM_OTH, channel=""):
        try:
            _obj = cls()
            _obj.money = money
            _obj.diamon = diamon
            _obj.free_diamon = free_diamon
            _obj.apple_product_id = apple_product_id
            _obj.platform = platform
            _obj.desc = desc
            _obj.trade_type = trade_type
            _obj.activity_desc = activity_desc
            _obj.update_time = datetime.datetime.now()
            _obj.channel = channel
            _obj.save()
            return _obj
        except Exception, e:
            logging.error("create TradeBalanceRule error:{0}".format(e))
        return ''

    @classmethod
    def update(cls, obj_id, money, diamon, free_diamon, desc, apple_product_id, trade_type, activity_desc,
               platform=PLATFORM_OTH):
        try:
            _obj = cls.objects.get(id=obj_id)
            _obj.money = money
            _obj.diamon = diamon
            _obj.free_diamon = free_diamon
            _obj.desc = desc
            _obj.platform = platform
            _obj.apple_product_id = apple_product_id
            _obj.trade_type = trade_type
            _obj.activity_desc = activity_desc
            _obj.update_time = datetime.datetime.now()
            _obj.save()
            return _obj
        except Exception, e:
            logging.error("update TradeBalanceRule error:{0}".format(e))
        return ''





class TradeBalanceOrder(Document):
    TradeType_IN = 0
    TradeType_OUT = 1

    TradeType = [
        (0, u'流入'),
        (1, u'流出'),
    ]

    FILL_IN_TYPE = [

        (0, u'支付宝'),
        (1, u'微信'),
        (2, u'苹果'),
        (3, u'微信JSAPI'),
        (4, u'银联'),
        (5, u'其他'),
        (6, u'后台添加余额'),
        (7, u'goole支付'),
        (8, u'扫码支付'),
        (9, u'helipay'),
        (10, u'官方代充'),
    ]

    FILL_IN_TYPE_MAP = {
        0: u'支付宝',
        1: u'微信',
        2: u'苹果',
        3: u'微信JSAPI',
        4: u'银联',
        5: u'其他',
        6: u'后台添加余额',
    }
    FILL_IN_TYPE_ALIPAY = 0
    FILL_IN_TYPE_WECHAT = 1
    FILL_IN_TYPE_IAP = 2
    FILL_IN_TYPE_WECHAT_JS = 3
    FILL_IN_TYPE_UNIONPAY = 4
    FILL_IN_TYPE_OTHER = 5
    FILL_IN_TYPE_REPLACE = 6

    PLATFORM = [
        (1, u'Android'),
        (2, u'IOS'),
        (3, u'WP'),
        (4, u'其他')
    ]

    PLATFORM_DICT = dict(PLATFORM)
    FILL_IN_TYPE_DICT = dict(FILL_IN_TYPE)
    TradeType_DICT = dict(TradeType)

    STATUS_FILL_IN_WAIT_PAY = 0
    STATUS_FILL_IN_PAYED = 1
    STATUS_FILL_IN_ERROR_RULE = 2
    STATUS_FILL_IN_ERROR = 3
    STATUS_FILL_IN_BACK = 4
    STATUS_FIIL_IN_CANCEL = 5

    STATUS_PAY_MAP = {
        STATUS_FILL_IN_WAIT_PAY: u'等待支付',
        STATUS_FILL_IN_PAYED: u'支付成功',
        STATUS_FILL_IN_ERROR_RULE: u'规则错误',
        STATUS_FILL_IN_ERROR: u'支付失败',
        STATUS_FILL_IN_BACK: u'退费',
        STATUS_FIIL_IN_CANCEL: u'取消'
    }
    user = GenericReferenceField("User", verbose_name=u'用户')
    rule = GenericReferenceField("TradeBalanceRule", verbose_name=u'交易规则')
    diamon = IntField(verbose_name=u'交易引力币')
    free_diamon = IntField(verbose_name=u'赠送钻石')

    money = IntField(verbose_name=u'交易金额')
    desc = StringField(verbose_name=u"描述", max_length=20, default='')
    user_agent = StringField(verbose_name=u"ua", max_length=128, default='')

    # 下单时间
    buy_time = DateTimeField(verbose_name=u"购买时间", default=datetime.datetime.now())

    filled_time = DateTimeField(verbose_name=u"支付成功时间")
    # 流入/流出
    trade_type = IntField(verbose_name=u'交易类型', choices=TradeType)

    # 充值渠道
    fill_in_type = IntField(verbose_name=u'充值类型', choices=FILL_IN_TYPE)

    platform = IntField(verbose_name=u'平台', choices=PLATFORM)
    status = IntField(verbose_name=u'充值类型', default=0)

    # 订单号（预留一个 外部订单号）
    order_id = StringField(max_length=64, verbose_name=u'订单号')
    out_order_id = StringField(max_length=64, verbose_name=u'外部订单号')

    class Meta:
        app_label = "customer"
        verbose_name = u"充值交易记录"
        verbose_name_plural = verbose_name

    def normal_info(self):
        return {
            'id': self.id,
            'user_nickname': self.user.nickname,
            'diamon': self.diamon,
            'money': self.money,
            'desc': self.desc,
            'pay_buy_time': datetime_to_timestamp(self.buy_time),
            'pay_success_time': datetime_to_timestamp(self.filled_time),
            'status': self.STATUS_PAY_MAP.get(self.status, 0),
            'trade_type': self.FILL_IN_TYPE_MAP.get(self.trade_type, 5),
        }

    @classmethod
    def order_list(cls, user_id, page=1, page_count=20):
        """
        function: 我关注的
        """
        user = User.objects.get(id=user_id)
        qs = cls.objects.filter(user=user).order_by("-buy_time")[(page - 1) * page_count:page * page_count]
        attach_foreignkey(qs, cls.user)
        return qs


##################################################
#               系统提现申请                       #
##################################################


class WithdrawRequest(Document):

    WITHDRAW_STATUS = [
        (0, u"已提交"),
        (2, u"已提现"),
        (3, u"被驳回"),
        (4, u"已通过"),
    ]
    # 同意提现申请返回值
    ASSENT_WITHDARW_REQUEST_RETURN_CODE = [
        (0, u"异常终止"),
        (1, u"余额不足"),
        (2, u"没有通过实名认证"),
        (100, u"超出当日提现限额"),
        (200, u"提现成功"),
        (400, u"微信打款失败" )
    ]

    WITHDRAW_MONEY_LIST = [
        5000, 10000, 20000, 30000,40000,50000
    ]

    user_id = IntField(verbose_name=u"用户id")
    request_money = IntField(verbose_name=u"提现金额(分)")
    actual_money = IntField(verbose_name=u"实际到账金额")
    request_ticket = IntField(verbose_name=u"提现所需收益")
    request_time = DateTimeField(verbose_name=u"提现日期", default=datetime.datetime.now())
    feedback_time = DateTimeField(verbose_name=u"结果反馈时间")
    fillin_time = DateTimeField(verbose_name=u"提现成功时间")
    status = IntField(verbose_name=u"提现状态", choices=WITHDRAW_STATUS)
    feedback_reason = StringField(verbose_name=u"提现反馈", max_length=128)
    user_agent = StringField(verbose_name=u"用户ua", max_length=1024)
    openid = StringField(verbose_name=u"商户下openid", max_length=128)
    ip = StringField(verbose_name=u"用户ip", max_length=128)

    class_DAY_MONEY_LIMIT = 300000
    class_MONTH_MONEY_TAX_LIMIT = 80000
    class_TAX_RATE = 0.08

    class Meta:
        app_label = u"customer"
        verbose_name = u"提现申请审核"
        verbose_name_plural = verbose_name

    def normal_info(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "request_money": self.request_money,
            "request_ticket": 0 if not self.request_ticket else self.request_ticket,
            "request_time": datetime_to_timestamp(self.request_time),
            "feedback_time": datetime_to_timestamp(self.feedback_time),
            "fillin_time": datetime_to_timestamp(self.fillin_time),
            "status": self.status,
            "feedback_reason": self.feedback_reason,
        }

    @classmethod
    def create_withdraw_request(cls, user_id, request_money, user_agent, openid, ip=''):
        try:
            request = WithdrawRequest(
                user_id=user_id,
                request_money=request_money,
                request_time=datetime.datetime.now(),
                user_agent=user_agent,
                status=0,
                openid=openid,
                ip=ip,
            )
            request.save()
            ticket_account = TicketAccount.objects.get(user=User.objects.get(id=user_id))
            ticket_account.money_requesting += request_money
            ticket_account.save()
            desc = u"<html><p>"+_(u"亲爱的用户您好，提现申请已成功提交，请等待工作人员审核（1-2工作日）") + u"</p></br></html>"
            MessageSender.send_system_message(user_id, desc)
            return True
        except Exception,e:
            logging.error("create withdraw request error:{0}".format(e))
            return False

    # 获取已提现金额
    @classmethod
    def get_withdraw_money(cls, user_id):
        try:
            user = User.objects.get(id=user_id)

            """留作参考
            withdraw_money = 0
            requests = WithdrawRequest.objects.filter(user_id=user_id, status=2).order_by("-request_time")
            for request in requests:
                withdraw_money += request.request_money
            return withdraw_money
        except Exception,e:
            logging.error("get withdraw money error:{0}".format(e))
            return 0
            """
            return TicketAccount.objects.get(user=user).money_withdrawed
        except Exception, e:
            logging.error("get withdraw money error:{0}".format(e))
            return 0

    #拒绝提现申请
    @classmethod
    def reject_withdraw_request(cls,order_id, feedback_reason):
        try:
            request = WithdrawRequest.objects.get(id=order_id)
            request.status = 3
            request.feedback_time = datetime.datetime.now()
            request.feedback_reason = feedback_reason
            request.save()
            user = User.objects.get(id=order_id.user_id)
            TicketAccount.objects(user=user).update(
                dec__money_requesting=request.request_money
            )
            return True
        except Exception, e:
            logging.error("reject withdraw request error :{0}".format(e))
            return False

    #同意提现申请  先将状态置为4 微信打钱成功后再置为2
    @classmethod
    def assent_withdraw_request(cls, order_id):
        try:
            request = WithdrawRequest.objects.get(id=order_id)
            request.status = 4
            actual_money , status = WithdrawRequest.compute_actual_money(request)
            if status:
                return status  #超出限额
            request.actual_money = actual_money
            request.save()
            data = cls.withdraw(request)
            print "witch draw dict data is " + str(data)
            if data.get("result_code") == "SUCCESS":
                request.fillin_time = datetime.datetime.now()
                request.status = 2
                request.feedback_reason = u"后台通过审核已提现"
                request.save()
                user = User.objects.get(id=request.user_id)
                TicketAccount.objects(user=user).update(
                    dec__money_requesting=request.request_money,
                    inc__money_withdrawed=request.request_money,
                )
                return 200
            else:
                return 400
        except Exception, e:
            logging.error("assent withdraw request %s " % e)
            request.save()
            return 0


    @classmethod
    def withdraw(cls, request):
        wempay = WeMPay(openid=request.openid, partner_trade_no=request.id, amount=request.actual_money,
                        desc='withdraw', ip="123.206.18.230")
        return wempay.post_xml()

    @classmethod
    def compute_actual_money(cls,request):
        day_has_withdrawed = cls.compute_day_has_withdrawed(request.user_id)
        total_revenue = cls.compute_total_revenue(request.user_id)
        withdrawed_money = cls.get_withdraw_money(request.user_id)
        if total_revenue<withdrawed_money + request.request_money:
            return 0, 1
        if request.request_money + day_has_withdrawed>cls.class_DAY_MONEY_LIMIT:
            return 0, 100
        month_has_withdrawed_money = cls.compute_month_has_withdrawed(request.user_id)
        if month_has_withdrawed_money>cls.class_MONTH_MONEY_TAX_LIMIT:
            return request.request_money*(1-cls.class_TAX_RATE), 0
        elif month_has_withdrawed_money+request.request_money>cls.class_MONTH_MONEY_TAX_LIMIT:
            return request.request_money - cls.class_TAX_RATE*(request.request_money + month_has_withdrawed_money - cls.class_MONTH_MONEY_TAX_LIMIT),0
        else:
            return request.request_money, 0

    @classmethod
    def compute_month_has_withdrawed(cls, user_id):
        cur = datetime.datetime.now()
        month = cur.month
        year = cur.year
        first_week_day, month_range = calendar.monthrange(year,month)
        first_day_of_month = datetime.datetime(year=year,month=month,day=1)
        last_day_of_month = datetime.datetime(year=year,month=month,day=month_range)

        withdraws = WithdrawRequest.objects.filter(user_id=user_id, status=2, fillin_time__gte=first_day_of_month,fillin_time__lte=last_day_of_month).values_list("request_money")

        sum = 0
        for money in withdraws:
            sum += money

        return sum

    @classmethod
    def compute_day_has_withdrawed(cls, user_id):
        cur = datetime.datetime.now()
        month = cur.month
        year = cur.year
        today = datetime.datetime(year=year,month=month,day=cur.day)
        one_day = datetime.timedelta(days=1)
        tomorrow = today + one_day
        withdraws = WithdrawRequest.objects.filter(user_id=user_id, status=2, fillin_time__gte=today,fillin_time__lte=tomorrow).values_list("request_money")

        sum = 0
        for money in withdraws:
            sum += money

        return sum

    @classmethod
    def compute_total_revenue(cls, user_id):
        user = User.objects.get(id=user_id)

        """ 留作参考
        #获取邀请收益
        friend_revenue = 0
        invite_list = UserInviteCode.get_invite_list(invite_id=user.id)
        for invite_user in invite_list:
            friend_revenue += invite_user.ticket * 0.1
        return (friend_revenue + user.ticket) * 0.6
        """
        return TicketAccount.objects.get(user=user).money

    @classmethod
    def get_money_list(cls):
        #todo 新版入库
        moneys=[]
        for m in cls.WITHDRAW_MONEY_LIST:
            money = {}
            money["money"] = m
            moneys.append(money)
        return moneys









