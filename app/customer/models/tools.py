# coding=utf-8

import datetime
from mongoengine import *
from base.settings import CHATPAMONGO
from app.customer.models.account import Account, TradeDiamondRecord
from app.customer.models.user import User
from django.db.models import F
from app.customer.models.user import VideoManagerVerify
from app.util.messageque.msgsender import MessageSender


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
    tools_type = IntField(verbose_name=u"道具类型")
    is_valid = IntField(verbose_name=u'是否有效', default = 1) #1有效，0 无效
    desc = StringField(verbose_name=u'描述', max_length=256, default="")

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
            "is_valid": self.is_valid,
            "desc": self.desc
        }

    def convert_http_to_https(self, url):
        if "https" in url:
            return url
        else:
            return url.replace("http", "https")

    @classmethod
    def send_activity_tools(cls, user_id):
        now = datetime.datetime.now()
        now_str = now.strftime('%Y-%m-%d 23:59:59')
        hm = cls.get_hm(now)
        activity_id = ""
        user = User.objects.filter(id=user_id).first()
        receive_data = {}

        if user.is_video_auth == 1:
            #  主播
            verify = VideoManagerVerify.objects.filter(user_id=user_id).first()
            if not verify:
                return
            verify_time = verify.verify_time
            temp_end_time = verify_time + datetime.timedelta(days=7)
            endtime = temp_end_time.strftime('%Y-%m-%d 23:59:59')

            # 6-22 之前认证的都属于老主播
            compare_time = datetime.datetime(2017, 6, 21)

            if verify_time < compare_time or datetime.datetime.strptime(endtime, "%Y-%m-%d %H:%M:%S") < now:
                # 老主播
                status, activity = cls.check_receive(2, now, user_id)
                if status == 3:
                    receive_data = eval(activity.tools_data)
                    activity_id = str(activity.id)
            else:
                # 新主播
                status, activity = cls.check_receive(1, now, user_id)
                if status == 3:
                    receive_data = eval(activity.tools_data)
                    activity_id = str(activity.id)
        else:
            #  非主播
            status, activity = cls.check_receive(3, now, user_id)
            if status == 3:
                receive_data = eval(activity.tools_data)
                activity_id = str(activity.id)

        if receive_data:
            for key, value in receive_data.items():
                tools = Tools.objects.filter(tools_type=int(key)).first()  # 道具
                user_tools = UserTools()
                user_tools.user_id = user_id
                user_tools.tools_id = str(tools.id)
                user_tools.tools_count = int(value)
                user_tools.time_type = 0
                user_tools.get_type = 4
                invalid_time = now + datetime.timedelta(days=1)
                user_tools.invalid_time = invalid_time
                user_tools.save()

                tools_record = UserToolsRecord()
                tools_record.user_id = user_id
                tools_record.tools_id = str(tools.id)
                tools_record.tools_count = 1
                tools_record.time_type = 0
                tools_record.oper_type = 4
                tools_record.create_time = now
                tools_record.save()

            activity_record = ToolsActivityRecord()
            activity_record.user_id = user_id
            activity_record.date_time = datetime.datetime(now.year, now.month, now.day)
            activity_record.tools_activity_id = activity_id
            activity_record.save()

            desc = u"<html><p>" + _(u"您的活动奖励已发送至您的账户，请注意查收，希望您在我们平台玩得开心～") + u"</p></br></html>"
            MessageSender.send_system_message(user.sid, desc)

    @classmethod
    def check_receive(cls, role, date_time, user_id):
        hm = cls.get_hm(date_time)
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

    @classmethod
    def get_hm(cls, now):
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



# 用户拥有道具
class UserTools(Document):

    TIME_TYPE = (
        (0, u"一天"),  # 一天的道具来源于两处 "收到" 和 "会员自动发放"
        (1, u"永久"),  # 永久道具来源于 购买
    )

    GET_TYPE = (
        (0, u"收到"),  # 限时一天的道具 (避免多次点击"领取")
        (1, u"会员自动发放"),  # 限时一天的道具
        (2, u"购买"),
        (3, u"后台添加"),
        (4, u"活动奖励"),
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

        # 判断道具是否为下架道具
        if tools.is_valid == 0:
            status = -1
            message = "此道具已下架,不可再购买"
            return status, message


        if account.diamond < tools.price:
            status = -1
            message = "您的账户余额不足"
            return status, message
        try:

            # 用户账号余额
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
        return time_type


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
        (5, u"后台添加"),
        (6, u"活动奖励添加"),

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


# 领取道具活动
class ToolsActivity(Document):

    Delete_STATUS = (
        (0, u"删除"),
        (1, u"未删除"),
    )

    name = StringField(max_length=512, verbose_name=u"名称")
    tools_data = StringField(max_length=512, verbose_name=u"道具,字典 字符串 格式")
    create_time = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())
    delete_status = IntField(verbose_name=u"是否删除", choices=Delete_STATUS)
    start_time = DateTimeField(verbose_name=u"起始时间(包含在内)")
    end_time = DateTimeField(verbose_name=u"结束时间(包含在内)")
    start_hms = StringField(verbose_name=u"起始的时分秒时间段 如: 08:25:00", max_length=32)
    end_hms = StringField(verbose_name=u"结束的时分秒时间段 如: 08:25:00", max_length=32)
    role = StringField(verbose_name=u"人群",  max_length=256)  #1: 新主播 2：老主播 3：用户(多个逗号分隔)


class ToolsActivityRecord(Document):
    date_time = DateTimeField(verbose_name=u"创建时间")
    tools_activity_id = StringField(max_length=64, verbose_name=u"道具活动id")
    user_id = IntField(verbose_name=u'用户id', required=True)






