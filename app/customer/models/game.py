# coding=utf-8

from django.db import models
import logging
import datetime
from wi_model_util.imodel import *
from mongoengine import *
from base.settings import CHATPAMONGO
from app.customer.models.user import User
from app.customer.models.vip import UserVip, Vip
from app.customer.models.task import UserTaskRecord
from app.customer.models.account import Account, TradeDiamondRecord, TradeGoldRecord
from app.customer.models.tools import UserTools, Tools
from app.customer.models.community import UserMoment
from api.settings import ConstantKey


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class TurnTable(Document):
    TYPE = {
        50000: u"钻石",
        50002: u"经验",
        50001: u"金币",
        0: u"门禁卡",
        1: u"漂流瓶",
        2: u"千里眼",
        5: u"一天VIP",
        3: u"观影券",
        4: u"观影碎片",
        50003: u"很遗憾",
    }
    id = IntField(verbose_name=u'id', primary_key=True)
    name = StringField(max_length=32, verbose_name=u'名称')
    logo_url = StringField(verbose_name=u"图片logo", max_length=512)
    type = IntField(verbose_name=u"物品类型")
    count = IntField(verbose_name=u"物品个数")
    is_share = IntField(verbose_name=u"物品个数")  # 1:分享  2:不分享
    delete_status = IntField(verbose_name=u"是否删除")  # 1:未删除 2:删除
    num = IntField(verbose_name=u"份数(总数为1000)")
    created_time = DateTimeField(verbose_name=u"添加时间")
    level = IntField(verbose_name=u"奖品等级")
    share_content = StringField(verbose_name=u"分享文案")

    class Meta:
        app_label = "customer"
        verbose_name = u"转盘游戏"

    def normal_info(self):
        data = {
            "id": self.id,
            "name": self.name,
            "logo_url": self.logo_url,
            "type": self.type,
            "count": self.count,
            "is_share": self.is_share,
        }
        if self.level:
            data["level"] = self.level

        return data

    @classmethod
    def get_list(cls):
        import random
        turn_table_list = cls.objects.filter(delete_status=1)
        list = []
        for turn_table in turn_table_list:
            list.append(turn_table)
        random.shuffle(list)
        return list

    @classmethod
    def save_reward(cls, reward_id, user, reward_type, price):
        turn_table = cls.objects.filter(id=reward_id).first()
        type = turn_table.type
        account = Account.objects.filter(user=user).first()
        type_list = [50000, 50001, 50002, 50003]
        types = Tools.objects.all().distinct("tools_type")

        if reward_type == 2:
            # 消耗金币
            account.gold_trade_out(price, u"大转盘抽奖消耗", TradeGoldRecord.TypeLuckDrawConsume)
        for t in types:
            type_list.append(t)
        if type not in [50000, 50001, 50002, 50003, 0, 1, 2, 3, 4, 5]:
            return
        if type in [0, 1, 2, 3, 4]:
            # 存入道具
            tool = Tools.objects.filter(tools_type=type).first()
            UserTools.give_tools(user.id, str(tool.id), turn_table.count)
        elif type == 50000:
            # 钻石
            account.diamond_trade_in(turn_table.count, 0, u"大转盘抽奖", TradeDiamondRecord.TradeTypeLuckDraw)

        elif type == 50001:
            # 金币
            account.gold_trade_in(turn_table.count, u"大转盘抽奖", TradeGoldRecord.TypeReward)

        UserTurnTableRecord.create_record(user.id, reward_type)


    @classmethod
    def create(cls, id, name, logo_url, type, count, is_share, num, delete_status, share_content, level=None):
        obj_ = cls()
        obj_.id = id
        obj_.name = name
        obj_.logo_url = logo_url
        obj_.type = type
        obj_.count = count
        obj_.is_share = is_share
        obj_.delete_status = delete_status
        if level:
            obj_.level = level
        obj_.share_content = share_content
        obj_.num = num
        obj_.created_time = datetime.datetime.now()
        obj_.save()

    @classmethod
    def get_reward_id(cls):
        tables = TurnTable.objects.all()
        obj_list = []
        for table in tables:
            data = (table.id, table.num)
            obj_list.append(data)

        id = WeightRandom(obj_list)
        return id()

    @classmethod
    def get_user_count(cls, user_id):
        now = datetime.datetime.now()
        startime = now.strftime("%Y-%m-%d 00:00:00")
        endtime = now.strftime('%Y-%m-%d 23:59:59')

        free_total_count = cls.get_free_total_count(user_id)
        gold_total_count = ConstantKey.TurnTable_Gold_Count

        free_used_count = 0
        gold_used_count = 0
        share_used_count = 0
        can_share = 1

        free_upper_limit = free_total_count + 3

        create_time = now.strftime("%Y-%m-%d")

        records = UserTurnTableRecord.objects.filter(user_id=user_id, create_time=create_time)
        if records:
            for record in records:
                count = record.count
                if record.type == 1:
                    free_used_count = count
                if record.type == 2:
                    gold_used_count = count
                if record.type == 3:
                    share_used_count = count

        task_count = UserTaskRecord.objects.filter(user_id=user_id, reward_type=3, finish_type=2,
                                                   create_time__gte=startime, create_time__lte=endtime).count()

        if task_count > 0:
            # 说明已经有过分享, 可以使用.
            free_total_count += task_count
            free_used_count += share_used_count

        if task_count >= ConstantKey.TurnTable_Share_Count:
            can_share = 0

        return free_used_count, free_total_count, gold_used_count, gold_total_count, free_upper_limit, can_share

    @classmethod
    def get_free_total_count(cls, user_id):
        user = User.objects.filter(id=user_id).first()
        if not user:
            return 0
        user_vip = UserVip.objects.filter(user_id=user.id).first()
        if user_vip:
            vip = Vip.objects.filter(id=user_vip.vip_id).first()
            if vip.vip_type == 1:
                return 6
            elif vip.vip_type == 2:
                return 9
        else:
            return 3

    @classmethod
    def check_is_can(cls, type, user_id, price):
        #  type  1:免费  2:金币
        user = User.objects.filter(id=user_id).first()
        account = Account.objects.filter(user=user).first()
        gold = 0
        is_can = 1
        error = u""

        free_used_count = 0
        gold_used_count = 0
        share_used_count = 0

        now = datetime.datetime.now()
        startime = now.strftime("%Y-%m-%d 00:00:00")
        endtime = now.strftime('%Y-%m-%d 23:59:59')
        create_time = now.strftime("%Y-%m-%d")

        free_total_count = cls.get_free_total_count(user_id)
        records = UserTurnTableRecord.objects.filter(user_id=user_id, create_time=create_time)
        if records:
            for record in records:
                count = record.count
                if record.type == 1:
                    free_used_count = count
                if record.type == 2:
                    gold_used_count = count
                if record.type == 3:
                    share_used_count = count

        if account.gold:
            gold = account.gold
        if type == 2:
            if gold < price:
                is_can = 3  # 金币不足
                error = u"金币不足"
            if gold_used_count >= 3:
                is_can = 4  # 金币次数到达上限
                error = u"金币次数到达上限"
        elif type == 1:
            task_count = UserTaskRecord.objects.filter(user_id=user_id, reward_type=3, finish_type=2,
                                                       create_time__gte=startime, create_time__lte=endtime).count()

            if free_used_count >= free_total_count:
                if task_count == 0:
                    is_can = 2  # 分享可获得
                    error = u"分享可获得免费抽奖机会"
                else:
                    if task_count == share_used_count:
                        if task_count < 3:
                            is_can = 2
                            error = u"分享可获得免费抽奖机会"
                        else:
                            is_can = 5  # 免费次数已用完
                            error = u"免费次数已用完"
        return is_can, error

    @classmethod
    def share_moment(cls, user_id, turn_table_id, picture_urls):
        turn_table = cls.objects.filter(id=turn_table_id).first()
        if not turn_table:
            return

        if turn_table.is_share == 2:
            return

        user_moment = UserMoment()
        user_moment.user_id = user_id
        user_moment.like_count = 0
        user_moment.like_user_list = []
        user_moment.comment_count = 0
        picture_url_list = picture_urls.split(',')
        if picture_url_list:
            for picture_url in picture_url_list:
                if picture_url:
                    pic_url = User.convert_http_to_https(picture_url)
                    dict = {
                        "url": pic_url,
                        "status": 1
                    }
                    user_moment.img_list.append(dict)
        user_moment.content = turn_table.share_content
        user_moment.show_status = 1
        user_moment.delete_status = 1
        user_moment.ispass = 2
        user_moment.type = 5
        user_moment.is_public = 1
        user_moment.create_time = datetime.datetime.now()
        user_moment.save()


class UserTurnTableRecord(Document):
    user_id = IntField(verbose_name=u"用户id")
    create_time = StringField(verbose_name=u"操作日期", max_length=64)  # %Y-%m-%d
    count = IntField(verbose_name=u"次数")
    type = IntField(verbose_name=u"类型")  # 1:免费  2:使用金币  3:分享

    @classmethod
    def create_record(cls, user_id, type):
        now = datetime.datetime.now()
        create_time = now.strftime("%Y-%m-%d")
        if type == 1:
            # 判断是 用户每日免费 还是分享后的免费
            free_total_count = TurnTable.get_free_total_count(user_id)
            record = cls.objects.filter(user_id=user_id, type=1, create_time=create_time).first()
            if not record:
                cls.create(user_id, create_time, 1, 1)
            else:
                used_count = record.count
                if used_count < free_total_count:
                    # 每日免费次数充足
                    record.update(inc__count=1)
                else:
                    # 每日免费次数已经用完
                    share_record = cls.objects.filter(user_id=user_id, type=3, create_time=create_time).first()
                    if not share_record:
                        cls.create(user_id, create_time, 1, 3)
                    else:
                        share_record.update(inc__count=1)

        elif type == 2:
            record = cls.objects.filter(user_id=user_id, type=type, create_time=create_time).first()
            if not record:
                cls.create(user_id, create_time, 1, 2)
            else:
                record.update(inc__count=1)

    @classmethod
    def create(cls, user_id, create_time, count, type):
        _obj = cls()
        _obj.user_id = user_id
        _obj.create_time = create_time
        _obj.count = count
        _obj.type = type
        _obj.save()


class WeightRandom:
    def __init__(self, items):
        weights = [w for _, w in items]
        self.goods = [x for x, _ in items]
        self.total = sum(weights)
        self.acc = list(self.accumulate(weights))

    def accumulate(self, weights):
        cur = 0
        for w in weights:
            cur = cur+w
            yield cur

    def __call__(self):
        import bisect
        import random
        return self.goods[bisect.bisect_right(self.acc, random.uniform(0, self.total))]


