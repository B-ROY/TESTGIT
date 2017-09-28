# coding=utf-8
from django.db import models
from mongoengine import *
import logging
import datetime
from base.settings import CHATPAMONGO
from app.customer.models.tools import Tools, UserTools
from app.customer.models.account import Account, TradeDiamondRecord, TradeGoldRecord
from app.customer.models.user import User

connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class Shop(Document):
    IDENTITY = {
        0: "门禁卡",
        1: "漂流瓶",
        2: "千里眼",
        3: "观影券",
        4: "观影碎片",
        5: "1天vip",
        50000: "钻石",
        50001: "金币"
    }
    goods_name = StringField(verbose_name=u"商品名称")
    goods_identity = IntField(verbose_name=u"商品标识")
    goods_num = IntField(verbose_name=u"商品数量")
    goods_price = IntField(verbose_name=u"商品价格")
    is_limit = IntField(verbose_name=u"是否限购")  # 1、限购 2、不限购
    goods_desc = StringField(verbose_name=u"商品描述")
    goods_type = IntField(verbose_name=u"商品类型")  # 1、钻石 2、红包
    status = IntField(verbose_name=u"状态")  # 1、可用 2、不可用

    def normal_info(self):
        data = {
            "id": str(self.id),
            "goods_name": self.goods_name,
            "goods_identity": self.goods_identity,
            "goods_num": self.goods_num,
            "goods_price": self.goods_price,
            "is_limit": self.is_limit,
            "goods_desc": self.goods_desc,
            "goods_type": self.goods_type
        }

        type_dict = {}
        tools_list = Tools.objects.all()
        for tools in tools_list:
            type_dict[int(tools.tools_type)] = tools

        if int(self.goods_identity) in type_dict:
            tools = type_dict[int(self.goods_identity)]
            data["tool_icon_url"] = tools.icon_url

        return data

    @classmethod
    def buy_goods(cls, user_id, goods, goods_count):
        code = 1
        error = ""

        user = User.objects.filter(id=user_id).first()
        if not user:
            code = -1
            error = u"错误用户"

        type_dict = {}
        tools_list = Tools.objects.all()
        for tools in tools_list:
            type_dict[int(tools.tools_type)] = tools

        goods_type = goods.goods_type  # 1:钻石  2:红包
        goods_identity = int(goods.goods_identity)
        if goods_identity in type_dict:
            # 道具
            tools = type_dict[goods_identity]
            if goods_type == 1:
                # 钻石购买
                status, message = UserTools.buy_tools(user_id, str(tools.id), goods_count)
                if status != 200:
                    code = status
                    error = message

            elif goods_type == 2:
                pass
                # return

        else:
            # 金币,  钻石 或者其他
            account = Account.objects.filter(user=user).first()
            if goods_type == 1:
                # 钻石商城
                if goods_identity == 50001:
                    # 钻石购买金币
                    account.diamond_trade_out(goods_count * goods.goods_price, u"钻石购买金币", TradeDiamondRecord.TradeTypeBuyGold)
                    account.gold_trade_in(goods_count * goods.goods_num, u"钻石购买金币", TradeGoldRecord.TypeDiamondBuy)
            elif goods_type == 2:
                # 红包商城
                pass
                # return

        return code, error


