# coding=utf-8
import datetime

from api.document.doc_tools import *
from api.view.base import *
from django.conf import settings
from api.convert.convert_user import *

from api.util.agoratools.voicekeyutil import generate_media_channel_key, generate_signalingkey
import time

from app.customer.models.user import *
from app.customer.models.adv import *
from app.customer.models.account import *
from app.customer.models.gift import GiftManager
from app.customer.models.personal_tags import *
from app.audio.models.record import AudioRoomRecord
from app.audio.models.price import *
from app.customer.models.push import PushService
from app.customer.models.online_user import *

from api.handler.thridpard.qcloud_cos import CosClient
from api.handler.thridpard.qcloud_cos import Auth
from api.handler.thridpard.qcloud_cos import CreateFolderRequest
from api.handler.thridpard.qcloud.im import QCloudIM
import json
from django.conf import settings
from app.customer.models.vip import *
import random
from app.customer.models.black_user import *
from app.customer.models.rank import *
from redis_model.redis_client import *
from app.picture.models.picture import PictureInfo
from app.customer.models.real_video_verify import RealVideoVerify

appID = settings.Agora_AppId
appCertificate = settings.Agora_appCertificate

def get_area_by_ip(ip):
    """
    In redis IP Library is preserverd as key-list

    key is the ip's the top three
    list's memeber is like  a_b_city
    a and b is the ip's fourth number
    for example 1.2.4.0 - 1.2.4.2 is Beijing
                1.2.4.3 - 1.2.4.5 is Shanghai
            In Redis, they are preserverd as 1.2.4 : [0_2_Beijing, 3_5_Shanghai]
    This method is used to resolve the city by ip and return the city.

    :param ip: user's ip
    :return: city if city else None
    """
    ips = ip.split(".")
    k = str(ips[0]) + "." + str(ips[1]) + "." + str(ips[2])

    ip4_list = RQueueClient.getInstance().redis.lrange(k, 0, 100)
    if ip4_list:
        for ip4 in ip4_list:
            ip4s = ip4.split("_")

            min_ip4 = int(ip4s[0])
            max_ip4 = int(ip4s[1])
            print min_ip4,max_ip4, ips[3]
            if min_ip4 <= int(ips[3]) <= max_ip4:
                city = ip4s[2]
                return city
        return None
    return None


#声网登录
@handler_define
class GenerateVoiceSig(BaseHandler):
    @api_define("Generate audio sig", r'/audio/sig',
        [
            Param('user_id', False, str, "", "", u'当前用户id'),
        ],description=u'生成声网登录sig')
    def get(self):
        user_id = self.current_user_id
        if self.has_arg("user_id"):
            user_id = self.arg("user_id")

        expiredtimes = int(time.time())+3600
        self.write({
            'status': "success",
            'sigkey': generate_signalingkey(appID, appCertificate, user_id, expiredtimes)
        })



@handler_define
class GenerateChannelKey(BaseHandler):
    @api_define("Generate ChannelKey", r'/audio/room/channelkey',[
        Param('channel_id', False, str, "","",u'语音聊天室的房间号'),
        Param('user_id', True, str, "","",u'当前用户id'),
        Param('room_user_id', True, str, "", "", u'房间创建者id'),
        Param('is_video', False, int, 0,0, u'是否是视频房间（0：否， 1：是')
    ], description=u"生成声网进入房间所要使用的ChannelKey")
    @login_required
    def get(self):
        unixts = int(time.time())
        randomint = -2147483647
        expiredts = 0
        uid = self.arg_int("user_id")
        ruid = self.arg_int("room_user_id")
        channelname = self.arg("channel_id", "")
        is_video = self.arg_int("is_video", 0)

        # 校验黑名单
        # black_user = BlackUser.objects.filter(from_id=uid, to_id=ruid).first()
        # if black_user:
        #     return self.write({
        #         "status": "failed",
        #         "error": "to_user is on the blacklist"
        #     })
        #
        # rever_black_user = BlackUser.objects.filter(from_id=ruid, to_id=uid).first()
        # if rever_black_user:
        #     return self.write({
        #         "status": "failed",
        #         "error": "you are on to_user's blacklist"
        #     })


        room_user = User.objects.get(id=ruid)
        if room_user.user_type == 2:
            channelkey = generate_media_channel_key(appID, appCertificate, channelname, unixts, randomint, uid,
                                                    expiredts)
            return self.write({'status': "success", 'channelKey': channelkey, 'channel_id': channelname})
        if room_user.disturb_mode != 0:
            return self.write({
                'status': "failed",
                "room_status": "20001",
            })

        if not channelname:
            try:
                room = AudioRoomRecord(
                        user_id=ruid,
                        is_video=0,
                        is_video_auth=1 if room_user.is_video_auth == 1 else 0,
                        user_gender= room_user.gender,
                        open_time=datetime.datetime.now(),
                        now_price=room_user.now_price,
                        status=1,
                        listen_url=room_user.listen_url,
                        pay_times=0,
                        spend=0,
                        gift_value=0,
                        )
                room.save()
                room_user.audio_room_id = str(room.id)
                room_user.save()
                channelname = str(room.id)
                #todo 之后修改逻辑
                return self.write({'status': "failed", 'room_status': 3 + 10000})
            except Exception, e:
                logging.error("create room record error:{0}".format(e))
                return self.write({"status": "failed", "error": str(e)})
        else:
            room = AudioRoomRecord.objects.get(id=channelname)

        if is_video == 1:
            room.now_price = room_user.video_price
        else:
            room.now_price = room_user.now_price
        if room.status == 0:
            channelname = User.objects.get(id=room.user_id).audio_room_id

        user_account = Account.objects.get(user=User.objects.get(id=uid))
        if uid != ruid and user_account.diamond < room.now_price:
            return self.write({"status": "failed", "error": u"余额不足一分钟", })

        room_status = AudioRoomRecord.get_room_status(user_id=ruid)

        if uid == ruid:
            channelkey = generate_media_channel_key(appID, appCertificate, channelname, unixts, randomint, uid, expiredts)
            self.write({'status': "success", 'channelKey': channelkey, 'channel_id': channelname})

        elif room_status == 1:
            user_status = AudioRoomRecord.get_room_status(user_id=uid)
            if user_status == 1:
                AudioRoomRecord.set_room_status(user_id=uid, status=3)
            channelkey = generate_media_channel_key(appID, appCertificate, channelname, unixts, randomint, uid, expiredts)
            #AudioRoomRecord.set_room_status(user_id=ruid, status=3)
            room = AudioRoomRecord.objects.get(id=channelname)
            room.status = 3
            room.report_join = datetime.datetime.now()
            room.is_video = is_video
            if is_video == 1:
                room.now_price = room_user.video_price
            else:
                room.now_price = room_user.now_price
            room.save()

            PushService.send_audio(user_id=uid, host_id=ruid, audio_room_id=channelname)
            self.write({'status': "success", 'channelKey': channelkey, 'channel_id': channelname})

        else:
            self.write({'status': "failed", 'room_status': room_status + 10000})


@handler_define
class IsVideoRoom(BaseHandler):
    @api_define("Is Video Room", r'/audio/room/type',[
                Param('channel_id', False, str, "","",u'房间号')
    ], description=u'根据房间号获取房间类型')
    @login_required
    def get(self):
        channel_id = self.arg("channel_id", "")
        is_video = AudioRoomRecord.objects.get(id=channel_id).is_video
        self.write({
            "status": "success",
            "channel_id": channel_id,
            "is_video": is_video
        })

@handler_define
class GetUidRoomStatus(BaseHandler):
    @api_define("Get Uid Room Status", r'/audio/uid/status',[
        Param('uid', True, str, "", "", u"uid"),
    ], description=u'根据uid获得用户房间状态')
    @login_required
    def get(self):
        user_id = self.arg_int('uid')
        room_status = AudioRoomRecord.get_room_status(user_id=user_id)
        self.write({'status': "success", 'room_status': room_status, })


#新版获取挂单房间列表
@handler_define
class GetVoiceRoomListV1(BaseHandler):
    @api_define("Get voice room list v1", r'/audio/room/list_v1', [
        Param('page', True, str, "1", "1", u'page'),
        Param('page_count', True, str, "10", "10", u'page_count'),
        Param('time_stamp', False, str, "10", "10", u"最后一个人的时间戳(page=1不用传)"),
        Param('gender', False, int, 0, 0, u"选择性别，0:全部,1:男,2:女"),
        Param('room_type', False, int, 0, 0, u"房间类型筛选，0:全部,1:语音,2:视频")
    ], description=u"获取挂单房间列表v1")
    def get(self):
        page = self.arg_int('page')
        page_count = self.arg_int('page_count')
        room_type = self.arg_int('room_type', 0)
        if room_type == 0:
            is_video = 2
        elif room_type == 1:
            is_video = 0
        else:
            is_video = 1
        """
        if self.current_user:
            gender = self.current_user.gender
        else:
            gender = 0
        """
        gender = self.arg_int("gender",0)
        if page == 1:
            query_time = datetime.datetime.now()
        else:
            time_stamp = float(self.arg('time_stamp'))
            query_time = datetime.datetime.fromtimestamp(time_stamp)

        data = []
        audiorooms = AudioRoomRecord.get_online_users_v1(query_time=query_time, page=page, page_count=page_count,
                                                         gender=gender, is_video=is_video)

        for audioroom in audiorooms:
            user = AudioRoomRecord.get_audio_user(audioroom.user_id)
            personal_tags = UserTags.get_usertags(user_id=audioroom.user_id)
            if not personal_tags:
                personal_tags = []
            dic = {
                "audioroom": convert_audioroom(audioroom),
                "user": convert_user(user),
                "personal_tags": personal_tags,
                "time_stamp": datetime_to_timestamp(audioroom.open_time),
            }
            data.append(dic)

        self.write({"status": "success", "data": data, })
'''
@handler_define
class GetAudioList(BaseHandler):
    @api_define("get audio List", r'/audio/audio/list_v1',[
        Param('page', True, str, "1", "1", u'page'),
        Param('page_count', True, str, "10", "10", u'page_count'),
        Param('time_stamp', False, str, "10", "10", u"最后一个人的时间戳(page=1不用传)"),
        Param('gender', False, int, 0, 0, u"选择性别，0:全部,1:男,2:女"),

    ],
        description=u'获取没有视频权限的在线列表')
    def get(self):
        page = self.arg_int('page')
        page_count = self.arg_int('page_count')
        """
        if self.current_user:
            gender = self.current_user.gender
        else:
            gender = 0
        """
        gender = self.arg_int("gender", 0)
        if page == 1:
            query_time = datetime.datetime.now()
        else:
            time_stamp = float(self.arg('time_stamp'))
            query_time = datetime.datetime.fromtimestamp(time_stamp)

        data = []
        audiorooms = AudioRoomRecord.get_online_users_v1(query_time=query_time, page=page, page_count=page_count, gender=gender, is_video=0)

        for audioroom in audiorooms:
            user = AudioRoomRecord.get_audio_user(audioroom.user_id)
            personal_tags = UserTags.get_usertags(user_id=audioroom.user_id)
            if not personal_tags:
                personal_tags = []
            dic = {
                "audioroom": convert_audioroom(audioroom),
                "user": convert_user(user),
                "personal_tags": personal_tags,
                "time_stamp": datetime_to_timestamp(audioroom.open_time),
            }
            data.append(dic)

        self.write({"status": "success", "data": data, })

@handler_define
class GetVideoList(BaseHandler):
    @api_define("get audio List", r'/audio/video/list_v1',[
        Param('page', True, str, "1", "1", u'page'),
        Param('page_count', True, str, "10", "10", u'page_count'),
        Param('time_stamp', False, str, "10", "10", u"最后一个人的时间戳(page=1不用传)"),
        Param('gender', False, int, 0, 0, u"选择性别，0:全部,1:男,2:女"),
    ],
        description=u'获取带有视频挂单权限的在线列表')
    def get(self):
        page = self.arg_int('page')
        page_count = self.arg_int('page_count')
        """
        if self.current_user:
            gender = self.current_user.gender
        else:
            gender = 0

        result_advs = []
        if page == 1:
            advs = Adv.get_list()
            for adv in advs or []:
                result_advs.append(adv.normal_info())
        """
        gender = self.arg_int("gender", 0)
        if page == 1:
            query_time = datetime.datetime.now()
        else:
            time_stamp = float(self.arg('time_stamp'))
            query_time = datetime.datetime.fromtimestamp(time_stamp)

        data = []
        audiorooms = AudioRoomRecord.get_online_users_v1(query_time=query_time, page=page, page_count=page_count, gender=gender, is_video=1)

        for audioroom in audiorooms:
            user = AudioRoomRecord.get_audio_user(audioroom.user_id)
            personal_tags = UserTags.get_usertags(user_id=audioroom.user_id)
            if not personal_tags:
                personal_tags = []
            dic = {
                "videoroom": convert_audioroom(audioroom),
                "user": convert_user(user),
                "personal_tags": personal_tags,
                "time_stamp": datetime_to_timestamp(audioroom.open_time),
            }
            data.append(dic)

        self.write({"status": "success", "data": data})
'''


#获取房间信息
@handler_define
class GetAudiorecordInfo(BaseHandler):
    @api_define("Get Audio Record Info", r'/audio/room/info', [
        Param('room_id', True, str, "", "", u'房间id'),
    ], description=u'获取房间信息')
    @login_required
    def get(self):
        room_id = self.arg("room_id")
        audioroom = AudioRoomRecord.objects.get(id=room_id)
        user = AudioRoomRecord.get_audio_user(audioroom.user_id)

        if audioroom.join_id:
            join = AudioRoomRecord.get_audio_user(audioroom.join_id)
            data = {
                "audioroom": convert_audioroom(audioroom),
                "user": convert_user(user),
                "join": convert_user(join),
            }
        else:
            data = {
                "audioroom": convert_audioroom(audioroom),
                "user": convert_user(user),
            }

        self.write({"status": "success", "data": data, })


#挂单接口
@handler_define
class CreateOneToOneOrder(BaseHandler):
    @api_define("Create order", r'/audio/order/create', [], description=u'用户开始挂单')
    @login_required
    def get(self):
        user_id = self.current_user_id
        user = self.current_user
        if not user.listen_url or user.now_price == None:
            self.write({"status": "failed", "error": u"请录制声音并上传挂单价格", })

        create_time = datetime.datetime.now()
        order_id = str(AudioRoomRecord.create_roomrecord(user_id=user_id, open_time=create_time))

        if order_id:
            self.write({"status": "success", "order_id": order_id})
        else:
            self.write({"status": "failed", "error": u"开启挂单失败", })


#价格列表
@handler_define
class GetPriceList(BaseHandler):
    @api_define("Get Price List", r'/audio/price/list', [], description=u'获取价格列表')
    @login_required
    def get(self):
        user = self.current_user
        price_list = PriceList.get_price_list()
        data = []
        for price in price_list:
            if (user.total_time + user.total_call_time) >= price.limit_time:
                check_is_ok = True
            else:
                check_is_ok = False
            dic = {
                "price": price.price,
                "desc": price.desc,
                "limit_time": price.limit_time,
                "check_is_ok": check_is_ok,
            }
            data.append(dic)

        self.write({"status": "success", "data": data,})

@handler_define
class GetVideoPriceList(BaseHandler):
    @api_define("Get Video Price List", r'/video/price/list', [],description=u'获取视频价格列表')
    @login_required
    def get(self):
        user = self.current_user
        video_price_list = VideoPriceList.get_price_list()
        check_is_ok = True
        data_video=[]
        for price in video_price_list:
            dic = {
                "price": price.price,
                "desc": price.desc,
                "limit_time": price.limit_time,
                "check_is_ok": check_is_ok,
            }
            data_video.append(dic)
        self.write({"status": "success", "data":data_video})




#获得用户历史信息 废弃接口直接返回200 代码先注释掉
@handler_define
class GetUserInfo(BaseHandler):
    @api_define("Get User Info", r'/audio/order/lastinfo', [], description=u'获取用户历史信息')
    @login_required
    def get(self):
        """
        user = self.current_user
        if user.audio_room_id:
            userroom = AudioRoomRecord.objects.get(id=user.audio_room_id)
            is_open = AudioRoomRecord.check_is_open(user.id)

            price_desc = PriceList.get_price_desc(userroom.now_price)
            data = convert_user(user)
            data["price_desc"] = price_desc

            self.write({"status": "success", "data": data, "is_open": is_open, })
        else:
            data = {}
            self.write({"status": "success", "data": data, "is_open": 0, })
        """
        return self.write({"status:sucess"})



@handler_define
class CloseOneToOneOrder(BaseHandler):
    @api_define("close order", r'/audio/order/close', [
            # Param("order_id", True, str, None, None, "")
        ], description=u'用户结束挂单')
    def get(self):
        end_time = datetime.datetime.now()
        user_id = self.current_user_id
        AudioRoomRecord.close_roomrecord(user_id, end_time)
        self.write({'status': 'success'})


#主播拒绝接听用户呼叫调用接口
@handler_define
class AudioRoomReject(BaseHandler):
    @api_define("Audio room reject", r'/audio/room/reject', [
        Param("user_id", True, str, "", "", u'主播id'),
        Param("join_id", True, str, "", "", u'加入者id'),
    ], description=u'拒绝接听订单接口')
    @login_required
    def get(self):
        user_id = self.arg_int("user_id")
        join_id = self.arg_int("join_id")
        AudioRoomRecord.set_room_status(user_id=user_id, status=1)
        join_status = AudioRoomRecord.get_room_status(user_id=join_id)
        if join_status == 3:
            AudioRoomRecord.set_room_status(user_id=join_id, status=1)

        self.write({'status': "success", })


#主播接听用户呼叫调用该接口
@handler_define
class AudioRoomAnswer(BaseHandler):
    @api_define("Audio room answer", r'/audio/room/answer', [
            Param("join_id", True, str, "", "", u'加入者id'),

        ], description=u'主播接听')
    @login_required
    def get(self):
        #返回加入房间的channelKey
        user_id = self.current_user_id
        join_id = self.arg("join_id")
        start_time = datetime.datetime.now()
        status = AudioRoomRecord.start_roomrecord(user_id=user_id, join_id=join_id, start_time=start_time)

        if status:
            self.write({"status": "success", })
        else:
            self.write({"status": "failed", })


# TODO: 15秒上报一次，如果没有上报，如果没有上报成功，系统的cron会在3分钟之后关闭房间
@handler_define
class ReportAudioRoom(BaseHandler):
    @api_define("Report audio room", r'/audio/room/report',[
        Param("room_id", True, str, None, None, "")
    ], description=u"上报通话")
    @login_required
    def get(self):
        room_id = self.arg("room_id")
        room = AudioRoomRecord.objects.get(id=room_id)
        user_id = self.current_user_id
        end_time = datetime.datetime.now()
        if room.status != 2:
            AudioRoomRecord.finish_roomrecord(room_id=room_id, end_time=end_time)
            return self.write({'status': "fail", "error": "房间已经关闭", 'errcode': '3001'})

        current_time = datetime.datetime.now()

        if abs(current_time - room.report_user).seconds < 180 and abs(current_time - room.report_join).seconds < 180:
            if int(user_id) == room.user_id:
                room.report_user = current_time
                room.save()
            elif int(user_id) == room.join_id:
                room.report_join = current_time
                room.save()
            else:
                AudioRoomRecord.finish_roomrecord(room_id=room_id, end_time=end_time)
                return self.write({'status': "fail", "error": "用户未找到", 'errcode':'3002'})

        else:
            AudioRoomRecord.finish_roomrecord(room_id=room_id, end_time=end_time)
            return self.write({'status': 'fail', "error": "房间异常", 'errcode': '3003'})

        return self.write({'status': "success"})


@handler_define
class QuitAudioRoom(BaseHandler):
    @api_define("Close audio room", r'/audio/room/quit',
        [
            # Param("order_id", False, str, None, None, ""),
            Param("room_id", True, str, None, None, "")
        ], description=u'结束1对1通话,主动挂断一方读取数据')
    @login_required
    def get(self):
        room_id = self.arg("room_id")
        end_time = datetime.datetime.now()
        data = AudioRoomRecord.finish_roomrecord(room_id=room_id, end_time=end_time)
        if data:
            self.write({'status': 'success', 'data': data, })
        else:
            self.write({'status': 'failed', })

# 被动关闭房间
@handler_define
class BeQuitedAudioRoom(BaseHandler):
    @api_define("Be closed audio room", r'/audio/room/bequited',
        [
            Param("room_id", True, str, None, None, "")
        ], description=u'结束1对1通话,被挂断一方读取数据')
    @login_required
    def get(self):
        room_id = self.arg("room_id")
        data = AudioRoomRecord.be_finished_roomrecord(room_id=room_id)
        if data:
            self.write({'status': 'success', 'data': data, })
        else:
            self.write({'status': 'failed', 'data': data, })


# 自动扣费接口 每1分钟调用一次
@handler_define
class PayAudioBill(BaseHandler):
    @api_define("pay audio bill", r'/audio/room/paybill', [
        Param("room_id", True, str, None, None, "")
    ], description=u'每分钟调用扣费')
    @login_required
    def get(self):
        room_id = self.arg("room_id")
        audio_status, times = GiftManager.audio_check(room_id=room_id)
        if not audio_status:
            return self.write({'status': 'failed', 'status_code': 4, })

        status, account_money = GiftManager.audio_bill(room_id=room_id, times=times)
        room_price = AudioRoomRecord.objects.get(id=room_id).now_price
        if status:
            AudioRoomRecord.add_paytimes(room_id=room_id)
            if account_money >= room_price * 3:
                self.write({'status': 'success', 'status_code': 0, })  # 付费成功
            elif account_money < room_price:
                self.write({'status': 'success', 'status_code': 1, })  # 付费成功，用户余额小于1分钟通话
            else:
                self.write({'status': 'success', 'status_code': 2, })  # 付费成功，用户余额不足3分钟
        else:
            self.write({'status': 'failed', 'status_code': 3, })  # 付费失败



class AudioRecord:
    appid = 10048692
    secret_id = u'AKIDgknyBYkNKnpONeweTRwK9t6Nn0jn78yG'
    secret_key = u'fBCXVJK1PpWPtYizb7vIGVMIJFm90GBa'
    def __init__(self,bucket,cos_path):
        self.cos_client = CosClient(self.appid, self.secret_id, self.secret_key)
        self.auth = Auth(self.cos_client.get_cred())
        self.bucket = bucket
        self.cos_path = cos_path

    def get_once_sign(self):
        return self.auth.sign_once(self.bucket, self.cos_path)

    def get_more_sign(self):
        return self.auth.sign_more(self.bucket, self.cos_path,int(time.time())+60)

    def get_down_sign(self):
        return self.auth.sign_download(self.bucket, self.cos_path,int(time.time())+60)

    def DirIsExist(self):
        return False

    def CreateIntroduceDir(self):
        #'/record/introduce/' + xxx 
        request = CreateFolderRequest(self.bucket, self.cos_path)
        create_folder_ret = self.cos_client.create_folder(request)
        return create_folder_ret


@handler_define
class UploadIntroduceRecord(BaseHandler):
    @api_define("Upload record", r'/audio/record/upload/introduce',[
        Param('user_id', True, str, "","",u'当前用户id'),
    ], description=u'上传录音文件')
    def get(self):
        uid = self.arg('user_id')
        bucket = u'heydo'
        cospath = u'/record/introduce/' + uid + '/'
        ar = AudioRecord(bucket,cospath)
        sign = ar.get_more_sign()
        result = ar.CreateIntroduceDir()

        self.write({'status':'success','sign':sign,'bucket':bucket,'cospath':cospath,'errcode':result.get('code')})


@handler_define
class UpdateNowPrice(BaseHandler):
    @api_define("Update now price", r'/audio/update/price', [
        Param('price', True, str, "", "", u'价格'),
    ], description=u'更新语音挂单价格')
    @login_required
    def get(self):
        user_id = self.current_user_id
        now_price = self.arg("price")
        result = AudioRoomRecord.update_now_price(user_id, now_price, 0)
        if result:
            self.write({'status': 'success', })
        else:
            self.write({'status': 'failed', })
@handler_define
class UpdateVideoPrice(BaseHandler):
    @api_define("Update video price", r'/video/update/price',[
            Param('price', True, str, "", "", u'价格'),
    ],description=u'更新视频挂单价格')
    @login_required
    def get(self):
        user_id = self.current_user_id
        now_price = self.arg("price")
        result = AudioRoomRecord.update_now_price(user_id, now_price, 1)
        if result:
            self.write({'status': 'success', })
        else:
            self.write({'status': 'failed', })


@handler_define
class UpdateListenUrlV1(BaseHandler):
    @api_define("Update listen url v1", r'/audio/update/listen_url_v1', [
        Param('listen_url', True, str, "", "", u'listen_url'),
        Param('url_duration', True, str, "", "", u'url时长(秒)'),
    ], description=u'更新listen_url v1')
    def get(self):
        user_id = self.current_user_id
        # listen_url = self.arg("listen_url")
        listen_url = User.convert_http_to_https(self.arg("listen_url"))
        url_duration = self.arg_int('url_duration')
        result = AudioRoomRecord.update_listen_url(user_id, listen_url, url_duration)
        if result:
            user = self.current_user
            if user.gender == 2 and user.bottle_switch == 1:
                to_list = []
                online_users = OnlineUser.get_list()
                for online_user in online_users:
                    if online_user.user.bottle_switch == 1 and online_user.user.gender == 1:
                        to_list.append(online_user.user.sid)

                if to_list:
                    random_int = int(time.mktime(datetime.datetime.now().timetuple()))
                    bottle_result = QCloudIM.voice_in_bottle(user=user, to_list=to_list, random_int=random_int, listen_url=listen_url, url_duration=url_duration)
                    print bottle_result

            self.write({'status': 'success', })
        else:
            self.write({'status': 'failed', })


@handler_define
class UserOnlineSubscribe(BaseHandler):
    @api_define("user online subscribe", r'/audio/user_subscribe', [], description=u'用户上线订阅')
    def post(self):
        body = self.request.body
        result = json.loads(body)
        user_id = int(result.get("account"))
        is_online = result.get("is_online")

        return self.write({"status": "success", })





@handler_define
class GetVoiceRoomListV2(BaseHandler):
    @api_define("Get voice room list v1", r'/audio/room/list_v2', [
        Param('page', True, str, "1", "1", u'page'),
        Param('page_count', True, str, "10", "10", u'page_count'),
        Param('time_stamp', False, str, "10", "10", u"最后一个人的时间戳(page=1不用传)"),
        Param('gender', False, int, 0, 0, u"选择性别，0:全部,1:男,2:女"),
        Param('room_type', False, int, 0, 0, u"房间类型筛选，0:全部,1:语音,2:视频")
    ], description=u"获取挂单房间列表v2")
    def get(self):
        page = self.arg_int('page')
        page_count = self.arg_int('page_count')
        room_type = self.arg_int('room_type', 0)

        if room_type == 0:
            is_video = 2
        elif room_type == 1:
            is_video = 0
        else:
            is_video = 1
        """
        if self.current_user:
            gender = self.current_user.gender
        else:
            gender = 0
        """
        ids = {
            2: [
                3078734,
                3078733,
                3078732,
                3078731,
                3078730,
                3078729,
                3078728,
                3078727,
                3078726,
                3078725,
                3078724,
                3078723,
                3078722,
                3078721,
                3078719,
                3078718,
                3078717,
                3078716,
                3078715,
                3078714,
                3078713,
                3078712,
                3078711,
                3078710,
                3078709,
                3078708,
                3078707,
                3078706,
                3078705,
                ],
            1: [
                3078761,
                3012010,
                3014151,
                3012694,
                3020174,
                3014372,
                3002127,
                3004655,
                3011170,
                3012349,
                3008618,
                3002192,
                3014207,
                3013780,
                3013408,
                3013281,
                3014195,
                3014208,
                3013449,
                3014206,
                3011658,
                3011033,
                3013099,
                3000542,
                3000469,
                3000490,
                3000549,
                3000545,
                3000579,
                3000575,
                3000629,
            ]
        }
        ua = self.request.headers.get('User-Agent')
        uas = ua.split(";")
        app_name = uas[0]

        if app_name == "reliaozaixian":
            ids = {
                2: [
                    3078705,
                    3078706,
                    3078707,
                    3078708,
                    3078709,
                    3078710,
                    3078711,
                    3078712,
                    3080101,
                    3080102,
                    3080100,
                    3080097,
                    3080096,
                    3080095,
                    3080093,
                    3080094,
                    3080092,
                    3080091,
                    3080087,
                    3080089,
                    3080086,
                    3080085,
                    3080082,
                    3080083,
                    3080081,

                ],
                1: [
                    3066517,
                    3066563,
                    3066564,
                    3066560,
                    3066561,
                    3066549,
                    3066548,
                    3066547,
                    3066545,
                    3066546,
                    3066544,
                    3066540,
                    3066538,
                    3066537,
                    3066534,
                    3066536,
                    3066532,
                    3066564,
                    3066530,
                    3066526,
                    3066527,
                    3066525,
                    3066522,
                    3066520,
                    3066519,
                ]

            }
        gender = self.arg_int("gender", 0)

        data = []
        if page ==1 :
            if gender == 1:
                users = User.objects.filter(identity__in=ids[1])
            elif gender == 2:
                users = User.objects.filter(identity__in=ids[2])
            else:
                users = User.objects.filter(identity__in=ids[1] + ids[2])
            for user in users:
                #if not user.audio_room_id:
                #   continue
                if user.id == 1 or user.id == 2:
                    continue
                if not user.audio_room_id:
                    continue
                audioroom = AudioRoomRecord.objects.get(id=user.audio_room_id)
                personal_tags = UserTags.get_usertags(user_id=user.id)
                if not personal_tags:
                    personal_tags = []
                dic = {
                    "audioroom": convert_audioroom(audioroom),
                    "user": convert_user(user),
                    "personal_tags":personal_tags,
                    "time_stamp":datetime_to_timestamp(audioroom.open_time)
                }
                data.append(dic)
	random.shuffle(data)
        self.write({"status": "success", "data": data, })


# 新人驾到  (在线的, 认证主播 认证时间倒序)
@handler_define
class GetNewAnchorList(BaseHandler):
    @api_define("Get new anchor online list ", r'/audio/room/new_anchor_list', [
        Param('page', True, str, "1", "1", u'page'),
        Param('page_count', True, str, "10", "10", u'page_count')
    ], description=u"新人驾到")
    def get(self):

        from app.customer.models.rank import NewAnchorRank
        page = self.arg_int('page')
        page_count = self.arg_int('page_count')

        ids = [
            3078724,
            3078723,
            3078722,
            3078721,
        ]
        random.shuffle(ids)
        data = []
        if page == 1:
            for id in ids:
                user = User.objects.filter(identity=id).first()
                if user.id == 1 or user.id == 2:
                    continue

                audioroom = AudioRoomRecord.objects.get(id=user.audio_room_id)
                personal_tags = UserTags.get_usertags(user_id=user.id)
                user_vip = UserVip.objects.filter(user_id=user.id).first()
                if user_vip:
                    vip = Vip.objects.filter(id=user_vip.vip_id).first()
                    dic = {
                        "audioroom": convert_audioroom(audioroom),
                        "user": convert_user(user),
                        "personal_tags": personal_tags,
                        "vip": convert_vip(vip)
                    }
                else:
                    # 测试
                    # vip = Vip.objects.filter(id="5928e5ee2040e4079fff2322").first()
                    dic = {
                        "audioroom": convert_audioroom(audioroom),
                        "user": convert_user(user),
                        "personal_tags": personal_tags
                    }
                data.append(dic)
        self.write({"status": "success", "data": data, })
@handler_define
class GetVoiceRoomListV3(BaseHandler):
    @api_define("Get voice room list v3", r'/audio/11room/list_v311', [
        Param('page', True, str, "1", "1", u'page'),
        Param('page_count', True, str, "10", "10", u'page_count'),
        Param('time_stamp', False, str, "10", "10", u"最后一个人的时间戳(page=1不用传)"),
        Param('gender', False, int, 0, 0, u"选择性别，0:全部,1:男,2:女"),
        Param('room_type', False, int, 0, 0, u"房间类型筛选，0:全部,1:语音,2:视频")
    ], description=u"获取挂单房间列表v3(带相册图片)")
    def get(self):
        page = self.arg_int('page')
        page_count = self.arg_int('page_count')
        room_type = self.arg_int('room_type', 0)

        if room_type == 0:
            is_video = 2
        elif room_type == 1:
            is_video = 0
        else:
            is_video = 1
        """
        if self.current_user:
            gender = self.current_user.gender
        else:
            gender = 0
        """
        gender = self.arg_int("gender",0)

        data = []
        if room_type == 2 and gender == 2 :
            try:
                anchor_list = UserRedis.get_index_anchor_list((page - 1) * page_count,(page * page_count)-1)
                anchor_data = eval(UserRedis.get_index_anchor())
                if len(anchor_list) > 0:
                    for anchor in anchor_list:
                        #tempobj = UserRedis.get_index_anchor(anchor)
                        # if "audioroom" in tempobj:
                        #     tempobj["audioroom"] = eval(tempobj["audioroom"])
                        # if "user" in tempobj:
                        #     tempobj["user"] = eval(tempobj["user"])
                        # if "vip" in tempobj:
                        #     tempobj["vip"] = eval(tempobj["vip"])
                        # if tempobj["personal_tags"]:
                        #     tempobj["personal_tags"] = eval(tempobj["personal_tags"])
                        data.append(anchor_data[anchor])
                else:
                    data = oldanchorlist(gender,is_video,page,page_count)
            except Exception,e:
                print e
                data = oldanchorlist(gender,is_video,page,page_count)
        else:
            data = oldanchorlist(gender,is_video,page,page_count)
        self.write({"status": "success", "data": map(lambda x:json.loads(x), data)})

def oldanchorlist(gender,is_video,page,page_count):
    data = []
    if gender!=0:
        if is_video == 1:
            users = User.objects.filter(is_video_auth=1,gender=gender,audio_room_id__ne="", disturb_mode=0).order_by("-current_score")[
                    (page - 1) * page_count:page * page_count]
        elif is_video == 0:
            users = User.objects.filter(is_video_auth__ne=1,gender=gender,audio_room_id__ne="", disturb_mode=0).order_by("-current_score")[
                    (page - 1) * page_count:page * page_count]
        else:
            users = User.objects.filter(gender=gender,audio_room_id__ne="", disturb_mode=0).order_by("-current_score")[(page - 1) * page_count:page * page_count]
    else:
        if is_video == 1:
            users = User.objects.filter(is_video_auth=1, audio_room_id__ne="", disturb_mode=0).order_by(
                "-current_score")[
                    (page - 1) * page_count:page * page_count]
        elif is_video == 0:
            users = User.objects.filter(is_video_auth__ne=1, audio_room_id__ne="", disturb_mode=0).order_by(
                "-current_score")[
                    (page - 1) * page_count:page * page_count]
        else:
            users = User.objects.filter(audio_room_id__ne="", disturb_mode=0).order_by("-current_score")[
                    (page - 1) * page_count:page * page_count]


    for user in users:
        #if not user.audio_room_id:
        #   continue
        if user.id == 1 or user.id == 2:
            continue
        audioroom = AudioRoomRecord.objects.get(id=user.audio_room_id)
        personal_tags = UserTags.get_usertags(user_id=user.id)
        if not personal_tags:
            personal_tags = []
        user_vip = UserVip.objects.filter(user_id=user.id).first()

        # 是否在线 查看心跳
        import time
        time = int(time.time())
        pre_time = time - 3600
        user_beat = UserHeartBeat.objects.filter(user=user, last_report_time__gte=pre_time).first()
        if user_beat:
            is_online = 1
        else:
            is_online = 0

        # 视频认证状态
        real_video = RealVideoVerify.objects(user_id=user.id, status__ne=2).order_by("-update_time").first()
        show_video = RealVideoVerify.objects(user_id=user.id, status=1).order_by("-update_time").first()

        if user_vip:
            vip = Vip.objects.filter(id=user_vip.vip_id).first()
            dic = {
                "audioroom": convert_audioroom(audioroom),
                "user": convert_user(user),
                "personal_tags": personal_tags,
                "time_stamp": datetime_to_timestamp(audioroom.open_time),
                "vip": convert_vip(vip),
                "is_online": is_online
            }
        else:
            dic = {
                "audioroom": convert_audioroom(audioroom),
                "user": convert_user(user),
                "personal_tags": personal_tags,
                "time_stamp": datetime_to_timestamp(audioroom.open_time),
                "is_online": is_online
            }

        if show_video:
            dic["check_real_video"] = show_video.status
        else:
            if real_video:
                dic["check_real_video"] = real_video.status
            else:
                dic["check_real_video"] = 3

        data.append(json.dumps(dic))
    return data


@handler_define
class GetVoiceRoomListV3(BaseHandler):
    @api_define("home page list v3", r'/audio/room/list_v3', [ ], description=u"首页接口")
    def get(self):
        result_advs = []
        hot_list = []
        video_list = []

        hot_ids = [
            3065228,
            3065232,
            3065233,
            3065234,
            3065235,

        ]
        for hot_id in hot_ids:
            user = User.objects.get(identity=hot_id)
            personal_tags = UserTags.get_usertags(user_id=user.id)
            user_vip = UserVip.objects.filter(user_id=user.id).first()

            if user_vip:
                vip = Vip.objects.filter(id=user_vip.vip_id).first()
                dic = {
                    "user":{
                        "_uid": user.sid,
                        "logo_big":user.image,
                        "nickname":user.nickname,
                        "desc":user.desc
                    },
                    "personal_tags": personal_tags,
                    "vip":{
                        "vip_type": vip.vip_type,
                        "icon_url": Vip.convert_http_to_https(vip.icon_url)
                    },
                    "is_online": 1
                }
            else:
                dic = {
                    "user": {
                        "_uid": user.sid,
                        "logo_big":user.image,
                        "nickname":user.nickname,
                        "desc":user.desc
                    },
                    "personal_tags": personal_tags,
                    "is_online": 1
                }
                dic["check_real_video"] = 3
            hot_list.append(dic)


        ids = {
            1: [
                3065237,
                3065238,
                3065239,
                3065240,
                3065241,
                3065243,
                3065246,
                3065244,
                3065242,
                3065248,
                3102710,
                3080151,
                3080148,
                3080146,
                3065247
            ]
        }

        users = User.objects.filter(identity__in=ids[1])
        for user in users:
            #if not user.audio_room_id:
            #   continue

            if user.id == 1 or user.id == 2:
                continue
            is_online =1
            # # 视频认证状态
            # real_video = RealVideoVerify.objects(user_id=user.id, status__ne=2).order_by("-update_time").first()
            # show_video = RealVideoVerify.objects(user_id=user.id, status=1).order_by("-update_time").first()

            personal_tags = UserTags.get_usertags(user_id=user.id)
            if not personal_tags:
                personal_tags = []
            user_vip = UserVip.objects.filter(user_id=user.id).first()
            if user_vip:
                vip = Vip.objects.filter(id=user_vip.vip_id).first()
                dic = {
                    "user":{
                        "_uid": user.sid,
                        "logo_big":user.image,
                        "nickname":user.nickname,
                        "desc":user.desc
                    },
                    "personal_tags": personal_tags,
                    "vip":{
                        "vip_type": vip.vip_type,
                        "icon_url": Vip.convert_http_to_https(vip.icon_url)
                    },
                    "is_online": is_online
                }
                video_list.append(dic)
            else:
                dic = {
                    "user": {
                        "_uid": user.sid,
                        "logo_big":user.image,
                        "nickname":user.nickname,
                        "desc":user.desc
                    },
                    "personal_tags": personal_tags,
                    "is_online": is_online
                }
                dic["check_real_video"] = 3
                video_list.append(dic)
        self.write({
            "status": "success",
            "banners": result_advs,
            "video_list": video_list,
            "hot_list": hot_list,
        })


# 新人驾到  (在线的, 认证主播 认证时间倒序)
@handler_define
class GetNewAnchorList(BaseHandler):
    @api_define("Get new anchor online list ", r'/audio/room/new_anchor_list', [
        Param('page', True, str, "1", "1", u'page'),
        Param('page_count', True, str, "10", "10", u'page_count')
    ], description=u"新人驾到")
    def get(self):

        from app.customer.models.rank import NewAnchorRank
        page = self.arg_int('page')
        page_count = self.arg_int('page_count')

        anchor_list = NewAnchorRank.objects.all()[(page - 1) * page_count:page * page_count]
        data = []
        for anchor in anchor_list:
            user = User.objects.filter(id=anchor.user_id).first()
            if user.id == 1 or user.id == 2:
                continue
            if not user.audio_room_id:
                continue
            audioroom = AudioRoomRecord.objects.get(id=user.audio_room_id)
            personal_tags = UserTags.get_usertags(user_id=user.id)
            user_vip = UserVip.objects.filter(user_id=user.id).first()
            if user_vip:
                vip = Vip.objects.filter(id=user_vip.vip_id).first()
                dic = {
                    "audioroom": convert_audioroom(audioroom),
                    "user": convert_user(user),
                    "personal_tags": personal_tags,
                    "vip": convert_vip(vip)
                }
            else:
                # 测试
                # vip = Vip.objects.filter(id="5928e5ee2040e4079fff2322").first()
                dic = {
                    "audioroom": convert_audioroom(audioroom),
                    "user": convert_user(user),
                    "personal_tags": personal_tags
                }
            data.append(dic)
        self.write({"status": "success", "data": json.data, })


@handler_define
class GetVoiceRoomListV3(BaseHandler):
    @api_define("Get voice room list v3", r'/audio/room12/list_v312', [
        Param('page', True, str, "1", "1", u'page'),
        Param('page_count', True, str, "10", "10", u'page_count'),
        Param('time_stamp', False, str, "10", "10", u"最后一个人的时间戳(page=1不用传)"),
        Param('gender', False, int, 0, 0, u"选择性别，0:全部,1:男,2:女"),
        Param('room_type', False, int, 0, 0, u"房间类型筛选，0:全部,1:语音,2:视频")
    ], description=u"获取挂单房间列表v3(带相册图片)")
    def get(self):
        page = self.arg_int('page')
        page_count = self.arg_int('page_count')
        room_type = self.arg_int('room_type', 0)


        if room_type == 0:
            is_video = 2
        elif room_type == 1:
            is_video = 0
        else:
            is_video = 1
        """
        if self.current_user:
            gender = self.current_user.gender
        else:
            gender = 0
        """
        gender = self.arg_int("gender",0)
        if page == 1:
            query_time = datetime.datetime.now()
        else:
            time_stamp = float(self.arg('time_stamp'))
            query_time = datetime.datetime.fromtimestamp(time_stamp)

        data = []

        # if gender!=0:
        #     if is_video == 1:
        #         users = User.objects.filter(is_video_auth=1,gender=gender,audio_room_id__ne="", disturb_mode=0).order_by("-current_score")[
        #                 (page - 1) * page_count:page * page_count]
        #     elif is_video == 0:
        #         users = User.objects.filter(is_video_auth__ne=1,gender=gender,audio_room_id__ne="", disturb_mode=0).order_by("-current_score")[
        #                 (page - 1) * page_count:page * page_count]
        #     else:
        #         users = User.objects.filter(gender=gender,audio_room_id__ne="", disturb_mode=0).order_by("-current_score")[(page - 1) * page_count:page * page_count]
        # else:
        #     if is_video == 1:
        #         users = User.objects.filter(is_video_auth=1, audio_room_id__ne="", disturb_mode=0).order_by(
        #             "-current_score")[
        #                 (page - 1) * page_count:page * page_count]
        #     elif is_video == 0:
        #         users = User.objects.filter(is_video_auth__ne=1, audio_room_id__ne="", disturb_mode=0).order_by(
        #             "-current_score")[
        #                 (page - 1) * page_count:page * page_count]
        #     else:
        #         users = User.objects.filter(audio_room_id__ne="", disturb_mode=0).order_by("-current_score")[
        #                 (page - 1) * page_count:page * page_count]

        ids = {
            2: [
                3078734,
                3078733,
                3078732,
                3078731,
                3078730,
                3078729,
                3078728,
                3078727,
                3078726,
                3078725,
                3078724,
                3078723,
                3078722,
                3078721,
                3078719,
                3078718,
                3078717,
                3078716,
                3078715,
                3078714,
                3078713,
                3078712,
                3078711,
                3078710,
                3078709,
                3078708,
                3078707,
                3078706,
                3078705,
            ],
            1: [
                3078761,
                3012010,
                3014151,
                3012694,
                3020174,
                3014372,
                3002127,
                3004655,
                3011170,
                3012349,
                3008618,
                3002192,
                3014207,
                3013780,
                3013408,
                3013281,
                3014195,
                3014208,
                3013449,
                3014206,
                3011658,
                3011033,
                3013099,
                3000542,
                3000469,
                3000490,
                3000549,
                3000545,
                3000579,
                3000575,
                3000629,
            ]
        }
        ua = self.request.headers.get('User-Agent')
        uas = ua.split(";")
        app_name = uas[0]

        if app_name == "tiantianyouliao":
            ids = {
                2: [
                    3078705,
                    3078706,
                    3078707,
                    3078708,
                    3078709,
                    3078710,
                    3078711,
                    3078712,
                    3080101,
                    3080102,
                    3080100,
                    3080097,
                    3080096,
                    3080095,
                    3080093,
                    3080094,
                    3080092,
                    3080091,
                    3080087,
                    3080089,
                    3080086,
                    3080085,
                    3080082,
                    3080083,
                    3080081,

                ],
                1: [
                    3066517,
                    3066563,
                    3066564,
                    3066560,
                    3066561,
                    3066549,
                    3066548,
                    3066547,
                    3066545,
                    3066546,
                    3066544,
                    3066540,
                    3066538,
                    3066537,
                    3066534,
                    3066536,
                    3066532,
                    3066564,
                    3066530,
                    3066526,
                    3066527,
                    3066525,
                    3066522,
                    3066520,
                    3066519,
                ]

            }


        gender = self.arg_int("gender", 0)

        data = []
        if page ==1 :
            if gender == 1:
                users = User.objects.filter(identity__in=ids[1])
            elif gender == 2:
                users = User.objects.filter(identity__in=ids[2])
            else:
                users = User.objects.filter(identity__in=ids[1] + ids[2])
        for user in users:
            #if not user.audio_room_id:
            #   continue
            if user.id == 1 or user.id == 2:
                continue
            audioroom = AudioRoomRecord.objects.get(id=user.audio_room_id)
            personal_tags = UserTags.get_usertags(user_id=user.id)
            if not personal_tags:
                personal_tags = []
            user_vip = UserVip.objects.filter(user_id=user.id).first()

            # 是否在线 查看心跳
            import time
            time = int(time.time())
            pre_time = time - 120
            user_beat = UserHeartBeat.objects.filter(user=user, last_report_time__gte=pre_time).first()
            if user_beat:
                is_online = 1
            else:
                is_online = 0

            # 相册(最多六张)
            pictures = PictureInfo.objects.filter(user_id=int(user.id), status=0, type__ne=2, show_status__ne=2).order_by('-created_at')[0:6]
            pics = []
            for picture in pictures:
                pic_url = picture.picture_url
                if pic_url:
                    pic_dic = {
                        "id": str(picture.id),
                        "picture_url": pic_url
                    }
                    pics.append(pic_dic)

            if user_vip:
                vip = Vip.objects.filter(id=user_vip.vip_id).first()
                dic = {
                    "audioroom": convert_audioroom(audioroom),
                    "user": convert_user(user),
                    "personal_tags": personal_tags,
                    "time_stamp": datetime_to_timestamp(audioroom.open_time),
                    "vip": convert_vip(vip),
                    "is_online": is_online,
                    "pictures": pics
                }
            else:
                dic = {
                    "audioroom": convert_audioroom(audioroom),
                    "user": convert_user(user),
                    "personal_tags": personal_tags,
                    "time_stamp": datetime_to_timestamp(audioroom.open_time),
                    "is_online": is_online,
                    "pictures": pics
                }
            data.append(dic)

        self.write({"status": "success", "data": data, })


# 新人驾到  (在线的, 认证主播 认证时间倒序)
@handler_define
class GetNewAnchorListV2(BaseHandler):
    @api_define("Get new anchor online list v2 ", r'/audio/room/new_anchor_list_v2', [
        Param('page', True, str, "1", "1", u'page'),
        Param('page_count', True, str, "10", "10", u'page_count')
    ], description=u"新人驾到v2")
    def get(self):

        from app.customer.models.rank import NewAnchorRank
        page = self.arg_int('page')
        page_count = self.arg_int('page_count')

        anchor_list = NewAnchorRank.objects.all()[(page - 1) * page_count:page * page_count]
        data = []
        for anchor in anchor_list:
            user = User.objects.filter(id=anchor.user_id).first()
            if user.id == 1 or user.id == 2:
                continue

            audioroom = AudioRoomRecord.objects.get(id=user.audio_room_id)
            personal_tags = UserTags.get_usertags(user_id=user.id)
            user_vip = UserVip.objects.filter(user_id=user.id).first()

            # 相册(最多六张)
            pictures = PictureInfo.objects.filter(user_id=int(user.id), status=0, type__ne=2, show_status__ne=2).order_by('-created_at')[0:6]
            pics = []
            for picture in pictures:
                pic_url = picture.picture_url
                if pic_url:
                    pic_dic = {
                        "id": str(picture.id),
                        "picture_url": pic_url
                    }
                    pics.append(pic_dic)

            if user_vip:
                vip = Vip.objects.filter(id=user_vip.vip_id).first()
                dic = {
                    "audioroom": convert_audioroom(audioroom),
                    "user": convert_user(user),
                    "personal_tags": personal_tags,
                    "vip": convert_vip(vip),
                    "pictures": pics
                }
            else:
                # 测试
                # vip = Vip.objects.filter(id="5928e5ee2040e4079fff2322").first()
                dic = {
                    "audioroom": convert_audioroom(audioroom),
                    "user": convert_user(user),
                    "personal_tags": personal_tags,
                    "pictures": pics
                }
            data.append(dic)
        self.write({"status": "success", "data": data, })

