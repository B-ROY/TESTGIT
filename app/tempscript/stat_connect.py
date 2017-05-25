# coding=utf-8
import datetime

from app.stat.models.phone_stat import PhoneStat
"""
    计算新版接通率 

"""


def gen_connect_csv(start_time, end_time):
    phone_stats = PhoneStat.objects.all()
    file_name_call = "stat_connect_call.csv"
    file_name_answer = "stat_connect_answer.csv"
    """
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
    """

    with open(file_name_call, "w") as f:
        with open(file_name_answer, "w") as f1:
            f.write("call_id,answer_uid,room_id,net_status,source,call_timestamp,received_timestamp,"
                    "answer_timestamp,price,call_type,call_guid,answer_guid,hangup_type,hangup_timestamp,ring_duration,"
                    "call_duration,is_answered,error_message,user_agent,channel,app_version,platform,is_call,gift_list" + "\n")
            f1.write("call_id,answer_uid,room_id,net_status,source,call_timestamp,received_timestamp,"
                    "answer_timestamp,price,call_type,call_guid,answer_guid,hangup_type,hangup_timestamp,ring_duration,"
                    "call_duration,is_answered,error_message,user_agent,channel,app_version,platform,is_call,gift_list" + "\n")

            for s in phone_stats:
                if s.is_call:
                    f.write(str(s.call_uid) + ","
                            + str(s.answer_uid) + ","
                            + str(s.room_id) + ","
                            + str(s.net_status) + ","
                            + str(s.source) + ","
                            + str(s.call_timestamp) + ","
                            + str(s.received_timestamp) + ","
                            + str(s.answer_timestamp) + ","
                            + str(s.price) + ","
                            + str(s.call_type) + ","
                            + (str(s.call_guid) if s.call_guid else "-") + ","
                            + (str(s.answer_guid) if s.answer_guid else "-") + ","
                            + str(s.hangup_type) + ","
                            + str(s.hangup_timestamp) + ","
                            + str(s.ring_duration) + ","
                            + str(s.call_duration) + ","
                            + str(s.is_answered) + ","
                            + (str(s.error_message).replace(",", "-") if s.error_message else "-") + ","
                            + str(s.user_agent).split(";")[2] + ","# 加上逗号正则
                            + str(s.channel) + ","
                            + (str(s.app_version) if s.app_version else "-") + ","
                            + (str(s.platform) if s.platform else "-") + ","
                            + str(s.is_call) + ","
                            + str(s.gift_list).replace(",", "-")
                            + "\n"
                            )
                else:
                    f1.write(str(s.call_uid) + ","
                            + str(s.answer_uid) + ","
                            + str(s.room_id) + ","
                            + str(s.net_status) + ","
                            + str(s.source) + ","
                            + str(s.call_timestamp) + ","
                            + str(s.received_timestamp) + ","
                            + str(s.answer_timestamp) + ","
                            + str(s.price) + ","
                            + str(s.call_type) + ","
                            + (str(s.call_guid) if s.call_guid else "-") + ","
                            + (str(s.answer_guid) if s.answer_guid else "-") + ","
                            + str(s.hangup_type) + ","
                            + str(s.hangup_timestamp) + ","
                            + str(s.ring_duration) + ","
                            + str(s.call_duration) + ","
                            + str(s.is_answered) + ","
                            + (str(s.error_message).replace(",", "-") if s.error_message else "-") + ","
                            + str(s.user_agent).split(";")[2] + ","  # 加上逗号正则
                            + str(s.channel) + ","
                            + (str(s.app_version) if s.app_version else "-") + ","
                            + (str(s.platform) if s.platform else "-") + ","
                            + str(s.is_call) + ","
                            + str(s.gift_list).replace(",", "-")
                            + "\n"
                            )


def compute():
    start_time = datetime.datetime(2017, 5, 10)
    end_time = datetime.datetime(2017,5, 12)
    gen_connect_csv(start_time=start_time, end_time=end_time)
    pass


if __name__ == '__main__':
    compute()