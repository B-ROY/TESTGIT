#coding=utf-8
from mongoengine import *
import logging
import datetime
import time
from base.core.util.dateutils import datetime_to_timestamp
from app.customer.models.user import *
from app.customer.models.account import *
from app.customer.models.online_user import *
from django.db import models
from base.settings import CHATPAMONGO


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class VideoRoomRecord(Document):

    STATUS = [
        (0, u'未挂单'),
        (1, u'挂单中'),
        (2, u'正在通话'),
        (3, u'有用户打入'),
        (4, u'离线'),
    ]

    USER_GENDER = [
        (1, u'男'),
        (2, u'女'),
    ]

    user_id = IntField(verbose_name=u'用户id', required=True)
    user_gender = IntField(verbose_name=u'用户性别', choices=USER_GENDER)
    join_id = IntField(verbose_name=u'加入者id', default=None)
    open_time = DateTimeField(verbose_name=u'挂单开始时间', default=None)
    start_time = DateTimeField(verbose_name=u'通话开始时间', default=None)
    end_time = DateTimeField(verbose_name=u'结束时间', default=None)
    report_user = DateTimeField(verbose_name=u'用户上报时间', default=None)
    report_join = DateTimeField(verbose_name=u'加入者上报时间', default=None)
    status = IntField(verbose_name=u'当前状态', default=0, choices=STATUS)
    now_price = IntField(verbose_name=u'当前价格', default=0)
    spend = IntField(verbose_name=u'礼物数目', default=0)
    listen_url = StringField(verbose_name=u'试听url', max_length=256, default="")
    pay_times = IntField(verbose_name=u'实际扣费次数')

    class Meta:
        app_label = "video"
        verbose_name = u"记录"
        verbose_name_plural = verbose_name

    def normal_info(self):
        data = {}
        data['id'] = str(self.id) + "v"
        data['user_id'] = self.user_id
        data['join_id'] = self.join_id
        data['open_time'] = datetime_to_timestamp(self.open_time)
        data['start_time'] = datetime_to_timestamp(self.start_time)
        data['end_time'] = datetime_to_timestamp(self.end_time)
        data['report_user'] = datetime_to_timestamp(self.report_user)
        data['report_join'] = datetime_to_timestamp(self.report_join)
        data['status'] = self.status
        data['video_price'] = self.now_price
        data['spend'] = self.spend
        data['listen_url'] = self.listen_url
        return data

    @classmethod
    def create_roomrecord(cls, user_id, open_time, status=1):
        user = User.objects.get(id=user_id)

        # 关闭之前开启的房间
        close_rooms = VideoRoomRecord.objects.filter(user_id=user_id, status=1)
        for close_room in close_rooms:
            close_room.status = 0
            close_room.end_time = open_time
            close_room.spend = 0
            close_room.save()

        try:
            roomrecord = VideoRoomRecord(
                user_id=user_id,
                user_gender=User.objects.get(id=user_id).gender,
                open_time=open_time,
                now_price=user.video_price,
                status=status,
                listen_url=user.listen_url,
                pay_times=0,
                )
            roomrecord.save()
            user.video_room_id = str(roomrecord.id)
            user.save()
        except Exception,e:
            logging.error("create room record error:{0}".format(e))
            return False
        return str(roomrecord.id)

    @classmethod
    def check_is_open(cls, user_id):
        try:
            room_id = User.objects.get(id=user_id).video_room_id
            if not room_id:
                return False
            status = VideoRoomRecord.objects.get(id=room_id).status
            if room_id and status != 0:
                return True
            else:
                return False
        except Exception,e:
            logging.error("check is open error:{0}".format(e))
            return False

    #另一个用户加入房间
    @classmethod
    def start_roomrecord(cls, user_id, join_id, start_time, status=2):
        try:
            room_id = User.objects.get(id=user_id).video_room_id
            roomrecord = VideoRoomRecord.objects.get(id=room_id)
            roomrecord.join_id = join_id
            roomrecord.start_time = start_time
            roomrecord.report_user = start_time
            roomrecord.report_join = start_time
            roomrecord.status = status
            roomrecord.save()

        except Exception,e:
            logging.error("start room record error:{0}".format(e))
            return False
        return True

    @classmethod
    def add_spend(cls, room_id, spend):
        roomrecord = VideoRoomRecord.objects.get(id=room_id)
        roomrecord.spend = spend
        roomrecord.save()
        return True

    @classmethod
    def add_paytimes(cls, room_id):
        roomrecord = cls.objects.get(id=room_id)
        roomrecord.pay_times += 1
        roomrecord.save()
        return True

    @classmethod
    def finish_roomrecord(cls, room_id, end_time, spend=0, status=0):
        try:
            roomrecord = VideoRoomRecord.objects.get(id=room_id)
            to_user = User.objects.get(id=roomrecord.join_id)
            time = int((end_time - roomrecord.start_time).total_seconds())
            minute = time/60
            to_user.add_experience(minute*10)  # 每分钟10点经验

            if roomrecord.end_time:
                time = roomrecord.end_time - roomrecord.start_time
                time = int(time.total_seconds())
                price = roomrecord.pay_times * roomrecord.now_price

                data = {}
                data['seconds'] = time
                data['price'] = price
                data['join_exp'] = price * 1
                if roomrecord.pay_times == 0:
                    data['user_exp'] = minute * 10
                else:
                    data['user_exp'] = (roomrecord.pay_times - 1) * 10
                data['spend'] = roomrecord.spend
                data['spend_exp'] = roomrecord.spend * 1
                return data

            roomrecord.end_time = end_time
            roomrecord.status = status
            roomrecord.save()

            join_id = roomrecord.join_id
            join_status = VideoRoomRecord.get_room_status(user_id=join_id)
            if join_status == 3:
                VideoRoomRecord.set_room_status(user_id=join_id, status=1)

            new_id = VideoRoomRecord.recreate_roomrecord(user_id=roomrecord.user_id)
            time = roomrecord.end_time - roomrecord.start_time
            time = int(time.total_seconds())
            price = roomrecord.pay_times * roomrecord.now_price

            from_user = User.objects.get(id=roomrecord.user_id)
            from_user.video_time += time
            from_user.video_income += spend
            from_user.video_amount += 1
            from_user.video_room_id = new_id
            from_user.save()

            to_user = User.objects.get(id=roomrecord.join_id)
            to_user.video_call_time += time
            to_user.save()

            data = {}
            data['seconds'] = time
            data['price'] = price
            data['join_exp'] = price * 1
            if roomrecord.pay_times == 0:
                data['user_exp'] = minute * 10
            else:
                data['user_exp'] = (roomrecord.pay_times - 1) * 10
            data['spend'] = roomrecord.spend
            data['spend_exp'] = roomrecord.spend * 1
            data['new_id'] = new_id + "v"

        except Exception,e:
            logging.error("finish room record error:{0}".format(e))
            return False
        return data

    # 被动关闭返回房间信息
    @classmethod
    def be_finished_roomrecord(cls, room_id):
        try:
            roomrecord = VideoRoomRecord.objects.get(id=room_id)
            if not roomrecord.end_time:
                time = datetime.datetime.now() - roomrecord.start_time
            else:
                time = roomrecord.end_time - roomrecord.start_time
            time = int(time.total_seconds())
            minute = time / 60
            price = roomrecord.pay_times * roomrecord.now_price

            data = {}
            data['seconds'] = time
            data['price'] = price
            data['join_exp'] = price * 1
            if roomrecord.pay_times == 0:
                data['user_exp'] = minute * 10
            else:
                data['user_exp'] = (roomrecord.pay_times - 1) * 10
            data['spend'] = roomrecord.spend
            data['spend_exp'] = roomrecord.spend * 1

        except Exception,e:
            logging.error("be finished roomrecord:{0}".format(e))
            return False
        return data

    @classmethod
    def recreate_roomrecord(cls, user_id):
        open_time = datetime.datetime.now()
        new_id = VideoRoomRecord.create_roomrecord(user_id, open_time)
        return str(new_id)

    @classmethod
    def get_online_users_v1(cls, query_time, page=1, page_count=10, gender=0):
        if gender == 0 or gender == 2:
            users = cls.objects(status__gt=0, status__lt=4, open_time__lt=query_time).order_by('-open_time')[0:page_count]
        else:
            users = cls.objects(status__gt=0, status__lt=4, open_time__lt=query_time, user_gender=2).order_by('-open_time')[0:page_count]
        return users

    @classmethod
    def get_video_user(cls, user_id):
        user = User.objects.get(id=user_id)
        return user

    @classmethod
    def close_roomrecord(cls, user_id, end_time):
        try:
            room_id = User.objects.get(id=user_id).video_room_id
            roomrecord = VideoRoomRecord.objects.get(id=room_id)
            roomrecord.status = 0
            roomrecord.end_time = end_time
            roomrecord.spend = 0
            roomrecord.save()
        except Exception,e:
            logging.error("close room record error:{0}".format(e))
            return False
        return True

    @classmethod
    def get_room_status(cls, user_id):
        try:
            room_id = User.objects.get(id=user_id).video_room_id
            if room_id:
                status = cls.objects.get(id=room_id).status
                return status
            else:
                return 0
        except Exception,e:
            logging.error("get room status error:{0}".format(e))
            return 0

    @classmethod
    def set_room_status(cls, user_id, status):
        try:
            room_id = User.objects.get(id=user_id).video_room_id
            if room_id:
                roomrecord = cls.objects.get(id=room_id)
                roomrecord.status = status
                roomrecord.save()
                return True
            else:
                return True
        except Exception, e:
            logging.error("set room status error:{0}".format(e))
            return False

    @classmethod
    def get_new_room_id(cls, room_id):
        try:
            room = VideoRoomRecord.objects.get(id=room_id)
            if room.status == 0:
                room_id = User.objects.get(id=room.user_id).video_room_id
        except Exception,e:
            logging.error("get new room id error:{0}".format(e))
            return False
        return room_id

    @classmethod
    def update_now_price(cls, user_id, now_price):
        try:
            user = User.objects.get(id=user_id)
            user.video_price = now_price
            user.save()
            if user.video_room_id:
                roomrecord = VideoRoomRecord.objects.get(id=user.video_room_id)
                roomrecord.now_price = now_price
                roomrecord.save()
            return True
        except Exception,e:
            logging.error("update now price error:{0}".format(e))
            return False

    @classmethod
    def need_closed_userrooms(cls, page=1, page_count=20):
        """
        3分钟没有上报就自动关闭
        """
        time = datetime.timedelta(0, 180)
        objs = VideoRoomRecord.objects.filter(status=2, report_user__lt=datetime.datetime.now()-time).\
                   order_by('-created_at')[(page-1)*page_count:page*page_count]
        return objs

    @classmethod
    def need_closed_joinrooms(cls, page=1, page_count=20):
        """
        3分钟没有上报就自动关闭
        """
        time = datetime.timedelta(0, 180)
        objs = VideoRoomRecord.objects.filter(status=2, report_join__lt=datetime.datetime.now()-time).\
                   order_by('-created_at')[(page-1)*page_count:page*page_count]
        return objs

    @classmethod
    def closed_waitingrooms(cls):
        """
        拨打超过三分钟就自动关闭
        """
        try:
            objs = VideoRoomRecord.objects.filter(status=3).order_by('-created_at')
            for obj in objs:
                if obj.report_join:
                    time = datetime.datetime.now() - obj.report_join
                    time = int(time.total_seconds())
                    if time > 180:
                        obj.status = 1
                        obj.report_join = None
                        obj.save()
            return True
        except Exception,e:
            logging.error("close waitingrooms error:{0}".format(e))
            return False


