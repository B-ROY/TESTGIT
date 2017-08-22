# coding=utf-8

from django.db import models

from mongoengine import *
from base.settings import CHATPAMONGO


class CharmRank(Document):
    CHANGE = [
        (0, u"不变"),
        (1, u"上升"),
        (2, u"下降"),

    ]
    user = GenericReferenceField("User", verbose_name=u'用户')
    charm = IntField(verbose_name=u"主播近三天魅力值")
    change_status = IntField(verbose_name=u"较上次位置变化情况")
    type = IntField(verbose_name=u"榜单类型")  # 1:周榜  2:日榜

    rank = IntField(verbose_name=u"当前排名", default=0)

    @classmethod
    def get_rank_list(self, interval, count):
        charm_rank_list = CharmRank.objects.filter(rank__lte=count)

        return charm_rank_list

    @classmethod
    def get_rank_list2(self, interval, count, type):
        charm_rank_list = CharmRank.objects.filter(rank__lte=count, type=int(type)).order_by("rank")

        return charm_rank_list


class WealthRank(Document):
    CHANGE = [
        (0, u"不变"),
        (1, u"上升"),
        (2, u"下降"),

    ]
    user = GenericReferenceField("User", verbose_name=u'用户')
    wealth = IntField(verbose_name=u"用户近三天财富值")
    change_status = IntField(verbose_name=u"较上次位置变化情况")
    rank = IntField(verbose_name=u"当前排名")
    type = IntField(verbose_name=u"榜单类型")  # 1:周榜  2:日榜


    @classmethod
    def get_rank_list(self, interval, count):
        wealth_rank_list = WealthRank.objects.filter(rank__lte=count)

        return wealth_rank_list

    @classmethod
    def get_rank_list2(self, interval, count, type):
        wealth_rank_list = WealthRank.objects.filter(rank__lte=count, type=type).order_by("rank")

        return wealth_rank_list


class InviteRank(Document):
    """
    用于5月13日--5月26日活动：显示邀请人数前五的用户 
    """
    head_image = StringField(verbose_name=u"用户头像")
    nickname = StringField(verbose_name=u"用户昵称")
    uid = IntField(verbose_name=u"用户长id")
    invite_num = IntField(verbose_name=u"邀请人数")
    rank = IntField(verbose_name=u"邀请排行")


    @classmethod
    def get_top_5(cls):
        return InviteRank.objects.all()


class InviteRankTwo(Document):
    """
        用于5月20日--5月26日活动：显示邀请人数前五的用户 
    """
    head_image = StringField(verbose_name=u"用户头像")
    nickname = StringField(verbose_name=u"用户昵称")
    uid = IntField(verbose_name=u"用户长id")
    invite_num = IntField(verbose_name=u"邀请人数")
    rank = IntField(verbose_name=u"邀请排行")

    @classmethod
    def get_top_5(cls):
        return InviteRankTwo.objects.all()


class NewAnchorRank(Document):
    """
    新人驾到 列表
    """
    user_id = IntField(verbose_name=u"用户id")


class ClairvoyantRank(Document):
    user_id = IntField(verbose_name=u"用户id")