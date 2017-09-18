# coding=utf-8

import datetime
# from app.customer.models.tools import *
from app.customer.models.first_charge_activity import *
from app.customer.models.account import *
from app.customer.models.user import *
from app.customer.models.friend import Friend
from app.customer.models.follow_user import FriendUser


# now = datetime.datetime.now()
# date = now.strftime('%Y年%m月%d日')
# print date

def sync_friend():
    friends = Friend.objects.filter(friend_status=2)
    for friend in friends:
        create_time = friend.update_time
        user_id = friend.user_id
        friend_id = friend.friend_id

        db_friend_user = FriendUser.objects.filter(from_id=user_id, to_id=friend_id).first()
        if not db_friend_user:
            friend_user = FriendUser()
            friend_user.create_time = create_time
            friend_user.from_id = user_id
            friend_user.to_id = friend_id
            friend_user.save()


def test():

    order = TradeBalanceOrder.objects.filter(id="58b52d4471bc820dc0188bb6").first()
    user = order.user

    # 首充活动
    act = FirstChargeActivity.objects.filter(temp_activity_type=1).first()
    now = datetime.datetime.now()

    #  判断是否活动有效
    if act:
        end_time = act.end_time
        days = (end_time - now).days
        if days < 0:
            return True

    #  判断是否是后台充值
    if order.fill_in_type == 6:
        return True

    #判断首充
    starttime = now.strftime("%Y-%m-%d 00:00:00")
    endtime = now.strftime('%Y-%m-%d 23:59:59')
    order_count = TradeBalanceOrder.objects.filter(status='1', user=user, buy_time__gte=starttime,
                                                   buy_time__lte=endtime,).count()
    if order_count > 1:
        return True

    money = order.money
    FirstChargeActivity.create_reward(user, money)


# dic1 = {
#     "master_key": "2",
#     "bottle": "2",
#     "clairvoyant": "5"
# }
#
# s = str(dic1)
# print s
# d1 = eval(s)
# print d1.get("bottle")
# print s

# now = datetime.datetime.now()
# end_time = now + datetime.timedelta(days=30)
# print end_time

# TOOLS_TYPE = (
#     (0, u'万能钥匙'),
#     (1, u'漂流瓶'),
#     (2, u'千里眼'),
# )
# print TOOLS_TYPE[2][0]

# now = datetime.datetime.now()
# yesterday = now - datetime.timedelta(days=1)
# yesterday_start = yesterday.strftime("%Y-%m-%d 00:00:00")
# yesterday_end = yesterday.strftime("%Y-%m-%d 23:59:59")
#
# print yesterday_start
# print yesterday_end

# def init_activity():
#     s = "2017-07-03 00:00:00"
#     e = "2017-07-10 23:59:59"
#     s_time = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
#     e_time = datetime.datetime.strptime(e, "%Y-%m-%d %H:%M:%S")
#     activity = ToolsActivity()
#     activity.tools_data = "{u'1': u'1', u'0': u'1'}"
#     activity.name = "test2"
#     activity.create_time = datetime.datetime.now()
#     activity.delete_status = 1
#     activity.start_time = s_time
#     activity.end_time = e_time
#     activity.start_hms = "14:00:00"
#     activity.end_hms = "15:59:59"
#     activity.role = "1,2,3,"  #1: 新主播 2：老主播 3：用户(多个逗号分隔)
#     activity.save()

# now = datetime.datetime.now()
# hour = now.hour
# minute = now.minute
# second = now.second
#
# if hour < 10:
#     hour_str = '0'+str(hour)
# else:
#     hour_str = str(hour)
#
# if minute < 10:
#     minute_str = '0'+str(minute)
# else:
#     minute_str = str(minute)
#
# if second < 10:
#     second_str = '0'+str(second)
# else:
#     second_str = str(second)
#
# print hour_str + ":" + minute_str + ":" + second_str

from app.customer.models.index_column import IndexColumn
def init_index_colum():
    column = IndexColumn()
    column.name = "热门推荐"
    column.column_type = 1
    column.delete_status = 1
    column.save()

    column2 = IndexColumn()
    column2.name = "新人驾到"
    column2.column_type = 2
    column2.delete_status = 1
    column2.save()

import time

def time_test():
    date_time = datetime.datetime(2017, 7, 8)
    print get_time(date_time)


def get_time(date_time):
    now = datetime.datetime.now()
    second = time.mktime(now.timetuple()) - time.mktime(date_time.timetuple())

    if second <= 0:
        second = 0

    #  微信格式
    if second == 0:
        interval = "刚刚"
    elif second < 30:
        interval = str(second) + "秒以前"
    elif second >= 30 and second < 60:
        interval = "半分钟前"
    elif second >= 60 and second < 60 * 60:  #  大于1分钟 小于1小时
        minute = int(second / 60)
        interval = str(minute) + "分钟前"
    elif second >= 60 * 60 and second < 60 * 60 * 24:  #  大于1小时 小于24小时
        hour = int((second / 60) / 60)
        interval = str(hour) + "小时前"
    elif second >= 60 * 60 * 24 and second <= 60 * 60 * 24 * 2: #  大于1D 小于2D
        interval = "昨天" + date_time.strftime('%Y-%m-%d %H:%M')
    elif second >= 60 * 60 * 24 * 2 and second <= 60 * 60 * 24 * 7:  #  大于2D小时 小于 7天
        day = int(((second / 60) / 60) / 24)
        interval = str(day) + "天前"
    elif second <= 60 * 60 * 24 * 365 and second >= 60 * 60 * 24 * 7:  #  大于7天小于365天
        interval = date_time.strftime('%Y-%m-%d %H:%M:%S')
    elif second >= 60 * 60 * 24 * 365:  #  大于365天
        interval = date_time.strftime('%Y-%m-%d %H:%M:%S')
    else:
        interval = "0"
    return interval

from app.picture.models.picture import PictureInfo
def update_pic():
    pics = PictureInfo.objects.all()
    for pic in pics:
        pic.update(set__show_status=1)


def video_price():
    from app.customer.models.video import PrivateVideoPrice
    video1 = PrivateVideoPrice()
    video1.price = 0
    video1.only_vip = 2
    video1.delete_status = 1
    video1.save()

    video2 = PrivateVideoPrice()
    video2.price = 100
    video2.only_vip = 2
    video2.delete_status = 1
    video2.save()

    video3 = PrivateVideoPrice()
    video3.price = 200
    video3.only_vip = 2
    video3.delete_status = 1
    video3.save()

    video4 = PrivateVideoPrice()
    video4.price = 300
    video4.only_vip = 1
    video4.delete_status = 1
    video4.save()

def update_usermoment():
    from app.customer.models.community import UserMoment
    UserMoment.objects.update(set__is_public=1)


def init_vip_privilege():
    from app.customer.models.vip import VipPrivilege

    p1 = VipPrivilege.create("专属标识", "https://heydopic-10048692.image.myqcloud.com/1502851151_93e44a1151bf39ef5a2ec454547cbe69",
                             "会员期间内，VIP用户将拥有专属标识，不同VIP等级显示的表示也有区分，让你在各个位置脱颖而出，时时刻刻展现尊贵的VIP身份。",
                             "https://heydopic-10048692.image.myqcloud.com/1502877604_695d703997c7bbc8e36d13cdcf55dfb9",
                             1, 1)

    p2 = VipPrivilege.create("免费看私房视频", "https://heydopic-10048692.image.myqcloud.com/1502853017_e66f49af3710e9b5f70ee779a733052a",
                             "会员期间内，高级VIP用户每天可以免费观看认证用户的2个私房视频，超级VIP用户可以免费观看认证用户的6个私房视频。【私房视频单价至少100钻石】 ",
                             "https://heydopic-10048692.image.myqcloud.com/1502952284_51694056c14e2d793ebe6166b4219ecb",
                             1, 2)

    p3 = VipPrivilege.create("免费看精华照片", "https://heydopic-10048692.image.myqcloud.com/1502853178_e72e4cfc84765dd1b185bf4de659fdf7",
                             "会员期间内，VIP用户可以免费查看认证用户的精华照片，是所有认证用户哦。【非VIP用户无法查看的哟】 ",
                             "https://heydopic-10048692.image.myqcloud.com/1502952230_1fe35448aa54aac4ba8795529c5c171b",
                             1, 3)

    p4 = VipPrivilege.create("充值送钻石", "https://heydopic-10048692.image.myqcloud.com/1502878381_011df750553ff2a6a7be45fefaf6d33a",
                             "会员期间内，超级VIP用户充值钻石，额外赠送钻石奖励，充值越多送得越多【高级VIP用户无此特权】 ",
                             "https://heydopic-10048692.image.myqcloud.com/1503047218_dbd07208a0eef1d10664e30063a27728",
                             1, 4)

    p5 = VipPrivilege.create("私信图片功能", "https://heydopic-10048692.image.myqcloud.com/1502878417_52ede4fde4d7590dfec85408bfb48b94",
                             "会员期间内，VIP用户与好友私信聊天室，可以任意发送图片 ，不受任何限制。【非VIP用户无法使用此功能】 ",
                             "https://heydopic-10048692.image.myqcloud.com/1502878489_2ba1a5451288fc5ad0fe5d5d5b3b69bf",
                             1, 5)

    p6 = VipPrivilege.create("私信语音功能", "https://heydopic-10048692.image.myqcloud.com/1502878591_e24d0d2a3107ed66de49a994d2d35df8",
                             "会员期间内，VIP用户与好友私信聊天室，可以发送语音短信功能，不受任何限制。【非VIP用户无法使用此功能】 ",
                             "https://heydopic-10048692.image.myqcloud.com/1502878559_ed590592425a62fab034c935188a89e1",
                             1, 6)

    p7 = VipPrivilege.create("门禁卡", "https://heydopic-10048692.image.myqcloud.com/1502881087_2ed91aa1f4921b9950843ab5aef77ffb",
                             "会员期间内，高级VIP用户每天可以免费获得10个门禁卡，使用门禁卡可以和10个不同的用户进行免费聊天；超级VIP用户每天可以免费获得20个门禁卡，使用门禁卡可以和20个不同用户进行免费聊天；1个门禁卡只针对1次会话有效。【门禁卡单价100钻石】 ",
                             "https://heydopic-10048692.image.myqcloud.com/1502881137_d358ebda348c45b6547c70ecd4cca716",
                             1, 7)

    p8 = VipPrivilege.create("漂流瓶", "https://heydopic-10048692.image.myqcloud.com/1502881243_660df9c12f6d15062ea33fa480c0ced9",
                             "会员期间内，高级VIP用户每天可以免费获得5个漂流瓶，超级VIP用户每天可以免费获得10个漂流瓶；每次使用漂流瓶，可以选择向100个男性或者女性用户发送你的问候语，可以更大几率获得更多异性的青睐。【漂流瓶单价1000钻石】 ",
                             "https://heydopic-10048692.image.myqcloud.com/1502881188_e6a31d8044e6a68ff21b94d710e2a60b",
                             1, 8)

    p9 = VipPrivilege.create("千里眼", "https://heydopic-10048692.image.myqcloud.com/1502881278_b0b0b30701e3fae8c5392afbffaebd37",
                             "会员期间内，高级VIP用户每天可以免费获得3个千里眼，超级VIP用户每天可以免费获得5个千里眼；每次使用千里眼，可以查看5名在线土豪用户信息，让你可以更大几率与土豪交朋友。【千里眼单价1000钻石】 ",
                             "https://heydopic-10048692.image.myqcloud.com/1502881644_488c832d20672bd50ea1c4f2eac79fdb",
                             1, 9)

def fix_friend():
    from app.customer.models.follow_user import FollowUser
    users = FriendUser.objects.all()
    if users:
        for user in users:
            from_id = user.from_id
            to_id = user.to_id
            follow_user = FollowUser.objects.filter(from_id=from_id, to_id=to_id).first()
            if not follow_user:
                u = FollowUser()
                u.from_id = from_id
                u.to_id = to_id
                u.create_time = user.create_time
                u.save()


def follow_unique():
    from app.customer.models.follow_user import FollowUser
    follower_users = FollowUser.objects.all()
    for follow in follower_users:
        unique_code = str(follow.from_id) + "_" + str(follow.to_id)
        follow.update(set__unique_code=unique_code)


def fix_user():
    from app.customer.models.user import User
    from app.customer.models.real_video_verify import RealVideoVerify
    users = User.objects.all()
    for user in users:
        status = RealVideoVerify.get_status(user.id)
        if status == 1:
            user.update(set__is_video_auth=1)
        else:
            if user.is_video_auth == 1:
                desc = u"<html><p>" + _(u'由于您未进行视频认证，将取消您的播主资格，如想再次成为视频播主，请进行申请视频认证，并添加审核人员微信: "honeynnm" ') + u"</p></html>"
                MessageSender.send_system_message(user.id, desc)
                user.update(set__is_video_auth=4)

def init_topic():
    from app.customer.models.community import MomentTopic
    now = datetime.datetime.now()

    topic = MomentTopic()
    topic.topic_type = 1
    topic.name = "第一美"
    topic.hot = 1
    topic.order = 1
    topic.delete_status = 1
    topic.create_time = now
    topic.save()

    topic2 = MomentTopic()
    topic2.topic_type = 2
    topic2.name = "国足二进世界杯"
    topic2.hot = 1
    topic2.order = 2
    topic2.delete_status = 1
    topic2.create_time = now
    topic2.save()

    topic3 = MomentTopic()
    topic3.topic_type = 3
    topic3.name = "蜘蛛小侠"
    topic3.hot = 1
    topic3.order = 3
    topic3.delete_status = 1
    topic3.create_time = now
    topic3.save()

    topic4 = MomentTopic()
    topic4.topic_type = 4
    topic4.name = "春风十里"
    topic4.hot = 2
    topic4.order = 0
    topic4.delete_status = 1
    topic4.create_time = now
    topic4.save()












