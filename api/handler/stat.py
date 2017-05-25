#coding=utf-8
import json

from api.document.doc_tools import *
from api.view.base import *
from app.stat.models.phone_stat import *
from app.customer.models.share import *


@handler_define
class CallStat(BaseHandler):
    @api_define("call statistics", r'/log/audio/callInfo',[], description="通话统计接口(depracted)")
    def post(self):
        user_agent = self.request.headers.get('User-Agent')
        data = self.get_arguments("data","")
        if self.get_arguments("data"):
            json_data = json.loads(data)
            channel_id = json_data.get("channelId")
            call_net_status = int(json_data.get("callNetStatus"))
            call_device_name = json_data.get("callDeviceName")
            source = int(json_data.get("source"))
            accept_uid = json_data.get("acceptUid")
            call_timestamp = datetime.datetime.fromtimestamp(int(json_data.get("callTimeStamp")))
            price = int(json_data.get("price"))
            call_system_version = json_data.get("callSystemVersion")
            call_type = int(json_data.get("callType"))
            call_uid = int(json_data.get("callUid"))
            guid = json_data.get("guid")
            hangup_type = int(json_data.get("hangupType"))
            hangup_timestamp = datetime.datetime.fromtimestamp(int(json_data.get("hangupTimeStamp")))
            duration = int(json_data.get("duration"))
            room_id = json_data.get("roomId")

        else:
            channel_id = self.get_arguments("channel")
            call_net_status = int(self.get_arguments("callNetStatus"))
            call_device_name = self.get_arguments("callDeviceName")
            source = self.get_arguments("source")
            accept_uid = self.get_arguments("acceptUid")
            call_timestamp = datetime.datetime.fromtimestamp(int(self.get_arguments("callTimeStamp")))
            price = int(self.get_arguments("price"))
            call_system_version = self.get_arguments("callSystemVersion")
            call_type = int(self.get_arguments("callType"))
            call_uid = int(self.get_arguments("callUid"))
            guid = self.get_arguments("guid")
            hangup_type = int(self.get_arguments("hangupType"))
            hangup_timestamp = datetime.datetime.fromtimestamp(int(self.get_arguments("hangupTimeStamp")))
            duration = int(self.get_arguments.get("duration"))
            room_id = self.get_arguments.get("roomId")

        PhoneStat.create_phone_stat(channel_id,call_net_status,call_device_name,source,accept_uid,call_timestamp,
                                    price, call_system_version, call_type, call_uid, guid, hangup_type,
                                    hangup_timestamp,duration, room_id,user_agent)

        return self.write({"status": "success"})


@handler_define
class CallStat1(BaseHandler):
    @api_define("call statistics audience", r'/log/audio/callinfo1',[
        Param("call_uid", True, int, 0, 1, u"呼叫端id"),
        Param("room_id", True, str, 0, 1, u"房间id"),
        Param("net_status", True, int, 0, 1, u"网络状况"),
        Param("source", True, int, 0, 1, u"用户进入拨打页面来源"),
        Param("call_timestamp", True, int, 0, 1, u"呼叫时间"),
        Param("price", True, int, 0, 1, u"通话价格"),
        Param("is_answered", True, int, 0, 1, u"是否接听"),
        Param("ring_duration", True, int, 0, 1, u"呼叫时长"),
        Param("answer_uid", True, int, 0, 1, u"主播id"),
        Param("call_duration", True, int, 0, 1, u"通话时长"),
        Param("start_time", True, int, 0, 1, u"通话开始时间"),
        Param("end_time", True, int, 0, 1, u"通话结束时间"),
        Param("gift_list", False, str, 0, 1, u"送出的礼物列表"),
        Param("hangup_type", True, int, 0, 1, u"挂断原因"),
        Param("error_message", False, str, 0, 1, u"错误信息"),
        Param("call_type", True, int, 0, 1, u"房间类型"),

    ], description=u"用户端通话统计上报")
    @login_required
    def post(self):
        call_uid = self.arg_int("call_uid")
        room_id = self.arg("room_id")
        net_status = self.arg_int("net_status")
        source = self.arg_int("source")
        call_timestamp = self.arg_int("call_timestamp")
        price = self.arg_int("price")
        is_answered = self.arg_int("is_answered")
        ring_duration = self.arg_int("ring_duration")

        answer_uid = self.arg_int("answer_uid")
        call_duration = self.arg("call_duration")
        start_time = self.arg_int("start_time")
        end_time = self.arg_int("end_time")
        gift_list = self.arg("gift_list", "")
        hangup_type = self.arg_int("hangup_type")
        error_message = self.arg("error_message", "")
        call_type = self.arg_int("call_type")
        guid = self.arg("guid")

        ua = self.request.headers.get('User-Agent')
        uas = ua.split(";")
        if uas[2] == "iPhone" or uas[2] == "iPad":
            platform = 1
        else:
            platform = 0

        call_timestamp = datetime.datetime.fromtimestamp(call_timestamp)
        start_time = datetime.datetime.fromtimestamp(start_time)
        end_time = datetime.datetime.fromtimestamp(end_time)

        PhoneStat.create_phone_stat(
            call_uid=call_uid,
            room_id=room_id,
            net_status=net_status,
            source=source,
            call_timestamp=call_timestamp,
            price=price,
            is_answered=is_answered==0,
            ring_duration=ring_duration,
            answer_uid=answer_uid,
            call_duration=call_duration,
            answer_timestamp=start_time,
            hangup_timestamp=end_time,
            gift_list=json.loads(gift_list) if gift_list else None,
            hangup_type=hangup_type,
            error_message=error_message,
            platform=platform,
            user_agent=ua,
            call_guid=guid,
            call_type=call_type,
            is_call=True
        )

        return self.write({"status":"success"})


@handler_define
class CallStat2(BaseHandler):
    @api_define("call statistics host", r'/log/audio/callinfo2',[
        Param("call_uid", True, int, 0, 1, u"呼叫端id"),
        Param("answer_uid", True, int, 0, 1, u"主播id"),
        Param("price", True, int, 0, 1, u"通话价格"),
        Param("room_id", True, str, 0, 1, u"房间id"),
        Param("net_status", True, int, 0, 1, u"网络状况"),
        Param("is_answered", True, int, 0, 1, u"是否接听"),
        Param("ring_duration", True, int, 0, 1, u"呼叫时长"),
        Param("call_duration", True, int, 0, 1, u"通话时长"),
        Param("end_time", True, int, 0, 1, u"通话结束时间"),
        Param("gift_list", False, str, 0, 1, u"送出的礼物列表"),
        Param("hangup_type", True, int, 0, 1, u"挂断原因"),
        Param("error_message", False, str, 0, 1, u"错误信息"),
        Param("call_type", True, int, 0, 1, u"房间类型"),
        Param("receive_timestamp", True, int, 0, 1, u"房间类型"),
        Param("answer_timestamp", True, int, 0, 1, u"房间类型"),
    ],description=u"用户行为统计上报")
    @login_required
    def post(self):
        call_uid = self.arg_int("call_uid")
        answer_uid = self.arg_int("answer_uid")
        price = self.arg_int("price")
        room_id = self.arg("room_id")
        net_status = self.arg_int("net_status")
        is_answered = self.arg_int("is_answered")
        ring_duration = self.arg_int("ring_duration")
        call_duration = self.arg("call_duration")
        end_time = self.arg_int("end_time")
        gift_list = self.arg("gift_list", "")
        hangup_type = self.arg_int("hangup_type")
        answer_timestamp = self.arg_int("answer_timestamp")
        receive_timestamp = self.arg_int("receive_timestamp")
        error_message = self.arg("error_message", "")
        call_type = self.arg_int("call_type")

        guid = self.arg("guid")

        ua = self.request.headers.get('User-Agent')
        uas = ua.split(";")
        if uas[2] == "iPhone" or uas[2] == "iPad":
            platform = 1
        else:
            platform = 0
        answer_timestamp = datetime.datetime.fromtimestamp(answer_timestamp)
        receive_timestamp = datetime.datetime.fromtimestamp(receive_timestamp)
        end_time = datetime.datetime.fromtimestamp(end_time)

        PhoneStat.create_phone_stat(
            call_uid=call_uid,
            answer_uid=answer_uid,
            room_id=room_id,
            answer_timestamp=answer_timestamp,
            received_timestamp=receive_timestamp,
            price=price,
            ring_duration=ring_duration,
            net_status=net_status,
            hangup_timestamp=end_time,
            error_message=error_message,
            is_answered=is_answered == 0,
            call_duration=call_duration,
            gift_list=json.loads(gift_list) if gift_list else None,
            hangup_type=hangup_type,
            call_type=call_type,
            platform=platform,
            user_agent=ua,
            answer_guid=guid,
            is_call=False
        )

        return self.write({"status": "success"})

@handler_define
class StatUserAction(BaseHandler):
    @api_define("stat user action", r'/log/user/action',[
        Param("data", True, str, "", "", description=u"用户行为统计")
    ],description=u"用户行为统计")
    def post(self):
        action = self.arg("data")
        UserAction.create_action_record(action)
        return self.write({"data":"success"})


@handler_define
class InviteShareStart(BaseHandler):
    @api_define("invite share start", "/log/share",
                [
                    Param("data", True, str, 0, "", "{'share_channel':1,'share_use':0,'count':3,'success_count':1}",
                          "分享渠道(0:微信，1：朋友圈，2:qq, 3:qq空间，4：微博), share_use：0：得钱分享，1：邀请分享,"
                          "count: 尝试分享次数， success_count:成功分享次数"),

                ], description=u"邀请好友分享")
    @login_required
    def post(self):
        user_id = int(self.current_user_id)
        guid = self.arg("guid")
        data = self.arg("data")
        share_infos = json.loads(data)

        for share_info in share_infos:
            share_channel = int(share_info.get("share_channel"))
            share_use = int(share_info.get("share_use"))
            count = int(share_info.get("count"))
            success_count = int(share_info.get("success_count"))
            ShareStat.create_invite_shareinfo(guid, user_id, share_channel, share_use, count, success_count)
        self.write({
            "status": "success"
        })



