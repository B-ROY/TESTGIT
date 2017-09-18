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
import international
from app.customer.models.black_user import *
from app.customer.models.rank import *
from redis_model.redis_client import *
from app.picture.models.picture import PictureInfo
from app.customer.models.real_video_verify import RealVideoVerify
from app_redis.user.models.user import *
from app.audio.models.roomrecord import RoomRecord


appID = settings.Agora_AppId
appCertificate = settings.Agora_appCertificate


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
        Param('room_user_id', False, str, "", "", u'房间创建者id'),
        Param('is_video', False, int, 0,0, u'是否是视频房间（0：否， 1：是')
    ], description=u"生成声网进入房间所要使用的ChannelKey")
    @login_required
    def get(self):
        user_id = self.arg("user_id")
        room_user_id = self.arg("room_user_id")
        if user_id != room_user_id: #拨打

            peer_id = room_user_id
            call_type = self.arg_int("is_video")

            room_user = User.objects.get(id=peer_id)
            user = self.current_user
            # todo 进行判断 peer_user能否被呼叫 如果可以 继续生成key 如果不能 返回错误(包括但不限于 勿扰 正在通话
            # 1.判断user 是是否是小号
            if room_user.user_type == 2:
                return self.write(
                    {'status': "success", 'channelKey': "", 'channel_id': "room_" + str(peer_id) + str(time.time())})
            # 2.判断该用户是否是勿扰
            if room_user.disturb_mode != 0:
                return self.write({
                    'status': "failed",
                    "room_status": "20001",
                })
            # 3. 判断用户是否正在通话
            if room_user.audio_status == 1:
                return self.write({'status': "fail", 'room_status': 10003})
            # 4 如果是视频电话 判断主播是否认证过
            if call_type == 1 and room_user.is_video_auth != 1:
                return self.write({'status': "fail", "error": "对方暂未进行视频认证～"})
            # 5. 判断拨打人是否余额足够
            user_account = Account.objects.get(user=user)
            room_price = room_user.video_price if call_type == 1 else room_user.now_price

            if user_account.diamond < room_price:
                return self.write({"status": "failed", "error": u"余额不足一分钟"})

            join_ip = self.user_ip
            # 能否拨通判断完毕，若能拨打则先创建房间 然后修改拨打人状态
            room_id = str(RoomRecord.create_room_reocord(room_user.id, user.id, room_price, call_type, join_ip).id)
            unixts = int(time.time())
            randomint = -2147483647
            expiredts = 0
            uid = self.current_user_id
            channelkey = generate_media_channel_key(appID, appCertificate, room_id, unixts, randomint, int(uid), expiredts)

            user.update(set__audio_status=1, set__last_room_id=room_id)
            room_user.update(set__audio_status=1, set__last_room_id=room_id)

            if room_user.is_video_auth:
                UserRedis.delete_user_recommed_id_v3_one(peer_id)

            return self.write({'status': "success", 'channelKey': channelkey, 'channel_id': room_id})
        else: # 接听
            room_id = self.arg("channel_id","")
            user = self.current_user
            # todo 判断redis中是否有自己的房间 没有可能是对面已经挂断了
            record = RoomRecord.objects.get(id=room_id)
            if record.room_status == 2:
                return self.write({"status": "fail", "error": "对方已经取消呼叫"})
            record.update(set__start_time=datetime.datetime.now(), set__is_answer=1)
            unixts = int(time.time())
            randomint = -2147483647
            expiredts = 0
            uid = int(self.current_user_id)
            channelkey = generate_media_channel_key(appID, appCertificate, str(record.id), unixts, randomint, uid,
                                                    expiredts)
            user.update(set__last_room_id=room_id)
            self.write({'status': "success", 'channelKey': channelkey, 'channel_id': str(record.id)})



@handler_define
class IsVideoRoom(BaseHandler):
    @api_define("Is Video Room", r'/audio/room/type', [
                Param('channel_id', False, str, "", "", u'房间号')
    ], description=u'根据房间号获取房间类型')
    @login_required
    def get(self):
        channel_id = self.arg("channel_id", "")
        is_video = RoomRecord.objects.get(id=channel_id).room_type
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
        user_id = self.arg("uid")
        user = User.objects.get(id=user_id)
        if user.audio_status == 2:
            status = 1
        else:
            status = 3
        self.write({'status': "success", 'room_status': status, })


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


#获取房间信息
@handler_define
class GetAudiorecordInfo(BaseHandler):
    @api_define("Get Audio Record Info", r'/audio/room/info', [
        Param('room_id', True, str, "", "", u'房间id'),
    ], description=u'获取房间信息')
    @login_required
    def get(self):
        room_id = self.arg("room_id")
        record = RoomRecord.objects.get(id=room_id)

        room_user = User.objects.get(id=record.user_id)
        join_user = User.objects.get(id=record.join_id)
        room_info = {}
        room_info['id'] = str(record.id)
        room_info['user_id'] = record.user_id
        room_info['is_video'] = record.room_type
        room_info['join_id'] = record.join_id
        room_info['now_price'] = record.price
        user_info = convert_user(room_user)
        user_info["audio_room_id"] = str(record.id)
        data = {
            "audioroom": room_info,
            "user": user_info,
            "join": convert_user(join_user),
        }

        self.write({"status": "success", "data": data, })

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


#主播拒绝接听用户呼叫调用接口
@handler_define
class AudioRoomReject(BaseHandler):
    @api_define("Audio room reject", r'/audio/room/reject', [
        Param("user_id", True, str, "", "",u'主播id'),
        Param("join_id", True, str, "", "", u'加入者id'),
    ], description=u'拒绝接听订单接口')
    @login_required
    def get(self):
        # 较新接口逻辑麻烦
        user_id = self.arg_int("user_id")
        join_id = self.arg_int("join_id")

        room_user = User.objects.get(id=user_id)
        join_user = User.objects.get(id=join_id)
        if room_user.last_room_id != join_user.last_room_id:
            return self.write({"status":"success"})

        room_id = join_user.last_room_id
        record = RoomRecord.objects.get(id=room_id)

        user = self.current_user
        if user.id == int(user_id):
            record.finish_room(end_type=4)
            return self.write({"status": "success"})
        elif user.id == int(join_id):
            record.finish_room(end_type=1)
            return self.write({"status": "success"})

        self.write({'status': "fail"})


#主播接听用户呼叫调用该接口
@handler_define
class AudioRoomAnswer(BaseHandler):
    @api_define("Audio room answer", r'/audio/room/answer', [
            Param("join_id", True, str, "", "", u'加入者id'),

        ], description=u'主播接听')
    @login_required
    def get(self):
        self.write({"status":"success"})
        return


# TODO: 15秒上报一次，如果没有上报，如果没有上报成功，系统的cron会在3分钟之后关闭房间
@handler_define
class ReportAudioRoom(BaseHandler):
    @api_define("Report audio room", r'/audio/room/report',[
        Param("room_id", True, str, None, None, "")
    ], description=u"上报通话")
    @login_required
    def get(self):
        room_id = self.arg("room_id")
        uid = self.current_user_id
        user = self.current_user
        record = RoomRecord.objects.get(id=room_id)

        # 1.判断房间是否关闭
        if record.room_status == 2:
            logging.error("/audio/report errcode 3001")
            user.update(set__audio_status=2)
            return self.write({'status': "fail", "error": "房间已经关闭", 'errcode': '3001'})

        if record.user_id == int(uid):
            record.update(set__report_time_user=datetime.datetime.now())
        elif record.join_id == int(uid):
            record.update(set__report_time_join=datetime.datetime.now())

        return self.write({"status":"success"})


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
        quit_type = self.arg_int("quit_type", 0)

        user = self.current_user

        record = RoomRecord.objects.get(id=room_id)
        if record.user_id == user.id:
            is_host = True
        else:
            is_host = False

        end_type = 0  # 1. 用户取消请请求 2. 用户挂断 3.用户异常挂断 4.主播拒绝 5 主播挂断 6 主播异常挂断
        if is_host and quit_type == 0:
            end_type = 5
        elif is_host and quit_type == 1:
            end_type = 3
        elif not is_host and quit_type == 0:
            end_type = 2
        elif not is_host and quit_type == 1:
            end_type = 6
        record.finish_room(end_type=end_type)

        total_time = int((datetime.datetime.now() - record.start_time).total_seconds())
        data = {}
        data['seconds'] = total_time
        data['price'] = record.price * record.pay_times
        data['spend'] = record.gift_value
        return self.write({"status": "success", "data": data})

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
        record = RoomRecord.objects.get(id=room_id)

        total_time = int((datetime.datetime.now() - record.start_time).total_seconds())
        data = {}
        data['seconds'] = total_time
        data['price'] = record.price * record.pay_times
        data['spend'] = record.gift_value
        # 只改变用户状态 由后台程序关闭房间
        user = self.current_user
        user.update(set__audio_status=2)

        user_id = self.current_user_id
        if record.user_id == int(user_id):
            record.update(set__report_time_user=datetime.datetime.now())
        elif record.join_id == int(user_id):
            record.update(set__report_time_join=datetime.datetime.now())

        return self.write({"status": "success", "data": data})


# 自动扣费接口 每1分钟调用一次
@handler_define
class PayAudioBill(BaseHandler):
    @api_define("pay audio bill", r'/audio/room/paybill', [
        Param("room_id", True, str, None, None, "")
    ], description=u'每分钟调用扣费')
    @login_required
    def get(self):
        room_id = self.arg("room_id")
        record = RoomRecord.objects.get(id=room_id)
        price = record.price
        user = self.current_user
        user_account = Account.objects.get(user=user)
        # 1.计算钱是否足够
        if user_account.diamond < price:
            return self.write({'status': 'fail', 'status_code': 3, })

        last_pay_time = record.last_pay_time
        if not last_pay_time:
            record.update(set__last_pay_time=datetime.datetime.now(), set__pay_times=1)
            pay_times = 1
        else:
            pay_interval = int((datetime.datetime.now() - last_pay_time).total_seconds())
            pay_times = (pay_interval + 5) / 60
            if pay_times:
                record.update(set__last_pay_time=datetime.datetime.now(), inc__pay_times=pay_times)

        cost = price * pay_times

        user_account.diamond_trade_out(price=cost, desc=u"语音聊天id=%s" % room_id,
                                       trade_type=TradeDiamondRecord.TradeTypeAudio)

        user.update(inc__cost=cost)

        room_user = User.objects.get(id=record.user_id)
        room_user.update(
            inc__ticket=int(cost)
        )
        # to_user.add_experience(10)
        ticket_account = TicketAccount.objects.get(user=room_user)
        ticket_account.add_ticket(trade_type=TradeTicketRecord.TradeTypeAudio, ticket=cost, desc=
        u"语音聊天id=%s" % room_id)

        account_money = user_account.diamond

        if account_money >= price * 3:
            return self.write({'status': 'success', 'status_code': 0, })  # 付费成功
        elif account_money < price:
            return self.write({'status': 'success', 'status_code': 1, })  # 付费成功，用户余额小于1分钟通话
        else:
            return self.write({'status': 'success', 'status_code': 2, })  # 付费成功，用户余额不足3分钟


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
        user = self.current_user
        now_price = self.arg("price")
        if not now_price or int(now_price)==0:
            now_price = 10
        user.update(set__now_price=now_price)

        self.write({'status': 'success', })


@handler_define
class UpdateVideoPrice(BaseHandler):
    @api_define("Update video price", r'/video/update/price',[
            Param('price', True, str, "", "", u'价格'),
    ],description=u'更新视频挂单价格')
    @login_required
    def get(self):
        user = self.current_user
        now_price = self.arg("price")
        user.update(set__video_price=now_price)
        self.write({'status': 'success', })


@handler_define
class UpdateListenUrlV1(BaseHandler):
    @api_define("Update listen url v1", r'/audio/update/listen_url_v1', [
        Param('listen_url', True, str, "", "", u'listen_url'),
        Param('url_duration', True, str, "", "", u'url时长(秒)'),
    ], description=u'更新listen_url v1')
    def get(self):
        user_id = self.current_user_id
        listen_url = User.convert_http_to_https(self.arg("listen_url"))
        url_duration = self.arg_int('url_duration')
        result = AudioRoomRecord.update_listen_url(user_id, listen_url, url_duration)

        if result:
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
        gender = self.arg_int("gender",0)

        data = []
        if room_type == 2 and gender == 2 :
            try:
                anchor_list = UserRedis.get_index_anchor_list((page - 1) * page_count,(page * page_count)-1)
                if len(anchor_list) > 0:
                    anchor_data = eval(UserRedis.get_index_anchor())
                    for anchor in anchor_list:
                        data.append(anchor_data[anchor])
                else:
                    data = oldanchorlist(gender,is_video,page,page_count)
            except Exception,e:
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
        advs = Adv.get_list()
        for adv in advs or []:
            result_advs.append(adv.normal_info())

        recommed_list = UserRedis.get_recommed_list_v3()
        if recommed_list:
            recommed_data = eval(UserRedis.get_recommed_v3())
            try:
                for recommed in recommed_list:
                    if recommed in recommed_data:
                        hot_list.append(json.loads(recommed_data[recommed]))

            except Exception,e:
                logging.error("audio_room_list_v3 error " + str(e))
        else:
            print "空的推荐列表"
        anchor_list = UserRedis.get_index_anchor_list_v3(0,-1)
        if len(anchor_list) > 0:
            anchor_data = eval(UserRedis.get_index_anchor_v3())
            for anchor in anchor_list:
                video_list.append(json.loads(anchor_data[anchor]))

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
        page = self.arg_int('page')
        page_count = self.arg_int('page_count')
        n = datetime.datetime.now() + datetime.timedelta(days=1)
        t = datetime.datetime(year=n.year, month=n.month, day=n.day)
        seven_days_ago = t - datetime.timedelta(days=60)

        # 返回新注册
        users = User.objects.filter(gender=2).order_by("-created_at")[page*page_count:(page+1)*page_count]
        data = []
        for user in users:
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
                dic = {
                    "audioroom": convert_audioroom(audioroom),
                    "user": convert_user(user),
                    "personal_tags": personal_tags
                }
            data.append(dic)

        self.write({"status": "success", "data": data, })


@handler_define
class GetVoiceRoomListV3(BaseHandler):
    @api_define("Get voice room list v3", r'/audio/room/list_v3', [
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

