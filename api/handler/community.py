#coding=utf-8
import datetime

from api.document.doc_tools import *
from api.view.base import *
from django.conf import settings
from api.convert.convert_user import *
import time
from app.customer.models.user import *
from app.customer.models.community import UserMoment, UserMomentLook, UserComment, AboutMeMessage
from app.util.shumeitools.shumeitools import *
from app.customer.models.shumeidetect import *
from app.customer.models.follow_user import FollowUser, FriendUser
from app.customer.models.black_user import BlackUser
from app.customer.models.vip import UserVip, Vip
from app.customer.models.video import VideoPurchaseRecord, VipWatchVideoRecord, PrivateVideo
from app.customer.models.real_video_verify import RealVideoVerify
import international


# 发布社区动态
@handler_define
class CreateMoment(BaseHandler):
    @api_define("Create community", r'/community/create', [
        Param('picture_urls', False, str, "", "", u'图片url, 多个逗号相隔'),
        Param('content', False, str, "", "", u'社区动态文字内容')
    ], description=u'发布社区动态')
    @login_required
    def post(self):
        user = self.current_user
        picture_urls = self.arg('picture_urls', "")
        content = self.arg('content', "")
        if not picture_urls and not content:
            return self.write({'status': "fail", 'error': _(u"内容图片均为空")})

        code, message = UserMoment.check_moment_count(user)
        if code == 2:
            return self.write({'status': "fail", 'error': _(message)})

        if content:
            if settings.INTERNATIONAL_TYPE == 86:
                # 文本内容鉴黄
                ret, duration = shumei_text_spam(text=content, timeout=1, user_id=user.id, channel="DYNAMIC_COMMENT", nickname=user.nickname,
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
            else:
                is_pass = 1
            if not is_pass:
                return self.write({'status': "fail",
                                   'error': _(u"经系统检测,您的内容涉及违规因素,请重新编辑")})
        UserMoment.create(user.id, picture_urls, content)
        self.write({"status": "success"})

@handler_define
class DeleteMoment(BaseHandler):
    @api_define("delete community", r'/community/delete', [
        Param('moment_id', True, str, "", "", u'社区动态id')
    ], description=u'删除社区动态')
    @login_required
    def get(self):
        user = self.current_user
        moment_id = self.arg('moment_id', "")
        user_moment = UserMoment.objects.filter(id=moment_id).first()
        if int(user_moment.user_id) == int(user.id):
            user_moment.delete_status = 2
            user_moment.save()
            if int(user_moment.type) == 3:
                # 私房视频也要修改状态
                video_id = user_moment.video_id
                video = PrivateVideo.objects.filter(id=video_id).first()
                if video:
                    if int(video.user_id) == int(user.id):
                        video.update(set__delete_status=2)
        self.write({"status": "success"})


@handler_define
class MomentList(BaseHandler):
    @api_define("community list", r'/community/list', [
        Param('list_type', True, str, "", "", u'1: 我的动态   2:我的关注动态   3:其他用户动态'),
        Param('show_user_id', False, str, "", "", u'展示的用户id (list_type = 3 时需要传入)'),
        Param('page', True, str, "1", "1", u'page'),
        Param('page_count', True, str, "10", "10", u'page_count'),
    ], description=u'(我的/关注/其他用户)社区动态列表')
    @login_required
    def get(self):
        user = self.current_user
        user_id = self.current_user_id
        list_type = self.arg_int("list_type")
        show_user_id = self.arg_int("show_user_id", 0)
        page = self.arg_int('page')
        page_count = self.arg_int('page_count')
        data = []

        if list_type == 1:
            # 我的动态
            moments = UserMoment.objects.filter(user_id=user.id, show_status__ne=2, delete_status=1, type=1).order_by("-create_time")[(page - 1) * page_count:page * page_count]
        elif list_type == 2:
            # 我的关注动态
            follow_users = FollowUser.objects.filter(from_id=user.id)
            friend_users = FriendUser.objects.filter(from_id=user.id)
            user_ids = []
            if follow_users:
                for follow_user in follow_users:
                    fo_uid = follow_user.to_id
                    if fo_uid not in user_ids:
                        user_ids.append(fo_uid)
            if friend_users:
                for friend_user in friend_users:
                    fr_uid = friend_user.to_id
                    if fr_uid not in user_ids:
                        user_ids.append(fr_uid)

            moments = UserMoment.objects.filter(user_id__in=user_ids, show_status__in=[1, 3, 4], delete_status=1, type=1).order_by("-create_time")[(page - 1) * page_count:page * page_count]
        elif list_type == 3:
            # 临时加一个 判断我的. 稍后客户端把lsit_type修复
            if show_user_id == int(user_id):
                moments = UserMoment.objects.filter(user_id=user.id, show_status__ne=2, delete_status=1, type=1).order_by("-create_time")[(page - 1) * page_count:page * page_count]
            else:
                # 其他用户动态
                moments = UserMoment.objects.filter(user_id=show_user_id, show_status__in=[1, 3, 4], delete_status=1, type=1).order_by("-create_time")[(page - 1) * page_count:page * page_count]

        if moments:
            for moment in moments:
                like_user_list = moment.like_user_list
                dic = convert_user_moment(moment)
                if int(user_id) in like_user_list:
                    is_liked = 1
                else:
                    is_liked = 0
                dic["is_liked"] = is_liked
                data.append(dic)

        self.write({"status": "success", "data": data})



@handler_define
class MomentListV3(BaseHandler):
    @api_define("community list_v3", r'/community/list_v3', [
        Param('list_type', True, str, "", "", u'1: 我的动态   2:我的关注动态   3:其他用户动态'),
        Param('show_user_id', False, str, "", "", u'展示的用户id (list_type = 3 时需要传入)'),
        Param('page', True, str, "1", "1", u'page'),
        Param('page_count', True, str, "10", "10", u'page_count'),
    ], description=u'(我的/关注/其他用户)社区动态列表_V3')
    @login_required
    def get(self):
        user = self.current_user
        user_id = self.current_user_id
        list_type = self.arg_int("list_type")
        show_user_id = self.arg_int("show_user_id", 0)
        page = self.arg_int('page')
        page_count = self.arg_int('page_count')
        data = []

        if list_type == 1:
            # 我的动态
            moments = UserMoment.objects.filter(user_id=user.id, show_status__ne=2, delete_status=1, is_public=1).order_by("-create_time")[(page - 1) * page_count:page * page_count]
        elif list_type == 2:
            # 我的关注动态
            follow_users = FollowUser.objects.filter(from_id=user.id)
            friend_users = FriendUser.objects.filter(from_id=user.id)
            user_ids = []
            if follow_users:
                for follow_user in follow_users:
                    fo_uid = follow_user.to_id
                    if fo_uid not in user_ids:
                        user_ids.append(fo_uid)
            if friend_users:
                for friend_user in friend_users:
                    fr_uid = friend_user.to_id
                    if fr_uid not in user_ids:
                        user_ids.append(fr_uid)

            moments = UserMoment.objects.filter(user_id__in=user_ids, show_status__in=[1, 3, 4], delete_status=1, is_public=1).order_by("-create_time")[(page - 1) * page_count:page * page_count]
        elif list_type == 3:
            # 临时加一个 判断我的. 稍后客户端把lsit_type修复
            if show_user_id == int(user_id):
                moments = UserMoment.objects.filter(user_id=user.id, show_status__ne=2, delete_status=1, is_public=1).order_by("-create_time")[(page - 1) * page_count:page * page_count]
            else:
                # 其他用户动态
                moments = UserMoment.objects.filter(user_id=show_user_id, show_status__in=[1, 3, 4], delete_status=1, is_public=1).order_by("-create_time")[(page - 1) * page_count:page * page_count]

        if moments:
            for moment in moments:
                like_user_list = moment.like_user_list
                dic = convert_user_moment(moment)
                if int(user_id) in like_user_list:
                    is_liked = 1
                else:
                    is_liked = 0
                dic["is_liked"] = is_liked
                if moment.type == 3:
                    buy_video_status = VideoPurchaseRecord.get_buy_status(user_id, moment.video_id)
                    dic["buy_video_status"] = buy_video_status

                dic["check_real_video"] = RealVideoVerify.get_status(moment.user_id)
                data.append(dic)

        self.write({"status": "success", "data": data})

@handler_define
class MomentList(BaseHandler):
    @api_define("index community list", r'/community/index_list', [
        Param('page', True, str, "1", "1", u'page'),
        Param('page_count', True, str, "10", "10", u'page_count'),
    ], description=u'首页社区动态列表')
    def get(self):
        data = []
        page = self.arg_int('page')
        user_id = self.current_user_id

        page_count = self.arg_int('page_count')
        moments = UserMoment.objects.filter(show_status__in=[1, 3, 4], delete_status=1, type=1).order_by("-create_time")[(page - 1) * page_count:page * page_count]
        if moments:
            for moment in moments:
                if moment:
                    dic = convert_user_moment(moment)
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

        self.write({"status": "success", "data": data})

@handler_define
class MomentListV3(BaseHandler):
    @api_define("index community list_v3", r'/community/index_list_v3', [
        Param('page', True, str, "1", "1", u'page'),
        Param('page_count', True, str, "10", "10", u'page_count'),
    ], description=u'首页社区动态列表_v3(私房视频, 相册等动态)')
    def get(self):
        data = []
        page = self.arg_int('page')
        user_id = self.current_user_id

        page_count = self.arg_int('page_count')
        ua = self.request.headers.get('User-Agent')
        uas = ua.split(";")
        app_name = uas[0]
        momentsid =["599d16092040e46ae1243870","599d3bb92040e438a3f9b4fc","599d193c2040e46ae2243880",
                    "599d05672040e46ae224386e","599d1b7b2040e46ae324388c","599d1eda2040e46ae324389b",
                    "599d2e402040e438a1f9b4cc","599d30e22040e438a2f9b4cf","599d33b72040e438a1f9b4d0",
                    "599d36252040e438a2f9b4d5","599d4ebc2040e438a3f9b539","599d3d072040e438a2f9b4f3",
                    "599d46fb2040e438a1f9b525","599d48252040e438a3f9b52a","599d48fe2040e438a3f9b52f",
                    "599d4a6b2040e438a2f9b535","599d52342040e438a2f9b542","59968acb18ce427fa73c9d3b",
                    "5996a20b18ce427fa73c9d54","5996a73d18ce427fa83c9d96","5996b9e318ce427fa83c9db5",
                    "599d45c32040e438a1f9b516"]
        if app_name == "yeseyueai":
            momentsid =['599e40402040e438a3f9b552',
                        '599e42242040e438a3f9b55a',
                        '599e446d2040e438a3f9b567',
                        '599e4ac32040e43f0ef9b4dc',
                        '599e678b2040e438a3f9b576',
                        '599e69342040e438a3f9b57b',
                        '599e6d992040e438a3f9b586',
                        '599e70ef2040e438a3f9b589',
                        '599e76492040e438a3f9b596',
                        '599e789e2040e43f0ef9b518',
                        '59a77ebb2040e46be74fd1ea',
                        '59a780c42040e46be84fd207',
                        '59a78c3f2040e46be74fd1fa',
                        '59a7a4972040e46be74fd201',
                        '59a7ab702040e46be74fd20e',
                        '59a7b2f42040e46be84fd23f',
                        '59a7be902040e423224fd231',
                        '59a7bff02040e46be74fd230',
                        '59a7a9822040e423224fd1fd',
                        '59a7b0f72040e46be84fd233',
                        '59a7b3e92040e46be84fd245',
                        '59a7baa12040e423224fd222',
                        '59a7bdce2040e46be74fd223',
                        '59a7d7202040e46be84fd26a']
        # moments = UserMoment.objects.filter(show_status__in=[1, 3, 4], delete_status=1, is_public=1).order_by("-create_time")[(page - 1) * page_count:page * page_count]
        moments = UserMoment.objects.filter(id__in=momentsid).order_by("-create_time")[(page - 1) * page_count:page * page_count]
        print "=========",moments.count()
        if moments:
            for moment in moments:
                if moment:
                    dic = convert_user_moment(moment)
                    if user_id:
                        like_user_list = moment.like_user_list
                        if int(user_id) in like_user_list:
                            is_liked = 1
                        else:
                            is_liked = 0
                        dic["is_liked"] = is_liked

                        if moment.type == 3:
                            buy_video_status = VideoPurchaseRecord.get_buy_status(user_id, moment.video_id)
                            dic["buy_video_status"] = buy_video_status

                        dic["check_real_video"] = RealVideoVerify.get_status(moment.user_id)

                        data.append(dic)
                    else:
                        dic["is_liked"] = 0
                        data.append(dic)

        self.write({"status": "success", "data": data})


@handler_define
class GetMoment(BaseHandler):
    @api_define("get  community moment", r'/community/get_community', [
        Param('moment_id', True, str, "", "", u'社区动态id')
    ], description=u'社区动态详情')
    @login_required
    def get(self):
        data = []
        user_id = self.current_user_id
        moment_id = self.arg('moment_id', "")
        moment = UserMoment.objects.filter(show_status__ne=2, id=moment_id).first()
        if moment:
            UserMomentLook.inc_look(user_id, str(moment.id))
            like_user_list = moment.like_user_list
            dic = convert_user_moment(moment)
            if int(user_id) in like_user_list:
                is_liked = 1
            else:
                is_liked = 0
            dic["is_liked"] = is_liked

            if moment.type == 3:
                buy_video_status = VideoPurchaseRecord.get_buy_status(user_id, moment.video_id)
                dic["buy_video_status"] = buy_video_status
                user_vip = UserVip.objects.filter(user_id=user_id).first()
                if user_vip:
                    now = datetime.datetime.now()
                    create_time = now.strftime("%Y-%m-%d")
                    vip_watch_record = VipWatchVideoRecord.objects.filter(user_id=user_id, create_time=create_time, video_id=moment.video_id).first()
                    vip_comment_status = 2
                    if vip_watch_record:
                        vip_comment_status = 1
                    dic["vip_comment_status"] = vip_comment_status

            dic["check_real_video"] = RealVideoVerify.get_status(moment.user_id)

            data.append(dic)
        else:
            return self.write({'status': "fail",
                               'error': _(u"该动态已经被删除")})
        return self.write({"status": "success", "data": data})


@handler_define
class CommentList(BaseHandler):
    @api_define("comment list", r'/community/comment_list', [
        Param('page', True, str, "1", "1", u'page'),
        Param('page_count', True, str, "10", "10", u'page_count'),
        Param('moment_id', True, str, "", "", u'社区动态id')
    ], description=u'动态详情评论列表')
    @login_required
    def get(self):
        data = []
        page = self.arg_int('page')
        page_count = self.arg_int('page_count')
        moment_id = self.arg('moment_id', "")
        comments = UserComment.objects.filter(user_moment_id=moment_id, delete_status=1).order_by("-create_time")[(page - 1) * page_count:page * page_count]

        if comments:
            for comment in comments:
                data.append(convert_comment(comment))

        self.write({"status": "success", "data": data})


@handler_define
class CreateComment(BaseHandler):
    @api_define("update_comment", r'/community/update_comment', [
        Param('moment_id', True, str, "", "", u'社区动态id'),
        Param('status', True, str, "", "", u'1: 新增  2:删除'),
        Param('comment_id', False, str, "", "", u'评论id  (删除时使用)'),
        Param('content', False, str, "", "", u'评论文字内容'),
        Param('comment_type', False, str, "", "", u'评论类型  1:评论动态  2:回复评论'),
        Param('reply_user_id', False, str, "", "", u'回复用户id'),
    ], description=u'(创建/删除) 评论')
    @login_required
    def get(self):
        moment_id = self.arg('moment_id', "")
        comment_id = self.arg('comment_id', "")
        content = self.arg('content', "")
        comment_type = self.arg_int('comment_type', 1)
        reply_user_id = self.arg_int('reply_user_id', 0)
        status = self.arg_int('status')
        user = self.current_user

        if status == 1:
            if comment_type == 1:
                code, message = UserComment.check_comment_count(user)
                if code == 2:
                    return self.write({'status': "fail", "error": message})
            user_moment = UserMoment.objects.filter(id=str(moment_id)).first()
            if int(user_moment.user_id) == int(user.id) and comment_type == 1:
                return self.write({'status': "fail", 'error': _(u"不可评论自己的动态")})
            user_vip = UserVip.objects.filter(user_id=user.id).first()

            # 购买的人可以评论私房视频
            if user_moment.type == 3:
                if comment_type ==2 and user.id != user_moment.user_id:
                    video = PrivateVideo.objects.filter(id=user_moment.video_id).first()
                    if int(video.price) != 0:
                        purchase_record = VideoPurchaseRecord.objects.filter(user_id=user.id, video_id=user_moment.video_id).first()
                        if not purchase_record:
                            return self.write({'status': "fail", 'error': _(u"只有购买视频才可评论")})

            black_type = BlackUser.is_black(user.id, user_moment.user_id)
            if black_type == 1 or black_type == 0:
                return self.write({'status': "fail", 'error': _(u"您已把对方拉黑")})
            elif black_type == 2:
                return self.write({'status': "fail", 'error': _(u"对方已把您拉黑")})

            if content:
                # 文本内容鉴黄
                ret, duration = shumei_text_spam(text=content, timeout=1, user_id=user.id, channel="COMMENT", nickname=user.nickname,
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
                    return self.write({'status': "fail",
                                       'error': _(u"经系统检测,您的内容涉及违规因素,请重新编辑")})
            comment = UserComment.create_comment(moment_id, user.id, content, comment_type, reply_user_id)

            vip_icon = ""
            if user_vip:
                vip = Vip.objects.filter(id=user_vip.vip_id).first()
                vip_icon = vip.icon_url

            return self.write({"status": "success", "comment_id": str(comment.id), "vip_icon": vip_icon})

        else:
            status = UserComment.delete_comment(comment_id, user.id)
            if status:
                return self.write({"status": "success"})
            else:
                return self.write({"status": "failed"})


@handler_define
class CreateLike(BaseHandler):
    @api_define("update_like", r'/community/update_like', [
        Param('moment_id', True, str, "", "", u'社区动态id'),
        Param('status', True, str, "", "", u'1:点赞  2:取消点赞'),
    ], description=u'点赞/取消点赞')
    @login_required
    def get(self):
        moment_id = self.arg('moment_id', "")
        status = self.arg_int('status')
        user_id = self.current_user_id
        UserMoment.update_like(status, user_id, moment_id)
        self.write({"status": "success"})


@handler_define
class UserHomeMoments(BaseHandler):
    @api_define("user home moments", r'/community/user_home_moments', [], description=u'个人主页社区动态列表')
    @login_required
    def get(self):
        user_id = self.current_user_id
        temp_moments = UserMoment.objects.filter(user_id=user_id, show_status__ne=2, delete_status=1, is_public=1).order_by("-create_time")
        count = 0
        moments = []
        data = []
        for moment in temp_moments:
            if count > 10:
                break

            imgs = moment.img_list
            if not imgs:
                continue

            for img in imgs:
                if img["status"] == 1:
                    moment.img_list = []
                    moment.img_list.append(img)
                    moments.append(moment)
                    count += 1
                    break
        if moments:
            for moment in moments:
                data.append(convert_user_moment(moment))
        self.write({"status": "success", "data": data})


@handler_define
class MomentList_V2(BaseHandler):
    @api_define("index community list V2", r'/community/index_list_v2', [
        Param('page', True, str, "1", "1", u'page'),
        Param('page_count', True, str, "10", "10", u'page_count'),
    ], description=u'首页社区动态列表_带两条评论')
    def get(self):
        data = []
        page = self.arg_int('page')
        user_id = self.current_user_id

        page_count = self.arg_int('page_count')
        moments = UserMoment.objects.filter(show_status__in=[1, 3, 4], delete_status=1, is_public=1, type=1).order_by("-create_time")[(page - 1) * page_count:page * page_count]
        if moments:
            for moment in moments:
                if moment:
                    dic = convert_user_moment(moment)

                    # 添加评论
                    comments = UserComment.objects.filter(user_moment_id=str(moment.id), delete_status=1).order_by("-create_time")[0:2]
                    comment_list = []
                    if comments:
                        for comment in comments:
                            comment_list.append(convert_comment(comment))
                    dic["comment_list"] = comment_list

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
        self.write({"status": "success", "data": data})


@handler_define
class MomentList_V2(BaseHandler):
    @api_define("community list_v2", r'/community/list_v2', [
        Param('list_type', True, str, "", "", u'1: 我的动态   2:我的关注动态   3:其他用户动态'),
        Param('show_user_id', False, str, "", "", u'展示的用户id (list_type = 3 时需要传入)'),
        Param('page', True, str, "1", "1", u'page'),
        Param('page_count', True, str, "10", "10", u'page_count'),
    ], description=u'(我的/关注/其他用户)社区动态列表_带两条评论')
    @login_required
    def get(self):
        user = self.current_user
        user_id = self.current_user_id
        list_type = self.arg_int("list_type")
        show_user_id = self.arg_int("show_user_id", 0)
        page = self.arg_int('page')
        page_count = self.arg_int('page_count')
        data = []

        if list_type == 1:
            # 我的动态
            moments = UserMoment.objects.filter(user_id=user.id, show_status__ne=2, delete_status=1, is_public=1, type=1).order_by("-create_time")[(page - 1) * page_count:page * page_count]
        elif list_type == 2:
            # 我的关注动态
            follow_users = FollowUser.objects.filter(from_id=user.id)
            friend_users = FriendUser.objects.filter(from_id=user.id)
            user_ids = []
            if follow_users:
                for follow_user in follow_users:
                    fo_uid = follow_user.to_id
                    if fo_uid not in user_ids:
                        user_ids.append(fo_uid)
            if friend_users:
                for friend_user in friend_users:
                    fr_uid = friend_user.to_id
                    if fr_uid not in user_ids:
                        user_ids.append(fr_uid)

            moments = UserMoment.objects.filter(user_id__in=user_ids, show_status__in=[1, 3, 4], delete_status=1, type=1).order_by("-create_time")[(page - 1) * page_count:page * page_count]
        elif list_type == 3:
            # 其他用户动态
            moments = UserMoment.objects.filter(user_id=show_user_id, show_status__in=[1, 3, 4], delete_status=1, type=1).order_by("-create_time")[(page - 1) * page_count:page * page_count]
        else:
            moments = None

        if moments:
            for moment in moments:
                like_user_list = moment.like_user_list
                dic = convert_user_moment(moment)

                # 添加评论
                comments = UserComment.objects.filter(user_moment_id=str(moment.id), delete_status=1).order_by("-create_time")[0:2]
                comment_list = []
                if comments:
                    for comment in comments:
                        comment_list.append(convert_comment(comment))
                dic["comment_list"] = comment_list

                if int(user_id) in like_user_list:
                    is_liked = 1
                else:
                    is_liked = 0
                dic["is_liked"] = is_liked
                data.append(dic)

        self.write({"status": "success", "data": data})


@handler_define
class MomentCheck(BaseHandler):
    @api_define("community check", r'/community/moment_check', [], description=u'动态发布检查')
    @login_required
    def get(self):
        user = self.current_user

        vip_count = 5
        anchor_vip_count = 15
        anchor_count = 10
        user_count = 2
        is_video = user.is_video_auth
        user_vip = UserVip.objects.filter(user_id=user.id).first()

        now = datetime.datetime.now()
        starttime = now.strftime("%Y-%m-%d 00:00:00")
        endtime = now.strftime('%Y-%m-%d 23:59:59')
        today_moment_count = UserMoment.objects.filter(user_id=user.id, show_status__ne=2, delete_status=1,
                                                       create_time__gte=starttime, create_time__lte=endtime).count()

        dic = {
            "code": 1,
            "msg": "可以发布"
        }

        if user_vip:
            if is_video == 1:
                if today_moment_count >= anchor_vip_count:
                    dic = {
                        "code": 3,
                        "msg": "今日动态已到达上限"
                    }
            else:
                if today_moment_count >= vip_count:
                    if int(user.gender) == 2:
                        dic = {
                            "code": 4,
                            "msg": "成为播主可继续发布动态"
                        }
                    else:
                        dic = {
                            "code": 3,
                            "msg": "今日动态已到达上限"
                        }

        else:
            if is_video == 1:
                if today_moment_count >= anchor_count:
                    dic = {
                        "code": 2,
                        "msg": "升级VIP,可以继续发布动态"
                    }
            else:
                if today_moment_count >= user_count:
                    dic = {
                        "code": 2,
                        "msg": "升级VIP,可以继续发布动态"
                    }

        return self.write({"status": "success", "data": dic})


@handler_define
class AboutMeMessageList(BaseHandler):
    @api_define("about_me list", r'/community/about_me_list', [
        Param('page', True, str, "1", "1", u'page'),
        Param('page_count', True, str, "10", "10", u'page_count'),
    ], description=u'与我相关 消息列表')
    @login_required
    def get(self):
        user_id = self.current_user_id
        page = self.arg_int('page')
        page_count = self.arg_int('page_count')
        messages = AboutMeMessage.objects.filter(user_id=user_id).order_by("-create_time")[(page - 1) * page_count:page * page_count]
        data = []
        if messages:
            for message in messages:
                dict = convert_about_me_message(message)
                moment = UserMoment.objects.filter(id=message.moment_id).first()
                buy_video_status = VideoPurchaseRecord.get_buy_status(user_id, moment.video_id)
                dict["moment"]["buy_video_status"] = buy_video_status
                like_user_list = moment.like_user_list
                if int(user_id) in like_user_list:
                    is_liked = 1
                else:
                    is_liked = 0
                dict["moment"]["is_liked"] = is_liked
                data.append(dict)

        return self.write({"status": "success", "data": data})








