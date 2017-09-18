# coding=utf-8

from django.db import models

from mongoengine import *
from base.settings import CHATPAMONGO


class Task(Document):
    IDENTITY = {
        # 播主
        1: u"新手任务",
        2: u"完善资料",
        3: u"上传头像",
        4: u"上传普通照片",
        5: u"添加签名",
        6: u"添加标签",
        7: u"上传精华照",
        8: u"每日认证",
        9: u"转发QQ",
        10: u"转发微信",
        11: u"转发朋友圈",
        12: u"使用道具",
        13: u"使用漂流瓶",
        14: u"使用千里眼",
        15: u"发布私房视频",
        18: u"成长任务",
        19: u"完成新手任务",
        20: u"视频通话50",
        21: u"视频通话100",
        22: u"视频通话500",
        23: u"视频通话1000",
        24: u"魅力值500",
        25: u"魅力值1000",
        26: u"魅力值5000",
        27: u"魅力值10000",

        # 男用户
        28: u"新手任务",
        29: u"完善资料",
        30: u"上传头像",
        31: u"上传普通照片",
        32: u"添加签名",
        33: u"添加标签",
        34: u"观看精华照",
        35: u"首次充值",
        36: u"每日任务",
        37: u"转发QQ",
        38: u"转发微信",
        39: u"转发朋友圈",
        40: u"使用道具",
        41: u"使用門禁卡",
        42: u"使用漂流瓶",
        43: u"观看2个私房视频",

        # 女用户
        44: u"新手任务",
        45: u"完善资料",
        46: u"上传头像",
        47: u"上传普通照片",
        48: u"添加签名",
        49: u"添加标签",
        50: u"认证视频播主",
        51: u"每日任务",
        52: u"转发QQ",
        53: u"转发微信",
        54: u"转发朋友圈"
    }

    GO_TYPE = {
        1: u"上传头像",
        2: u"上传普通照片",
        3: u"添加签名",
        4: u"添加标签",
        5: u"使用漂流瓶",
        6: u"使用千里眼",
        7: u"使用门禁卡",
        8: u"发布私房视频",
        9: u"转发QQ",
        10: u"转发微信",
        11: u"转发朋友圈",
        12: u"观看精华照片",
        13: u"观看2个私房视频",
        14: u"首次充值",
        15: u"认证视频播主",
        16: u"上传精华照片",
    }
    name = StringField(verbose_name=u"任务名称", max_length=32)
    pid = StringField(verbose_name=u"父id")
    identity = IntField(verbose_name=u"任务序列")
    level = IntField(verbose_name=u"层级")
    reward_type = IntField(verbose_name=u"奖励类型")  # 1:金币  2:钻石
    reward_count = IntField(verbose_name=u"奖励数量")
    role = IntField(verbose_name=u"任务所属角色")  # 1:男用户 2:女用户 3:播主
    go_type = IntField(verbose_name=u"前往类型")
    is_valid = IntField(verbose_name=u"是否可用")  # 1:可用 2:不可用
    order = IntField(verbose_name=u"排序")

    @classmethod
    def get_list(cls, role, user_id):
        task_list = cls.objects.filter(is_valid=1, role=1, level=1).order_by("order")
        data = []
        for task in task_list:
            if int(role) != 3:
                id = str(task.id)
                dic = Task.normal_info(task)
                dic["data"] = []
                p2_list = cls.objects.filter(pid=id, is_valid=1, role=1).order_by("order")
                for t2 in p2_list:
                    p2_dic = Task.normal_info(t2)
                    p2_dic["data"] = []
                    p3_list = cls.objects.filter(pid=str(t2.id), is_valid=1, role=1).order_by("order")

                    if not p3_list:
                        # 只有二级任务
                        UserTaskRecord.objects.filter(task_id=str(t2.id), user_id=user_id).first()

                    if p3_list:
                        for t3 in p3_list:
                            p3_dic = Task.normal_info(t3)
                            p2_dic["data"].append(p3_dic)

                    dic["data"].append(p2_dic)
                data.append(dic)
            else:
                # 成长任务:
                pass

        return data

    def normal_info(self):
        if not self.go_type:
            go_type = 0
        else:
            go_type = self.go_type
        return {
            "id": str(self.id),
            "name": self.name,
            "identity": self.identity,
            "level": self.level,
            "reward_type": self.reward_type,
            "reward_count": self.reward_count,
            "role": self.role,
            "go_type": go_type
        }


class UserTaskRecord(Document):
    task_id = StringField(verbose_name=u"任务id")
    user_id = IntField(verbose_name=u"用户id")
    create_time = DateTimeField(verbose_name=u"创建时间")
    finish_type = IntField(verbose_name=u"完成状态")  # 1:待领取  2:已完成
