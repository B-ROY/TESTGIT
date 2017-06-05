# coding=utf-8

import datetime
from mongoengine import *
from base.settings import CHATPAMONGO
from app.customer.models.account import *
from app.customer.models.user import User
from django.db.models import F


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)

# 道具
class Tools(Document):

    TOOLS_TYPE = (
        (0, u'门禁卡'),
        (1, u'漂流瓶'),
        (2, u'千里眼'),
    )

    name = StringField(max_length=32, verbose_name=u'名称')
    icon_url = StringField(max_length=256, verbose_name=u'icon图片')
    gray_icon_url = StringField(max_length=256, verbose_name=u'icon灰色图片')
    price = IntField(verbose_name=u'道具价格', default=0)
    tools_type = IntField(verbose_name=u"道具类型", choices=TOOLS_TYPE)

    class Meta:
        app_label = "customer"
        verbose_name = u"道具"
        verbose_name_plural = verbose_name

    def normal_info(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "icon_url": self.convert_http_to_https(self.icon_url),
            "gray_icon_url": self.convert_http_to_https(self.gray_icon_url),
            "price": self.price,
            "tools_type": self.tools_type,
        }

    def convert_http_to_https(self, url):
        if "https" in url:
            return url
        else:
            return url.replace("http", "https")


# 用户拥有道具
class UserTools(Document):

    TIME_TYPE = (
        (0, u"一天"),  # 一天的道具来源于两处 "收到" 和 "会员自动发放"
        (1, u"永久"),  # 永久道具来源于 会员购买
    )

    GET_TYPE = (
        (0, u"收到"),  # 限时一天的道具 (避免多次点击"领取")
        (1, u"会员自动发放"),  # 限时一天的道具
        (2, u"购买"),
    )

    user_id = IntField(verbose_name=u'用户id', required=True)
    tools_id = StringField(max_length=64, verbose_name=u"道具id")
    tools_count = IntField(verbose_name=u"道具数量", default=0)
    time_type = IntField(verbose_name=u"道具时限类型", choices=TIME_TYPE)
    get_type = IntField(verbose_name=u"获取方式", choices=GET_TYPE)
    invalid_time = DateTimeField(verbose_name=u"失效日期")

    # 用户购买道具, 购买道具为永久道具 (判断余额, 添加用户道具, 添加记录)
    @classmethod
    def buy_tools(cls, user_id, tools_id):
        user = User.objects.filter(id=user_id).first()
        account = Account.objects.filter(user=user).first()
        tools = Tools.objects.filter(id=tools_id).first()
        status = 200
        message = "success"
        now = datetime.datetime.now()

        if account.diamond < tools.price:
            status = -1
            message = "您的账户余额不足"
            return status, message
        try:

            # 用户账号余额
            # account.last_diamond = account.diamond
            # account.diamond -= tools.price
            # account.update_time = datetime.datetime.now()
            # account.save()

            account.diamond_trade_out(price=tools.price, desc=u"购买道具, 道具id=%s" %
                                                                   (str(tools.id)), trade_type=TradeDiamondRecord.TradeTypeTools)


            user_tools = UserTools.objects.filter(user_id=user_id, tools_id=str(tools_id), time_type=1).first()
            if user_tools:
                user_tools.tools_count += 1
                user_tools.save()
            else:
                user_tools = UserTools()
                user_tools.user_id = user_id
                user_tools.tools_id = tools_id
                user_tools.tools_count = 1
                user_tools.time_type = 1
                user_tools.get_type = 2
                user_tools.invalid_time = None
                user_tools.save()

            # 道具记录
            tools_record = UserToolsRecord()
            tools_record.user_id = user_id
            tools_record.tools_id = str(tools.id)
            tools_record.tools_count = 1
            tools_record.time_type = 1
            tools_record.oper_type = 2
            tools_record.create_time = now
            tools_record.save()
            return status, message

        except Exception, e:
            status = -1
            message = "error"
            return status, message

    @classmethod
    def has_tools(cls, user_id, tool_id):
        count = UserTools.objects.filter(tools_id=tool_id, user_id=user_id).count()
        if count == 0:
            return 0  # 无道具
        else:
            return 1  # 有道具

    # 消耗一个道具
    @classmethod
    def reduce_tools(cls, user_id, tools_id):
        limit_tools = UserTools.objects.filter(time_type=0, tools_id=tools_id, user_id=user_id).first()
        if limit_tools:
            time_type = 0
            if limit_tools.tools_count > 1:
                limit_tools.tools_count -= 1
                limit_tools.save()
            else:
                limit_tools.delete()
        else:
            # 如果没有 限时道具
            time_type = 1
            tools = UserTools.objects.filter(tools_id=tools_id, user_id=user_id).first()
            if tools.tools_count > 1:
                print tools.tools_count, "+========================="
                tools.tools_count -= 1
                tools.save()
            else:
                tools.delete()

        # 创建记录
        record = UserToolsRecord()
        record.user_id = user_id
        record.tools_id = tools_id
        record.tools_count = 1
        record.time_type = time_type
        record.oper_type = 0
        record.create_time = datetime.datetime.now()
        record.save()


# 用户道具 记录表
class UserToolsRecord(Document):

    TIME_TYPE = (
        (0, u"一天"),
        (1, u"永久"),
    )

    OPER_TYPE = (
        (0, u"正常使用"),
        (1, u"到时销毁"),
        (2, u"购买道具"),
        (3, u"会员发放道具"),
        (4, u"领取道具"),
    )

    user_id = IntField(verbose_name=u'用户id', required=True)
    tools_id = StringField(max_length=64, verbose_name=u"道具id")
    tools_count = IntField(verbose_name=u"道具数量", default=0)
    time_type = IntField(verbose_name=u"道具时限类型", choices=TIME_TYPE)
    oper_type = IntField(verbose_name=u"操作形式", choices=OPER_TYPE)
    create_time = DateTimeField(verbose_name=u"创建时间")


# 道具赠送 记录表
class SendToolsRecord(Document):

    send_id = IntField(verbose_name=u'发送道具用户id', required=True)
    receive_id = IntField(verbose_name=u'接收道具用户id', required=True)
    tools_id = StringField(max_length=64, verbose_name=u"道具id")
    tools_count = IntField(verbose_name=u"道具数量", default=0)
    create_time = DateTimeField(verbose_name=u"创建时间")
    update_time = DateTimeField(verbose_name=u"更新时间")

    @classmethod
    def add(cls,send_id, receive_id, tools_id, tools_count):
        record = SendToolsRecord.objects.filter(send_id=send_id, receive_id=receive_id, tools_id=tools_id).first()
        now = datetime.datetime.now()
        if record:
            record.tools_count += tools_count
            record.update_time = now
            record.save()
        else:
            send_record = SendToolsRecord()
            send_record.send_id = send_id
            send_record.receive_id = receive_id
            send_record.tools_id = tools_id
            send_record.tools_count = tools_count
            send_record.create_time = now
            send_record.update_time = now
            send_record.save()






