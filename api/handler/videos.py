# coding=utf-8


from api.document.doc_tools import *
from api.view.base import *
from api.convert.convert_user import *
import hashlib
import hmac
import base64
import random
import time
import datetime
from app.customer.models.real_video_verify import RealVideoVerify
from app.customer.models.video import PrivateVideo, PrivateVideoPrice, VipWatchVideoRecord, VideoPurchaseRecord
from app.util.shumeitools.shumeitools import *
from app.customer.models.vip import UserVip, Vip
from app.customer.models.community import UserMoment
from app.util.messageque.msgsender import MessageSender
from app.customer.models.video import InviteMessage
from app.customer.models.benifit import TicketAccount
from app.customer.models.account import TradeDiamondRecord, TradeTicketRecord, Account
import international
from app.customer.models.tools import UserTools


@handler_define
class RealVideoVerifyUpload(BaseHandler):
    @api_define("real video upload", "/video/upload_verify", [
                    Param("cover_url", True, str, "", "", u"封面地址"),
                    Param("video_url", True, str, "", "", u"视频地址"),
                    Param("file_id", False, str, "", "", u"file_id"),
                ], description=u"视频认证上传")
    @login_required
    def get(self):
        cover_url = self.arg("cover_url")
        video_url = self.arg("video_url")
        file_id = self.arg("file_id", "")
        user_id = self.current_user_id
        video_verify = RealVideoVerify()
        now = datetime.datetime.now()
        video_verify.user_id = int(user_id)
        video_verify.cover_url = cover_url
        video_verify.video_url = video_url
        video_verify.feedback_reason = ""
        video_verify.create_time = now
        video_verify.update_time = now
        video_verify.status = 0
        video_verify.is_valid = 1
        video_verify.file_id = file_id
        video_verify.save()

        self.write({"status": "success"})


@handler_define
class GetVODSign(BaseHandler):
    @api_define("get vod sign", "/video/get_vod_sign",
                [], description=u"获取云点播签名")
    def get(self):
        secret_id = "AKIDrgKznR0CqJbi5If9uUt6A5pNlyrfttGe"
        secret_key = "Vq03vb8WntnVL3e3HPMAvY2LTPBpIG9w"

        time1 = int(time.time())
        time2 = int(time.time()) + 3600
        original = "secretId=%s&currentTimeStamp=%d&expireTime=%s&random=%d" % \
                   (secret_id, time1, time2, random.randint(0, 1000000))

        sign_temp = hmac.new(secret_key, original, hashlib.sha1).digest()
        sign = base64.b64encode(sign_temp + original)
        self.write({"status": "success", "sign": sign})


@handler_define
class PrivateVideoPriceList(BaseHandler):
    @api_define("private video price list", r'/video/price_list', [
    ], description=u'私房视频价格列表(1:vip才可设置  2:均可)')
    @login_required
    def get(self):
        price_list = PrivateVideoPrice.objects.filter(delete_status=1)
        data = []
        if price_list:
            for price in price_list:
                dict = {
                    "price": price.price,
                    "only_vip": price.only_vip
                }
                data.append(dict)

        self.write({"status": "success", "data": data})


@handler_define
class PrivateVideoCreate(BaseHandler):
    @api_define("Create private video", r'/video/create', [
        Param('cover_url', True, str, "", "", u'封面url'),
        Param('video_url', True, str, "", "", u'视频url'),
        Param('publish_status', False, str, "1", "", u'是否发布到动态 1:不发布  2:发布'),
        Param('desc', False, str, "", "", u'描述'),
        Param('price', True, str, "0", "", u'视频价格'),
        Param('file_id', False, str, "", "", u'file_id'),
    ], description=u'保存私房视频')
    @login_required
    def get(self):
        user_id = self.current_user_id
        user = self.current_user
        cover_url = self.arg('cover_url')
        video_url = self.arg('video_url')
        publish_status = self.arg_int('publish_status', 1)
        desc = self.arg('desc', "")
        file_id = self.arg('file_id', "")
        price = self.arg_int('price', 0)

        real_video_auth = RealVideoVerify.get_status(user_id)

        if int(real_video_auth) != 1:
            return self.write({"status": "fail", 'error': _(u"视频认证通过后才可发布私房视频")})

        code, message = PrivateVideo.check_video_count(user)
        if code == 2:
            return self.write({"status": "fail", 'error': _(message)})

        if desc:
            # 文本内容鉴黄
            ret, duration = shumei_text_spam(text=desc, timeout=1, user_id=user.id, channel="DYNAMIC_COMMENT", nickname=user.nickname,
                                             phone=user.phone, ip=self.user_ip)
            print ret
            is_pass = 0
            if ret["code"] == 1100:
                if ret["riskLevel"] == "PASS":
                    is_pass = 1
                if ret["riskLevel"] == "REJECT":
                    is_pass = 0
                if ret["riskLevel"] == "REVIEW":
                    # todo +人工审核逻辑
                    is_pass = 1
            if not is_pass:
                return self.write({'status': "fail", 'error': _(u"经系统检测,您的内容涉及违规因素,请重新编辑")})

        video = PrivateVideo()
        video.desc = desc
        video.user_id = int(user_id)
        video.cover_url = cover_url
        video.video_url = video_url
        video.price = price
        video.create_time = datetime.datetime.now()
        video.delete_status = 1
        video.show_status = 3
        video.is_valid = 1
        video.file_id = file_id
        video.save()

        user_moment = UserMoment()
        user_moment.user_id = user_id
        user_moment.like_count = 0
        user_moment.like_user_list = []
        user_moment.comment_count = 0

        user_moment.img_list = []
        user_moment.content = desc
        user_moment.create_time = datetime.datetime.now()
        user_moment.show_status = 5  # 1:展示  2:数美屏蔽  3:举报  4:数美部分屏蔽  5:数美鉴定中
        user_moment.delete_status = 1  # 1:未删除  2:删除
        user_moment.ispass = 2
        user_moment.type = 3
        user_moment.video_id = str(video.id)
        user_moment.cover_url = cover_url
        user_moment.video_url = video_url
        user_moment.price = video.price
        # 同步到动态
        if publish_status == 2:
            code, message = UserMoment.check_moment_count(user)
            if code == 2:
                return self.write({'status': "fail", 'error': _(message)})
            user_moment.is_public = 1

            # 发布私房视频 任务
            from app.customer.models.task import Task
            role = Task.get_role(user.id)
            task_identity = 0
            if role == 3:
                task_identity = 15
            if task_identity:
                MessageSender.send_do_task(user_id=user.id, task_identity=task_identity)

        else:
            user_moment.is_public = 2

        user_moment.save()

        from app_redis.user.models.user import UserRedis
        pure_id = "597ef85718ce420b7d46ce11"
        if user.is_video_auth == 1:
            if user.label:
                if pure_id in user.label:
                    user_moment.update(set__is_pure=1)
                else:
                    user_moment.update(set__is_pure=3)
            else:
                user_moment.update(set__is_pure=3)
        else:
            if UserRedis.is_target_user(user.id):
                user_moment.update(set__is_pure=2)
            else:
                user_moment.update(set__is_pure=4)



        return self.write({"status": "success"})

@handler_define
class BuyPrivateVideo(BaseHandler):
    @api_define("buy private video ", r'/video/buy_video', [
        Param('video_id', True, str, "", "", u'私房视频ID'),
    ], description=u'购买私房视频')
    @login_required
    def get(self):
        user = self.current_user
        video_id = self.arg('video_id')
        video = PrivateVideo.objects.filter(id=video_id, delete_status=1).first()
        if not video:
            return self.write({"status": "fail", "error": _(u"视频已删除")})

        to_user_id = video.user_id
        to_user = User.objects.filter(id=to_user_id).first()

        account = Account.objects.filter(user=user).first()
        if account.diamond < video.price:
            return self.write({"status": "fail", "error": _(u"余额不足")})
        try:
            old_record = VideoPurchaseRecord.objects.filter(user_id=user.id, video_id=video_id).first()
            if old_record:
                return self.write({"status": "success", "msg": "Already purchased"})
            # 用户账号余额
            account.diamond_trade_out(price=video.price, desc=u"购买私房视频, 私房视频id=%s" %
                                                              (str(video_id)), trade_type=TradeDiamondRecord.TradeTypePrivateVideo)

            user.update(
                inc__wealth_value=video.price/10,
                inc__cost=video.price,
            )

            to_user.update(
                inc__charm_value=video.price/10,
                inc__ticket=video.price
            )

            # 2. 收礼人+经验, +粒子数
            # to_user.add_experience(10)
            ticket_account = TicketAccount.objects.get(user=to_user)
            ticket_account.add_ticket(trade_type=TradeTicketRecord.TradeTypePrivateVideo,
                                      ticket=video.price, desc=u"购买私房视频, 私房视频id=%s" % (str(video_id)))

            # 购买记录
            VideoPurchaseRecord.create_record(user.id, video_id)

            return self.write({"status": "success"})
        except Exception, e:
            return self.write({"status": "fail"})


# vip 是否到达免费观看上限
@handler_define
class PrivateVideoCanWatch(BaseHandler):
    @api_define("private video delete", r'/video/can_watch', [
        Param('video_id', True, str, "", "", u'私房视频ID'),
    ], description=u'vip是否可以到达免费观看上限(1:可以观看   2:不可以观看)')
    @login_required
    def get(self):
        user_id = self.current_user_id
        video_id = self.arg("video_id")
        now = datetime.datetime.now()
        create_time = now.strftime("%Y-%m-%d")
        count = VipWatchVideoRecord.objects.filter(user_id=user_id, create_time=create_time).count()
        super_vip_count = 6
        vip_count = 2
        user_vip = UserVip.objects.filter(user_id=user_id).first()
        can_watch = 2

        buy_video_status = VideoPurchaseRecord.get_buy_status(user_id, video_id)

        # 观影券个数  观影碎片个数  每个视频所需观影碎片数
        watch_card_count, watch_card_part_count, need_part_count = UserTools.get_watch_count(user_id)

        # 今天是否看过词视频
        looked_today = VipWatchVideoRecord.objects.filter(user_id=user_id, create_time=create_time, video_id=video_id).first()
        is_looked_today = 2
        if looked_today:
            is_looked_today = 1

        if user_vip:
            vip = Vip.objects.filter(id=user_vip.vip_id).first()
            if vip.vip_type == 1:
                # 高级
                if count < vip_count or looked_today:
                    can_watch = 1
                vip_total_count = vip_count

            if vip.vip_type == 2:
                # 超级
                if count < super_vip_count or looked_today:
                    can_watch = 1
                vip_total_count = super_vip_count

            looked_count = count

            if can_watch == 1:
                # 添加观看记录
                VipWatchVideoRecord.create_record(video_id, user_id)

            return self.write({"status": "success", "can_watch": can_watch, "looked_count": looked_count,
                               "vip_total_count": vip_total_count, "buy_video_status": buy_video_status,
                               "watch_card_count": watch_card_count, "watch_card_part_count": watch_card_part_count,
                               "need_part_count": need_part_count,
                               "is_looked_today": is_looked_today})
        else:
            return self.write({"status": "success", "can_watch": can_watch, "looked_count": 0,
                               "watch_card_count": watch_card_count, "watch_card_part_count": watch_card_part_count,
                               "need_part_count": need_part_count,
                               "vip_total_count": 0, "buy_video_status": buy_video_status, "is_looked_today": is_looked_today})


@handler_define
class PrivateVideoWatchRecord(BaseHandler):
    @api_define("private video record ", r'/video/create_watch_record', [
        Param('video_id', True, str, "", "", u'私房视频ID'),
    ], description=u'vip 免费私房视频观看记录')
    @login_required
    def get(self):
        user_id = self.current_user_id
        video_id = self.arg("video_id")
        status = VipWatchVideoRecord.create_record(video_id, user_id)
        if status:
            return self.write({"status": "success"})
        else:
            return self.write({"status": "fail"})


# 私房视频删除
@handler_define
class PrivateVideoDelete(BaseHandler):
    @api_define("private video delete", r'/video/delete_video', [
        Param('video_id', True, str, "", "", u'私房视频ID'),
    ], description=u'私房视频删除')
    @login_required
    def get(self):
        video_id = self.arg('video_id')
        user_id = self.current_user_id
        status = PrivateVideo.delete_video(video_id, user_id)
        if status:
            self.write({"status": "success"})


# 私房视频列表
@handler_define
class PrivateVideoList(BaseHandler):
    @api_define("private video list", r'/video/list', [
        Param('user_id', True, str, "", "", u' user_id'),
    ], description=u'私房视频列表')
    @login_required
    def get(self):
        data = []
        current_user_id = self.current_user_id
        user_id = self.arg("user_id")

        if int(user_id) == int(current_user_id):
            videos = PrivateVideo.objects.filter(show_status__ne=2, user_id=user_id, delete_status=1).order_by("-create_time")
        else:
            videos = PrivateVideo.objects.filter(show_status=1, user_id=user_id, delete_status=1).order_by("-create_time")

        if videos:
            for video in videos:
                moment = UserMoment.objects.filter(video_id=str(video.id)).order_by("-create_time").first()
                if moment:
                    dic = convert_user_moment(moment)
                    buy_video_status = VideoPurchaseRecord.get_buy_status(current_user_id, moment.video_id)
                    dic["buy_video_status"] = buy_video_status

                    if user_id:
                        like_user_list = moment.like_user_list
                        if int(user_id) in like_user_list:
                            is_liked = 1
                        else:
                            is_liked = 0
                        dic["is_liked"] = is_liked
                        data.append(dic)
                    else:
                        dic["is_liked"] = 0
                        data.append(dic)
                    dic["check_real_video"] = RealVideoVerify.get_status(moment.user_id)

        self.write({"status": "success", "data": data})


# 认证系统消息(视频认证, 播主认证)
@handler_define
class InviteMessageSend(BaseHandler):
    @api_define("video  verify_message", r'/video/invite_message', [
        Param('type', True, str, "", "", u'1: 播主认证  2:视频认证  3:上传照片 4:上传视频'),
        Param('user_id', True, str, "", "", u'邀请认证id'),
    ], description=u'邀请认证消息')
    @login_required
    def get(self):
        type = self.arg_int('type')
        user_id = self.arg("user_id")
        user = User.objects.filter(id=user_id).first()
        desc = ""
        desc_new = ""
        if type == 1:
            desc = u"<html><p>" + _(u"%s 邀请您参加播主认证" % self.current_user.nickname) + u"</p></br></html>"
            desc_new = _(u"%s 邀请您参加播主认证" % self.current_user.nickname)
        elif type == 2:
            desc = u"<html><p>" + _(u"%s 邀请您参加视频认证" % self.current_user.nickname) + u"</p></br></html>"
            desc_new = _(u"%s 邀请您参加视频认证" % self.current_user.nickname)
        elif type == 3:
            desc = u"<html><p>" + _(u"%s 邀请您上传照片" % self.current_user.nickname) + u"</p></br></html>"
            desc_new = _(u"%s 邀请您上传照片" % self.current_user.nickname)
        elif type == 4:
            desc = u"<html><p>" + _(u"%s 邀请您上传视频" % self.current_user.nickname) + u"</p></br></html>"
            desc_new = _(u"%s 邀请您上传视频" % self.current_user.nickname)

        if desc:
            message = InviteMessage.objects.filter(from_user_id=self.current_user.id, to_user_id=user_id, type=int(type)).first()
            if message:
                return self.write({"status": "fail", "error": _(u"您已发送过邀请")})

            ua = self.request.headers.get('User-Agent')
            ua_version = ua.split(";")[1]
            if ua_version and ua_version < "2.4.0":
                MessageSender.send_system_message(user.sid, desc)
            else:
                MessageSender.send_system_message_v2(to_user_id=user.sid, content=desc_new)
            InviteMessage.create_invite_message(self.current_user.id, user_id, type)
            return self.write({"status": "success"})


@handler_define
class VideoTask(BaseHandler):
    @api_define("private video delete", r'/video/video_task', [
        Param('video_id', True, str, "", "", u'私房视频ID'),
    ], description=u'观看私房视频 任务')
    @login_required
    def get(self):
        video_id = self.arg('video_id')
        user_id = self.current_user_id

        from app.customer.models.task import Task
        role = Task.get_role(user_id)
        task_identity = 0
        if role == 1:
            task_identity = 43

        if task_identity:
            vip_count = VipWatchVideoRecord.objects.filter(video_id=video_id, user_id=user_id).count()
            buy_count = VideoPurchaseRecord.objects.filter(video_id=video_id, user_id=user_id).count()
            count = vip_count + buy_count
            if count >= 2:
                MessageSender.send_do_task(user_id=user_id, task_identity=task_identity)



