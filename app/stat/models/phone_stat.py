# coding=utf-8
from mongoengine import *
import datetime


class PhoneStat(Document):
    SOURCE = [
        (0, u"热门个人页"),
        (1, u'首页列表个人页'),
        (2, u'在线列表个人页'),
        (3, u'好友列表个人页'),
        (4, u"好友申请个人页"),
        (5, u"好友设置个人页"),
        (6, u"好友广告个人页"),
        (7, u"好友聊天个人页"),
        (8, u"邀请个人页"),
        (9, u"我也不知道什么页"),
        (11, u"翻牌子"),
        (50, u"聊天页"),
        (99, u"其它"),
    ]

    NET_STATUS = [
        (0, "无网"),
        (1, "2G"),
        (2, "3G"),
        (3, "4G"),
        (4, "LTE"),
        (5, "Wifi"),
    ]

    CALL_TYPE = [
        (0, u"语音"),
        (1, u"视频")
    ]

    HANGUP_TYPE = [
        (0, u"拨打人挂断"),
        (1, u'被拨打人拒绝'),
        (2, u'拨打时间超时'),
        (3, u'声网报错'),
        (4, u"通话中拨打人挂断"),
        (5, u"通话中被拨打人挂断"),
        (6, u"拨打人余额不足"),
        (99, u"其他原因"),
    ]

    IS_ANSWER = [
        (0, u"未接通"),
        (1, u'已接通'),
    ]

    call_uid = IntField(verbose_name=u"呼叫id")
    answer_uid = IntField(verbose_name=u"主播id")

    room_id = StringField(verbose_name=u"房间ID")

    net_status = IntField(verbose_name=u"网络状态", choices=NET_STATUS)

    source = IntField(verbose_name=u"来源", choices=SOURCE)

    call_timestamp = DateTimeField(verbose_name=u"呼叫时间")
    received_timestamp = DateTimeField(verbose_name=u"开始响铃时间")
    answer_timestamp = DateTimeField(verbose_name=u"接听时间")

    price = IntField(verbose_name=u"通话价格")

    call_type = IntField(verbose_name=u"通话类型", choices=CALL_TYPE)

    call_guid = StringField(verbose_name=u"拨打者guid")
    answer_guid = StringField(verbose_name=u"接听者guid")

    hangup_type = IntField(verbose_name=u"挂断原因",choices=HANGUP_TYPE)
    hangup_timestamp = DateTimeField(verbose_name=u"挂断时间")

    ring_duration = IntField(verbose_name=u"响铃时长")
    call_duration = IntField(verbose_name=u"通话时长")

    is_answered = BooleanField(verbose_name=u"是否接听")

    error_message = StringField(verbose_name=u"错误信息")

    #user_agent中的内容 和gift_list就不区分call和answer了
    user_agent = StringField(verbose_name=u"请求ua")
    channel = StringField(verbose_name=u"渠道")
    app_version = StringField(verbose_name=u"app版本")
    platform = IntField(verbose_name=u"platform",)
    is_call = BooleanField(verbose_name=u"用户or主播")
    gift_list = ListField(verbose_name=u"礼物列表")
    record_time = DateTimeField(verbose_name=u'记录时间')

    @classmethod
    def create_phone_stat(cls,call_uid="", answer_uid="",room_id="",net_status=0, source=0,call_timestamp=datetime.datetime.fromtimestamp(0),
                          received_timestamp=datetime.datetime.fromtimestamp(0), answer_timestamp=datetime.datetime.fromtimestamp(0),price=10,call_type=0, call_guid="",
                          answer_guid="", hangup_type=0, hangup_timestamp=datetime.datetime.fromtimestamp(0), ring_duration=0, call_duration=0,
                          is_answered=False, user_agent="", channel="", app_version="", platform=0, is_call=True,
                          gift_list=None,error_message=""):

        phone_stat = cls(
            call_uid=call_uid,
            answer_uid=answer_uid,
            room_id=room_id,
            net_status=net_status,
            source=source,
            call_timestamp=call_timestamp,
            received_timestamp=received_timestamp,
            answer_timestamp=answer_timestamp,
            price=price,
            call_type=call_type,
            call_guid=call_guid,
            answer_guid=answer_guid,
            hangup_type=hangup_type,
            hangup_timestamp=hangup_timestamp,
            ring_duration=ring_duration,
            call_duration=call_duration,
            is_answered=is_answered,
            user_agent=user_agent,
            channel=channel,
            app_version=app_version,
            platform=platform,
            is_call=is_call,
            gift_list=gift_list,
            error_message=error_message,
            record_time=datetime.datetime.now()
        )
        phone_stat.save()


class UserAction(Document):

    action = StringField(verbose_name=u"用户行为记录")

    @classmethod
    def create_action_record(cls, data):
        cls(action=data).save()