# coding=utf-8
from django.db import models
import logging
import datetime

from app.customer.models.user import *
from app.customer.models.account import *
from app.audio.models.record import *
from app.audio.models.price import *
from app.picture.models.picture import *
from tornado.web import *
from api.settings import *
from mongoengine import *
from base.settings import CHATPAMONGO


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


# log所在路径选择
LOG_DIR="/mydata/logs/nginx/access"
#LOG_DIR = "/Users/JT/Desktop"


class UserStatistics(Document):
    uid = IntField(verbose_name=u"用户id")
    guid = StringField(verbose_name=u"设备id", max_length=64)
    created_time = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())
    update_time = DateTimeField(verbose_name=u"最后更新时间", default=datetime.datetime.now())
    time_list = ListField(StringField(verbose_name=u"时间列表", max_length=64))
    user_agent = StringField(verbose_name=u"ua", max_length=64)

    class Meta:
        statistics_label = "statistics"
        verbose_name = u"id和设备统计"
        verbose_name_plural = verbose_name


class GuidStatistics(Document):
    guid = StringField(verbose_name=u"设备id", max_length=64)
    user_agent = StringField(verbose_name=u"ua", max_length=64)
    first_time = DateTimeField(verbose_name=u"首次进入app时间", default=datetime.datetime.now())
    update_time = DateTimeField(verbose_name=u"最后更新时间", default=datetime.datetime.now())
    time_list = ListField(StringField(verbose_name=u"时间列表", max_length=64))

    class Meta:
        statistics_label = "statistics"
        verbose_name = u"设备统计"
        verbose_name_plural = verbose_name

    @classmethod
    def write_record(cls):
        try:
            _datetime = datetime.datetime.now() - datetime.timedelta(days=1)
            guid_log_dir = LOG_DIR + "/guid-" + _datetime.strftime('%Y-%m-%d') + ".log"

            file = open(guid_log_dir, 'r')
            for line in file:
                user_token, address, ua = line.split(' ', 2)
                if user_token != "-" and str("user_token=") in user_token:
                    user_token = str(user_token).split('user_token=')[1].decode('string_escape')
                    if user_token:
                        if user_token[-1] == ";":
                            user_token = user_token[0:-1]
                        if user_token[-1] == "\"" and user_token[0] == "\"":
                            user_token = user_token[1:-1]
                        uid = decode_signed_value(secret=cookie_secret, name="user_token", value=user_token)
                    else:
                        uid = None
                else:
                    uid = None

                if str("guid=") in address:
                    guid = str(address)[1:-1].split('guid=')[1].split('&')[0]
                    platform = str(address)[1:-1].split('platform=')[1]
                    ua = str(ua).split('"')[1].split('"')[0]

                    guid_db = GuidStatistics.objects.filter(guid=guid)
                    if not guid_db:
                        guid_db = GuidStatistics(
                            guid=guid,
                            user_agent=ua,
                            first_time=_datetime.date(),
                            update_time=_datetime.date(),
                            time_list=[str(_datetime.date())],
                        )
                        guid_db.save()
                    else:
                        guid_db = guid_db.first()
                        if str(_datetime.date()) not in guid_db.time_list:
                            guid_db.time_list.append(str(_datetime.date()))
                            guid_db.update_time = _datetime.date()
                            guid_db.save()

                    if uid:
                        uid_db = UserStatistics.objects.filter(uid=uid, guid=guid)
                        if not uid_db:
                            uid_db = UserStatistics(
                                uid=uid,
                                guid=guid,
                                created_time=_datetime.date(),
                                update_time=_datetime.date(),
                                time_list=[str(_datetime.date())],
                                user_agent=ua,
                            )
                            uid_db.save()
                        else:
                            uid_db = uid_db.first()
                            if str(_datetime.date()) not in uid_db.time_list:
                                uid_db.time_list.append(str(_datetime.date()))
                                uid_db.update_time = _datetime.date()
                                uid_db.save()

            file.close()
            return True
        except Exception, e:
            logging.error("write guid statistics error:{0}".format(e))
            file.close()
            return False


class AudioStatisticsTime(Document):
    statistics_time = DateTimeField(verbose_name=u"统计时间", default=datetime.datetime.now())
    audio_times = DictField(verbose_name=u"挂单人次")
    audio_person = DictField(verbose_name=u"挂单人数")
    audio_duration = DictField(verbose_name=u"通话时长(秒)")
    channel_key_times = IntField(verbose_name=u"拨打次数")
    answer_times = IntField(verbose_name=u"接通次数")
    total_spend = IntField(verbose_name=u"通话总消费金币数")

    class Meta:
        statistics_label = "statistics"
        verbose_name = u"语音统计(时间)"
        verbose_name_plural = verbose_name

    @classmethod
    def write_record(cls):
        try:
            _datetime = datetime.datetime.now() - datetime.timedelta(days=1)
            prices = PriceList.objects.all()
            open_records = AudioRoomRecord.objects(open_time__gt=_datetime.date(),
                                                   open_time__lt=datetime.datetime.now().date())
            start_records = AudioRoomRecord.objects(start_time__gt=_datetime.date(),
                                                    start_time__lt=datetime.datetime.now().date())

            audio_times = {}
            audio_person = {}
            audio_duration = {}
            total_spend = 0

            for price in prices:
                audio_times[str(price.price)] = []
                audio_person[str(price.price)] = []
                audio_duration[str(price.price)] = 0

            for record in open_records:
                audio_times[str(record.now_price)].append(record.user_id)
                if record.user_id not in audio_person[str(record.now_price)]:
                    audio_person[str(record.now_price)].append(record.user_id)

            for record in start_records:
                time = int((record.end_time - record.start_time).total_seconds())
                audio_duration[str(record.now_price)] += time
                total_spend += record.spend

            bill_records = TradeDiamondRecord.objects(created_time__gt=_datetime.date(),
                                                      created_time__lt=datetime.datetime.now().date())
            bill_records = bill_records.filter(trade_type=2)
            for record in bill_records:
                total_spend += record.diamon

            audio_statistics = AudioStatisticsTime(
                statistics_time=_datetime.date(),
                audio_times=audio_times,
                audio_person=audio_person,
                audio_duration=audio_duration,
                channel_key_times=0,
                answer_times=0,
                total_spend=total_spend,
            )
            audio_statistics.save()
            return True

        except Exception, e:
            logging.error("write audio statistics time error:{0}".format(e))
            return False


class AudioStatisticsId(Document):
    uid = IntField(verbose_name=u"用户ID")
    call_list = ListField(DictField(verbose_name=u"呼叫列表"))
    be_called_list = ListField(DictField(verbose_name=u"被呼叫列表"))

    class Meta:
        statistics_label = "statistics"
        verbose_name = u"语音统计(ID)"
        verbose_name_plural = verbose_name

    @classmethod
    def write_record(cls):
        try:
            _datetime = datetime.datetime.now() - datetime.timedelta(days=1)
            guid_log_dir = LOG_DIR + "/audio-" + _datetime.strftime('%Y-%m-%d') + ".log"

            file = open(guid_log_dir, 'r')
            channel_key_times = 0
            answer_times = 0
            for line in file:
                if str('user_token=') in line:
                    cookie = line.split('user_token=')[1].split(' ')[0].decode('string_escape')
                    if cookie[-1] == ";":
                        cookie = cookie[0:-1]
                    if cookie[-1] == "\"" and cookie[0] == "\"":
                        cookie = cookie[1:-1]
                    uid = decode_signed_value(secret=cookie_secret, name="user_token", value=cookie)

                if str('"/audio/room/channelkey"') in line:
                    room_user_id = line.split('room_user_id=')[1].split('\"')[0].split('&')[0]
                    if int(uid) != int(room_user_id):
                        channel_key_times += 1

                        logtime = line.split(' ', 10)[1]
                        logdate, logtime = logtime[1:-1].split('T')
                        logtime, timezone = logtime.split('+')
                        logtime = logdate + ' ' + logtime

                        call_dic = {}
                        call_dic['time'] = logtime
                        call_dic['user_id'] = int(uid)
                        call_dic['room_user_id'] = int(room_user_id)

                        uid_statistics = AudioStatisticsId.objects.filter(uid=int(uid))
                        if not uid_statistics:
                            uid_statistics = AudioStatisticsId(
                                uid=uid,
                                call_list=[],
                                be_called_list=[],
                            )
                        else:
                            uid_statistics = uid_statistics.first()

                        uid_statistics.call_list.append(call_dic)
                        uid_statistics.save()

                        ruid_statistics = AudioStatisticsId.objects.filter(uid=int(room_user_id))
                        if not ruid_statistics:
                            ruid_statistics = AudioStatisticsId(
                                uid=room_user_id,
                                call_list=[],
                                be_called_list=[],
                            )
                        else:
                            ruid_statistics = ruid_statistics.first()

                        ruid_statistics.be_called_list.append(call_dic)
                        ruid_statistics.save()

                elif str('"/audio/room/answer"') in line:
                    answer_times += 1

                    #                elif uri == '"/audio/add/private_picture"':

                    #                elif uri == '"/audio/change/private_picture"':

                    #                elif uri == '"/audio/purchase/private_picture"':

            audio_statistics = AudioStatisticsTime.objects.get(statistics_time=_datetime.date())
            audio_statistics.channel_key_times += channel_key_times
            audio_statistics.answer_times += answer_times
            audio_statistics.save()

            file.close()
            return True
        except Exception, e:
            logging.error("write audio statistics id error:{0}".format(e))
            file.close()
            return False


class PictureStatistics(Document):
    statistics_time = DateTimeField(verbose_name=u"统计时间", default=datetime.datetime.now())
    picture_count = DictField(verbose_name=u"发布图片张数")
    like_count = IntField(verbose_name=u"图片点赞数")
    comment_count = IntField(verbose_name=u"图片评论数")
    unlock_times = IntField(verbose_name=u"解锁图片次数")
    unlock_count = ListField(verbose_name=u"解锁图片张数")
    diamond_count = IntField(verbose_name=u"付费图片消费金币数")

    class Meta:
        statistics_label = "statistics"
        verbose_name = u"图片统计"
        verbose_name_plural = verbose_name

    @classmethod
    def write_record_db(cls):
        try:
            _datetime = datetime.datetime.now() - datetime.timedelta(days=1)
            picture_count, diamond_count = {}, 0
            unlock_times, unlock_count = 0, []
            prices = PicturePriceList.objects.all()
            picture_count['0'] = 0

            for price in prices:
                picture_count[str(price.picture_price)] = 0

            pictures = PictureInfo.objects(created_at__gt=_datetime.date(),
                                           created_at__lt=datetime.datetime.now().date())
            for picture in pictures:
                picture_count[str(picture.price)] += 1

            bill_records = TradeDiamondRecord.objects(created_time__gt=_datetime.date(),
                                                      created_time__lt=datetime.datetime.now().date())
            bill_records = bill_records.filter(trade_type=3)
            for record in bill_records:
                unlock_times += 1
                if record.desc not in unlock_count:
                    unlock_count.append(record.desc)
                diamond_count += record.diamon

            picture_statistics = PictureStatistics(
                statistics_time=_datetime.date(),
                picture_count=picture_count,
                like_count=0,
                comment_count=0,
                unlock_times=unlock_times,
                unlock_count=unlock_count,
                diamond_count=diamond_count,
            )
            picture_statistics.save()

            return True
        except Exception, e:
            logging.error("write picture statistics db error:{0}".format(e))
            return False

    @classmethod
    def write_record_log(cls):
        try:
            _datetime = datetime.datetime.now() - datetime.timedelta(days=1)
            guid_log_dir = LOG_DIR + "/picture-" + _datetime.strftime('%Y-%m-%d') + ".log"
            like_count, comment_count = 0, 0

            file = open(guid_log_dir, 'r')

            for line in file:
                if str('"/picture/like"') in line:
                    like_count += 1

                elif str('"/picture/createcomment"') in line:
                    comment_count += 1

            picture_statistics = PictureStatistics.objects.get(statistics_time=_datetime.date())
            picture_statistics.like_count += like_count
            picture_statistics.comment_count += comment_count
            # picture_statistics.unlock_times = unlock_times
            # picture_statistics.unlock_count = unlock_count
            picture_statistics.save()

            file.close()
            return True
        except Exception, e:
            logging.error("write picture statistics log error:{0}".format(e))
            file.close()
            return False


class AccountStatistics(Document):
    statistics_time = DateTimeField(verbose_name=u"统计时间", default=datetime.datetime.now())
    revenue_count = IntField(verbose_name=u"收入总金额")
    sale_day_ios = DictField(verbose_name=u'ios日销售额')
    buyer_day_ios = DictField(verbose_name=u'ios日购买用户')
    order_day_ios = DictField(verbose_name=u'ios日订单数')

    sale_day_android = IntField(verbose_name=u"安卓日销售额")
    buyer_day_android = ListField(IntField(verbose_name=u"安卓日购买用户"))
    order_day_android = IntField(verbose_name=u"安卓日订单数")

    sale_day_h5 = IntField(verbose_name=u"h5日销售额")
    buyer_day_h5 = ListField(IntField(verbose_name=u"h5日购买用户"))
    order_day_h5 = IntField(verbose_name=u"h5日订单数")

    class Meta:
        statistics_label = "statistics"
        verbose_name = u"进账统计"
        verbose_name_plural = verbose_name

    @classmethod
    def write_record(cls):
        try:
            _datetime = datetime.datetime.now() - datetime.timedelta(days=1)
            revenue_count = 0
            sale_day_ios, buyer_day_ios, order_day_ios = {"wechat": 0, "app": 0}, {"wechat": [], "app": []}, {
                "wechat": 0, "app": 0}
            sale_day_android, buyer_day_android, order_day_android = 0, [], 0
            sale_day_h5, buyer_day_h5, order_day_h5 = 0, [], 0

            records = TradeBalanceOrder.objects(buy_time__gt=_datetime.date(),
                                                buy_time__lt=datetime.datetime.now().date()).filter(status=1)
            for record in records:
                revenue_count += record.money

                if record.platform == 1:
                    sale_day_android += record.money
                    if record.user.id not in buyer_day_android:
                        buyer_day_android.append(record.user.id)
                    order_day_android += 1

                elif record.platform == 2:
                    if record.money * 0.7 == record.diamon:
                        sale_day_ios["app"] += record.money
                        if record.user.id not in buyer_day_ios["app"]:
                            buyer_day_ios["app"].append(record.user.id)
                        order_day_ios["app"] += 1
                    else:
                        sale_day_ios["wechat"] += record.money
                        if record.user.id not in buyer_day_ios["wechat"]:
                            buyer_day_ios["wechat"].append(record.user.id)
                        order_day_ios["wechat"] += 1

                elif record.platform == 3:
                    sale_day_h5 += record.money
                    if record.user.id not in buyer_day_h5:
                        buyer_day_h5.append(record.user.id)
                    order_day_h5 += 1

            account_statistics = AccountStatistics(
                statistics_time=_datetime.date(),
                revenue_count=revenue_count,
                sale_day_ios=sale_day_ios,
                buyer_day_ios=buyer_day_ios,
                order_day_ios=order_day_ios,
                sale_day_android=sale_day_android,
                buyer_day_android=buyer_day_android,
                order_day_android=order_day_android,
                sale_day_h5=sale_day_h5,
                buyer_day_h5=buyer_day_h5,
                order_day_h5=order_day_h5,
            )
            account_statistics.save()

            return True
        except Exception, e:
            logging.error("write account statistics error:{0}".format(e))
            return False



