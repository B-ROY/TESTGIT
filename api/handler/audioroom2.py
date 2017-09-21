#coding=utf-8

from api.document.doc_tools import *
from api.view.base import *

from api.convert.convert_user import *
from api.util.agoratools.voicekeyutil import generate_media_channel_key, generate_signalingkey
import time,datetime
from app.customer.models.account import Account, TicketAccount,TradeTicketRecord, TradeDiamondRecord
from app.audio.models.roomrecord import RoomRecord
from django.conf import settings
from app_redis.user.models.user import *


appID = settings.Agora_AppId
appCertificate = settings.Agora_appCertificate


#声网登录
@handler_define
class GenerateVoiceSig(BaseHandler):
    @api_define("Generate audio sig", r'/room/sig',
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
class RoomCall(BaseHandler):
    @api_define("room call", r'/room/call',
        [
            Param("peer_id", True, str, "", "", u'对方id'),
            Param("call_type", True, int, 1, 1, u'呼叫类型(0:语音,1:视频)')
        ],
        description=u"呼叫接口"
    )
    @login_required
    def get(self):
        peer_id = self.arg("peer_id")
        call_type = self.arg_int("call_type")

        room_user = User.objects.get(id=peer_id)
        user = self.current_user
        # todo 进行判断 peer_user能否被呼叫 如果可以 继续生成key 如果不能 返回错误(包括但不限于 勿扰 正在通话
        # 1.判断user 是是否是小号
        if room_user.user_type==2:
            return self.write({'status': "success", 'channelKey': "", 'channel_id': "room_"+str(peer_id)+str(time.time())})
        # 2.判断该用户是否是勿扰
        if room_user.disturb_mode != 0:
            return self.write({
                'status': "failed",
                "room_status": "20001",
            })
        # 3. 判断用户是否正在通话
        if room_user.audio_status==1:
            return self.write({'status': "failed", 'room_status': 10003})
        # 4 如果是视频电话 判断主播是否认证过
        if call_type == 1 and room_user.is_video_auth!=1:
            return self.write({'status': "failed", "error": "对方暂未进行视频认证～"})
        #5. 判断拨打人是否余额足够
        user_account = Account.objects.get(user=user)
        room_price = room_user.video_price if call_type == 1 else room_user.now_price
        # 主播下首页
        if room_user.is_video_auth:
            UserRedis.delete_user_recommed_id_v3_one(peer_id)

        if user_account.diamond < room_price:
            return self.write({"status": "failed", "error": u"余额不足一分钟" })

        #能否拨通判断完毕，若能拨打则先创建房间 然后修改拨打人状态
        join_ip = self.user_ip
        room_id = str(RoomRecord.create_room_reocord(room_user.id, user.id, room_price, call_type, join_ip).id)
        unixts = int(time.time())
        randomint = -2147483647
        expiredts = 0
        uid = self.current_user_id
        channelkey = generate_media_channel_key(appID, appCertificate, room_id, unixts, randomint, int(uid), expiredts)

        user.update(set__audio_status=1, set__last_room_id=room_id)
        room_user.update(set__audio_status=1, set__last_room_id=room_id)

        return self.write({'status': "success", 'channelKey': channelkey, 'channel_id': room_id})

@handler_define
class IsVideoRoom(BaseHandler):
    @api_define("Is Video Room", r'/room/type',[
                Param('room_id', False, str, "","",u'房间号')
    ], description=u'根据房间号获取房间类型')
    @login_required
    def get(self):
        channel_id = self.arg("room_id", "")
        is_video = RoomRecord.objects.get(id=channel_id).room_type
        self.write({
            "status": "success",
            "channel_id": channel_id,
            "is_video": is_video
        })

@handler_define
class GetRoomStatus(BaseHandler):
    @api_define("Get Uid Room Status", r'/room/status', [
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


@handler_define
class RoomAnswer(BaseHandler):
    @api_define("room answer", r'/room/answer',
                [
                    Param("room_id", True, str, "", "", description=u"房间id")
                ], description=u"接听接口")
    @login_required
    def get(self):
        room_id = self.arg("room_id")
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
        channelkey = generate_media_channel_key(appID, appCertificate, str(record.id), unixts, randomint, uid, expiredts)
        user.update(set__last_room_id=room_id)
        self.write({'status': "success", 'channelKey': channelkey, 'channel_id': str(record.id)})


@handler_define
class RoomInfo(BaseHandler):
    @api_define("room refuse", r'/room/info',
                [
                    Param("room_id", True, str, "", "", description=u"房间id")
                ], description=u"拒绝通话接口")
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
        data = {
            "audioroom": room_info,
            "user": convert_user(room_user),
            "join": convert_user(join_user),
        }
        self.write({"status": "success", "data": data})



@handler_define
class RoomRefuse(BaseHandler):
    @api_define("room refuse", r'/room/refuse',
                [
                    Param("room_id", True, str, "", "", description=u"房间id")
                ], description=u"拒绝通话接口")
    @login_required
    def get(self):
        room_id = self.arg("room_id")
        # todo 拒绝 删除redis 更改数据库
        record = RoomRecord.objects.get(id=room_id)
        record.finish_room(end_type=4)

        return self.write({"status": "success"})

@handler_define
class RoomCancel(BaseHandler):
    @api_define("room cancel invite", r'/room/cancel',
                [
                    Param("room_id", True, str, "", "", description=u"房间id")
                ], description=u"拨打人取消呼叫")
    @login_required
    def get(self):
        # todo 加判断 是否是本人请求

        room_id = self.arg("room_id")
        record = RoomRecord.objects.get(id=room_id)
        record.finish_room(end_type=1)

        return self.write({"status": "success"})


@handler_define
class RoomQuit(BaseHandler):
    @api_define("room hangup", r'/room/quit',
                [
                    Param("room_id", True, str, "","", description=u"房间id"),
                    Param("quit_type", False, str, "", "", description=u"退出原因")  # 0.主动挂断， 1.对方异常挂断
                ], description=u"结束通话接口")
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

        end_type = 0 #1. 用户取消请请求 2. 用户挂断 3.用户异常挂断 4.主播拒绝 5 主播挂断 6 主播异常挂断
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


@handler_define
class RoomEndInfo(BaseHandler):
    @api_define("room end info", r'/room/bequited',
                [
                    Param("room_id", True, str, "", "", description=u"房间id"),
                ], description=u"被挂断的一方获取数据")
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


@handler_define
class RoomReport(BaseHandler):
    @api_define("room report", r'/room/report',[
                Param("room_id", True, str, "", "", description=u"房间心跳接口")
                ],
                description=u"房间心跳接口")
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
class RoomPaybill(BaseHandler):
    @api_define("room paybill", r'/room/paybill',[
                Param("room_id", True, str, "", "", description=u"房间心跳接口")
                ], description=u"付费接口")
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
            pay_times = (pay_interval + 5)/60
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

@handler_define
class RoomReportClose(BaseHandler):
    @api_define("room paybill", r'/room/reportclose', [
        Param("room_id", True, str, "", "", description=u"房间心跳接口")
    ], description=u"付费接口")
    @login_required
    def get(self):
        room_id = self.arg("room_id")
        record = RoomRecord.objects.get(id=room_id)

        user_id = self.current_user_id
        if record.user_id == int(user_id):
            record.finish_room(end_type=6)
        elif record.join_id == int(user_id):
            record.finish_room(end_type=3)

        return self.write({"status": "success"})








