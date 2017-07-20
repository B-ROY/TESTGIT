# coding=utf-8

import datetime
import logging

from base.settings import CHATPAMONGO
from django.conf import settings
from mongoengine import *
from app.customer.models.user import *
from app.customer.models.tools import *
from app.customer.models.vip import *


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class FirstChargeActivity(Document):
    temp_activity_type = IntField(verbose_name=u"活动类型")
    name = StringField(max_length=32, verbose_name=u'活动名称')
    recharge_min = IntField(verbose_name=u"最小充值金额")
    recharge_max = IntField(verbose_name=u"最大充值金额")
    tool_data = StringField(verbose_name=u"道具 数据")
    vip_data = StringField(verbose_name=u"vip 数据")
    create_time = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())
    end_time = DateTimeField(verbose_name=u"截止时间")
    is_valid = IntField(verbose_name=u'是否有效', default = 1)  # 1有效 0 无效

    @classmethod
    def create_reward(cls, user, money):
        user_id = user.id
        now = datetime.datetime.now()
        yuan_money = int(money/100)
        activity = FirstChargeActivity.objects.filter(temp_activity_type=1, recharge_min__lte=money,
                                                      recharge_max__gt=money, is_valid=1).first()
        if not activity:
            max_act = FirstChargeActivity.objects.filter(temp_activity_type=1, is_valid=1, recharge_min=None).order_by("-recharge_max").first()
            max_recharge = max_act.recharge_max
            if max_recharge <= money:
                activity = max_act

        tool_data = activity.tool_data
        tool_dic = None
        vip_data = activity.vip_data
        vip_dic = None

        if tool_data:
            tool_dic = eval(tool_data)
        if vip_data:
            vip_dic = eval(vip_data)

        # 发放奖励
        if tool_dic:
            for key, value in tool_dic.items():
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
                tools_record.oper_type = 6
                tools_record.create_time = now
                tools_record.save()

        if vip_dic:
            vip_name = ""
            start_time = ""
            end_time = ""
            for key, value in vip_dic.items():
                print key
                print value
                vip = Vip.objects.filter(vip_type=int(key), is_valid=1).first()
                if int(key) == 1:
                    vip_name = "高级"
                elif int(key) == 2:
                    vip_name = "超级"
                user_vip = UserVip.objects.filter(user_id=user_id).first()
                vip_id = str(vip.id)
                now = datetime.datetime.now()
                days = 30 * int(value) + 1
                print days, "days==="
                if user_vip:
                    user_vip.vip_id = vip_id
                    end_time = user_vip.end_time + datetime.timedelta(days=days)
                else:
                    user_vip = UserVip()
                    user_vip.user_id = user_id
                    user_vip.vip_id = vip_id
                    user_vip.create_time = now
                    end_time = now + datetime.timedelta(days=days)
                user_vip.end_time = end_time
                user_vip.save()
                start_time = user_vip.create_time.strftime('%Y年%m月%d日')
                end_time = user_vip.end_time.strftime('%Y年%m月%d日')
            desc = u"<html><p>" + _(u"亲的的用户，充值金额%s元，活动奖励已到账、赠送%sVIP已开启，有效时间为%s-%s，祝您玩的开心，聊得愉快") % (unicode(yuan_money), vip_name, start_time, end_time ) + u"</p></html>"
        else:
            desc = u"<html><p>" + _(u"亲爱的用户，充值金额%s元，活动奖励已发放到您的账户中，请注意查收哦~祝您玩的开心，聊得愉快") % unicode(yuan_money) + u"</p></html>"
        # MessageSender.send_system_message(user_id, desc)
        print desc, "======================="


    @classmethod
    def update(cls):
        activity_list = FirstChargeActivity.objects.filter(temp_activity_type=1, is_valid=1)
        now = datetime.datetime.now()
        end_time = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(days=31)
        for activity in activity_list:
            activity.end_time = end_time
            activity.save()

    @classmethod
    def init(cls):
        act1 = FirstChargeActivity()
        act1.temp_activity_type = 1
        act1.name = "财神驾到(首充)"
        tool_dic1 = {
            "0": "10"
        }
        act1.recharge_min = 100
        act1.recharge_max = 5000
        act1.tool_data = str(tool_dic1)
        act1.create_time = datetime.datetime.now()
        act1.is_valid = 1
        act1.save()

        act2 = FirstChargeActivity()
        act2.temp_activity_type = 1
        act2.name = "财神驾到(首充)"
        tool_dic2 = {
            "0": "10",
            "1": "5"
        }
        act2.recharge_min = 5000
        act2.recharge_max = 10000
        act2.tool_data = str(tool_dic2)
        act2.create_time = datetime.datetime.now()
        act2.is_valid = 1
        act2.save()

        act3 = FirstChargeActivity()
        act3.temp_activity_type = 1
        act3.name = "财神驾到(首充)"
        tool_dic3 = {
            "0": "5",
            "1": "5",
            "2": "5"
        }
        act3.recharge_min = 10000
        act3.recharge_max = 50000
        act3.tool_data = str(tool_dic3)
        act3.create_time = datetime.datetime.now()
        act3.is_valid = 1
        act3.save()

        act4 = FirstChargeActivity()
        act4.temp_activity_type = 1
        act4.name = "财神驾到(首充)"
        tool_dic4 = {
            "0": "5",
            "1": "5"
        }
        vip_dic4 = {
            "2": "1"
        }
        act4.recharge_min = 50000
        act4.recharge_max = 100000
        act4.tool_data = str(tool_dic4)
        act4.vip_data = str(vip_dic4)
        act4.create_time = datetime.datetime.now()
        act4.is_valid = 1
        act4.save()

        act5 = FirstChargeActivity()
        act5.temp_activity_type = 1
        act5.name = "财神驾到(首充)"
        tool_dic5 = {
            "0": "10",
            "1": "5",
            "2": "5"
        }
        vip_dic5 = {
            "2": "2"
        }

        act5.recharge_max = 100000
        act5.tool_data = str(tool_dic5)
        act5.vip_data = str(vip_dic5)
        act5.create_time = datetime.datetime.now()
        act5.is_valid = 1
        act5.save()

        cls.update()

