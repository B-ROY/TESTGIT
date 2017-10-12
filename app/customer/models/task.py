# coding=utf-8

from django.db import models

from mongoengine import *
from base.settings import CHATPAMONGO
from app.customer.models.user import User
import datetime


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
        8: u"每日任务",
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
    reward_type = IntField(verbose_name=u"奖励类型")  # 1:金币  2:钻石  3:转盘抽奖机会
    reward_count = IntField(verbose_name=u"奖励数量")
    role = IntField(verbose_name=u"任务所属角色")  # 1:男用户 2:女用户 3:播主
    go_type = IntField(verbose_name=u"前往类型")
    is_valid = IntField(verbose_name=u"是否可用")  # 1:可用 2:不可用
    order = IntField(verbose_name=u"排序")
    is_day_task = IntField(verbose_name=u"是否是每日任务(只需标记顶级任务)")  # 1:是
    grow_task_type = IntField(verbose_name=u"成长任务类型")  # 1:完成新手任务  2:通话时长  3: 魅力值

    @classmethod
    def get_list(cls, user_id):
        user = User.objects.filter(id=user_id).first()
        role = 1
        novice_task = 28
        day_task = 36
        if user.is_video_auth == 1:
            # 播主
            role = 3
            novice_task = 1
            day_task = 8
        else:
            if user.gender == 2:
                role = 2
                novice_task = 44
                day_task = 51

        task_list = cls.objects.filter(is_valid=1, role=role, level=1).order_by("order")
        novice_data = None
        day_data = None
        anchor_data = None

        for task in task_list:
            identity = task.identity
            id = str(task.id)
            if identity != 18:
                dic = Task.normal_info(task)
                dic["data"] = []
                p2_list = cls.objects.filter(pid=id, is_valid=1, role=role).order_by("order")
                now = datetime.datetime.now()
                starttime = now.strftime("%Y-%m-%d 00:00:00")
                endtime = now.strftime('%Y-%m-%d 23:59:59')
                for t2 in p2_list:
                    p2_dic = Task.normal_info(t2)
                    p2_dic["data"] = []
                    p3_list = cls.objects.filter(pid=str(t2.id), is_valid=1, role=role).order_by("order")

                    if task.is_day_task and task.is_day_task == 1:
                        record = UserTaskRecord.objects.filter(task_id=str(t2.id), user_id=user_id,
                                                               create_time__gte=starttime, create_time__lte=endtime).first()
                    else:
                        record = UserTaskRecord.objects.filter(task_id=str(t2.id), user_id=user_id).first()

                    if not p3_list:
                        # 只有二级任务
                        total = 1
                        finish_count = 0
                        if record:
                            finish_count = 1
                    else:
                        total = 0
                        finish_count = 0
                        for t3 in p3_list:
                            p3_dic = Task.normal_info(t3)
                            p2_dic["data"].append(p3_dic)
                            p3_tid = str(t3.id)
                            total += 1

                            if task.is_day_task and task.is_day_task == 1:
                                record = UserTaskRecord.objects.filter(task_id=p3_tid, user_id=user_id,
                                                    create_time__gte=starttime, create_time__lte=endtime).first()
                            else:
                                record = UserTaskRecord.objects.filter(task_id=p3_tid, user_id=user_id).first()
                            if record:
                                p3_dic["finish_type"] = 2
                                finish_count += 1
                            else:
                                p3_dic["finish_type"] = 0

                    if not record:
                        p2_dic["finish_type"] = 0
                    else:
                        finish_type = record.finish_type
                        p2_dic["finish_type"] = finish_type
                        # if finish_type == 2:
                        # finish_count += 1

                    p2_dic["total"] = total
                    p2_dic["finish_count"] = finish_count

                    if record and record.finish_type == 1:
                        p2_dic["record_id"] = str(record.id)

                    dic["data"].append(p2_dic)

                if identity == novice_task:
                    # 新手任务
                    novice_data = dic
                elif identity == day_task:
                    day_data = dic
            else:
                # 成长任务:
                dic = Task.normal_info(task)
                dic["data"] = []
                tasks = Task.objects.filter(pid=id, is_valid=1).order_by("sort")
                grow_type_list = []   # 1:完成新手任务 2:视频时长  3:魅力值
                for t in tasks:
                    if t.grow_task_type not in grow_type_list:
                        grow_type_list.append(t.grow_task_type)

                video_task_list = Task.objects.filter(pid=id, is_valid=1, grow_task_type=2).order_by("-reward_count")
                video_task_ids = []
                video_count = 1
                min_video_task = None
                max_video_task = None
                task_len = len(video_task_list)
                for video_task in video_task_list:
                    video_task_ids.append(str(video_task.id))
                    if video_count == 1:
                        max_video_task = video_task
                    if video_count == task_len:
                        min_video_task = video_task
                    video_count += 1

                charm_task_list = Task.objects.filter(pid=id, is_valid=1, grow_task_type=3).order_by("reward_count")
                charm_task_ids = []
                charm_count = 1
                charm_task_len = len(charm_task_list)
                for charm_task in charm_task_list:
                    charm_task_ids.append(str(charm_task.id))
                    if charm_count == 1:
                        min_charm_task = charm_task
                    if charm_count == charm_task_len:
                        max_charm_task = charm_task
                    charm_count += 1

                for grow_type in grow_type_list:
                    p2_dic = {}
                    if grow_type == 1:
                        t = Task.objects.filter(identity=19).first()
                        record = UserTaskRecord.objects.filter(user_id=user_id, task_id=str(t.id)).first()
                        finish_count = 0
                        p2_dic = Task.normal_info(t)
                        if record:
                            finish_type = record.finish_type
                            p2_dic["finish_type"] = finish_type
                            # if finish_type == 2:
                            finish_count += 1

                            if record.finish_type == 1:
                                p2_dic["record_id"] = str(record.id)

                        p2_dic["total"] = 1
                        p2_dic["finish_count"] = finish_count
                    elif grow_type == 2:
                        time_len = 1
                        if user.video_time:
                            time_len = (user.video_time/60) + 1  # 分钟

                        # 当前通话时长任务进度
                        record = UserTaskRecord.objects.filter(task_id__in=video_task_ids,
                                                               user_id=user_id).order_by("-create_time").first()
                        if not record:
                            name = min_video_task.name.split(",")[0]
                            total = int(min_video_task.name.split(",")[1])
                            p2_dic = Task.normal_info(min_video_task)
                            p2_dic["name"] = name
                            p2_dic["total"] = total
                            if time_len > total:
                                p2_dic["finish_type"] = 1
                            else:
                                p2_dic["finish_type"] = 0
                            p2_dic["finish_count"] = time_len
                        else:
                            task_id = record.task_id
                            t = Task.objects.filter(id=task_id).first()
                            name = t.name.split(",")[0]
                            total = int(t.name.split(",")[1])
                            p2_dic = Task.normal_info(t)
                            if record.finish_type == 1:  # 待领取
                                p2_dic["name"] = name
                                p2_dic["total"] = total
                                p2_dic["finish_count"] = time_len
                                p2_dic["finish_type"] = record.finish_type
                                if record.finish_type == 1:
                                    p2_dic["record_id"] = str(record.id)
                            else:
                                # 已完成. 判断是不是最高的已经领取. 如果不是.显示领取过的下一个成长阶段
                                if task_id == str(max_video_task.id):
                                    p2_dic["name"] = name
                                    p2_dic["total"] = int(max_video_task.name.split(",")[1])
                                    p2_dic["finish_count"] = time_len
                                    p2_dic["finish_type"] = record.finish_type
                                else:
                                    new_task = Task.objects.filter(reward_count__gt=t.reward_count).order_by("reward_count").first()
                                    total = int(new_task.name.split(",")[1])
                                    p2_dic["name"] = name
                                    p2_dic["total"] = total
                                    p2_dic["finish_count"] = time_len
                                    if time_len > total:
                                        p2_dic["finish_type"] = 1
                                    else:
                                        p2_dic["finish_type"] = 0

                    elif grow_type == 3:
                        # 魅力值
                        user_charm = 0
                        if user.charm_value:
                            user_charm = user.charm_value

                        # 当前魅力值任务进度
                        record = UserTaskRecord.objects.filter(task_id__in=charm_task_ids,
                                                               user_id=user_id).order_by("-create_time").first()

                        if not record:
                            name = min_charm_task.name.split(",")[0]
                            total = int(min_charm_task.name.split(",")[1])
                            p2_dic = Task.normal_info(min_charm_task)
                            p2_dic["name"] = name
                            p2_dic["total"] = total
                            p2_dic["finish_type"] = 0
                            p2_dic["finish_count"] = user_charm
                        else:
                            task_id = str(record.task_id)
                            t = Task.objects.filter(id=task_id).first()
                            name = t.name.split(",")[0]
                            total = int(t.name.split(",")[1])
                            p2_dic = Task.normal_info(t)
                            if record.finish_type == 1:  # 待领取
                                p2_dic["name"] = name
                                p2_dic["total"] = total
                                p2_dic["finish_count"] = user_charm
                                p2_dic["finish_type"] = record.finish_type
                                if record.finish_type == 1:
                                    p2_dic["record_id"] = str(record.id)
                            else:
                                # 已完成. 判断是不是最高的已经领取. 如果不是.显示领取过的下一个成长阶段
                                if task_id == str(max_charm_task.id):
                                    p2_dic["name"] = name
                                    p2_dic["total"] = int(max_charm_task.name.split(",")[1])
                                    p2_dic["finish_count"] = user_charm
                                    p2_dic["finish_type"] = record.finish_type
                                else:
                                    new_task = Task.objects.filter(reward_count__gt=t.reward_count).order_by("reward_count").first()
                                    total = int(new_task.name.split(",")[1])
                                    p2_dic["name"] = name
                                    p2_dic["total"] = total
                                    p2_dic["finish_count"] = user_charm
                                    p2_dic["finish_type"] = 0
                    # 添加到成长任务
                    dic["data"].append(p2_dic)
                    anchor_data = dic

        return novice_data, day_data, anchor_data

    def normal_info(self):
        if not self.go_type:
            go_type = 0
        else:
            go_type = self.go_type
        return {
            "name": self.name,
            "identity": self.identity,
            "level": self.level,
            "reward_type": self.reward_type,
            "reward_count": self.reward_count,
            "go_type": go_type
        }

    @classmethod
    def get_day_task(cls, task):
        if task.pid:
            task = Task.objects.filter(id=task.pid).first()
            return cls.get_day_task(task)
        else:
            if task.is_day_task:
                return task.is_day_task
            else:
                return 0


    @classmethod
    def get_role(cls, user_id):
        user = User.objects.filter(id=user_id).first()
        role = 1
        if user.is_video_auth == 1:
            # 播主
            role = 3
        else:
            if user.gender == 2:
                role = 2

        return role

    # 任务完成 领取
    @classmethod
    def finish_task(cls, user, record_id):
        from app.customer.models.account import Account, TradeGoldRecord, TradeDiamondRecord
        user_id = user.id
        code = 1
        error = ""
        record = UserTaskRecord.objects.filter(id=record_id).first()
        task = Task.objects.filter(id=record.task_id).first()
        if not record or not task:
            code = -1
            error = "数据错误"
            return code, error

        # 如果领取的是新手任务, 判断所有新手任务完成.  成长任务是需要: 完成新手任务的
        novice_task = 28
        if user.is_video_auth == 1:
            # 播主
            novice_task = 1
        else:
            if user.gender == 2:
                novice_task = 44
        top_task = Task.objects.filter(identity=novice_task).first()
        now = datetime.datetime.now()

        # 新手任务
        if task.pid == str(top_task):
            level_2_list = []
            total_count = 0
            total_tasks = Task.objects.filter(pid=top_task.id)
            for total_task in total_tasks:
                level_2_list.append(str(total_task.id))
                total_count += 1

            # 新手任务下二级任务完成个数)
            finish_count = UserTaskRecord.objects.filter(user_id=user_id, task_id__in=level_2_list, finish_type=2).count()
            if finish_count == total_count:
                top_novice_task = UserTaskRecord.objects.filter(task_id=str(top_task.id)).first()
                if not top_novice_task:
                    new_record = UserTaskRecord()
                    new_record.user_id = user_id
                    new_record.task_id = str(top_task.id)
                    new_record.reward_type = top_task.reward_type
                    new_record.finish_type = 1
                    new_record.create_time = now
                    new_record.save()

        # 奖励
        reward_type = task.reward_type
        reward_count = task.reward_count
        account = Account.objects.filter(user=user).first()
        if reward_type == 2:
            account.diamond_trade_in(reward_count, 0, u"任务奖励, task_id="+str(task.id), TradeDiamondRecord.TradeTypeDiamondTaskReward)
        elif reward_type == 1:
            account.gold_trade_in(reward_count, u"任务奖励, task_id="+str(task.id), TradeGoldRecord.TypeTaskReward)
        elif reward_type == 3:
            # 大转盘机会
            pass
        record.update(set__finish_type=2)
        return code, error


class UserTaskRecord(Document):
    task_id = StringField(verbose_name=u"任务id")
    reward_type = IntField(verbose_name=u"奖励类型")  # 1:金币  2:钻石  3:转盘抽奖机会
    user_id = IntField(verbose_name=u"用户id")
    create_time = DateTimeField(verbose_name=u"创建时间")
    finish_type = IntField(verbose_name=u"完成状态")  # 1:待领取  2:已完成
