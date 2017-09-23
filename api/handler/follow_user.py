#coding=utf-8
from api.document.doc_tools import *
from api.view.base import BaseHandler
import time
from api.view.base import *
from api.convert.convert_user import *
from api.handler.thridpard.qcloud.im import *
from app.customer.models.black_user import *
from app.customer.models.vip import *
from app.customer.models.follow_user import *
import international


@handler_define
class Follow_User(BaseHandler):
    @api_define("follow user", r'/follow/follow_user', [
        Param("follow_user_id", True, str, "", "", u"follow_user_id"),
        Param("follow_type", True, str, "", "", u"follow_type:  1:关注  2: 取消关注"),
    ], description="关注(取消)用户")
    @login_required
    def get(self):
        user = self.current_user
        follow_user_id = self.arg_int("follow_user_id")
        follow_type = self.arg_int("follow_type")
        follow_user = User.objects.filter(id=follow_user_id).first()

        black_type = BlackUser.is_black(user.id, follow_user_id)
        if black_type == 1 or black_type == 0:
            return self.write({'status': "fail",'error': _(u"您已把对方拉黑")})
        elif black_type == 2:
            return self.write({'status': "fail",'error': _(u"对方已把您拉黑")})

        if follow_type == 1:
            # 关注
            FollowUser.follow_user_add(user, follow_user)
        elif follow_type == 2:
            # 取消关注
            FollowUser.follow_user_delete(user, follow_user)

        return self.write({"status": "success"})


@handler_define
class Follow_User_List(BaseHandler):
    @api_define("follow user list", r'/follow/follow_user_list', [
        Param('page', True, str, "1", "1", u'page'),
        Param('page_count', True, str, "10", "10", u'page_count'),
    ], description="关注用户列表")
    @login_required
    def get(self):
        user = self.current_user
        page = self.arg_int('page')
        page_count = self.arg_int('page_count')
        follow_users = FollowUser.objects.filter(from_id=user.id).order_by("-create_time")[(page - 1) * page_count:page * page_count]
        data = []
        for follow_user in follow_users:
            u = User.objects.filter(id=follow_user.to_id).first()
            user_vip = UserVip.objects.filter(user_id=u.id).first()
            if not user_vip:
                dic = {
                    "user": convert_user(u)
                }
            else:
                vip = Vip.objects.filter(id=user_vip.vip_id).first()
                dic = {
                    "user": convert_user(u),
                    "vip": convert_vip(vip)
                }
            data.append(dic)
        return self.write({"status": "success", "data": data})

@handler_define
class Fans_User_List(BaseHandler):
    @api_define("fans user list", r'/follow/fans_user_list', [
        Param('page', True, str, "1", "1", u'page'),
        Param('page_count', True, str, "10", "10", u'page_count'),
    ], description="粉丝用户列表")
    @login_required
    def get(self):
        user = self.current_user
        page = self.arg_int('page')
        page_count = self.arg_int('page_count')

        fans_users = FollowUser.objects.filter(to_id=user.id).order_by("-create_time")[(page - 1) * page_count:page * page_count]
        data = []
        for fans_user in fans_users:
            u = User.objects.filter(id=fans_user.from_id).first()
            user_vip = UserVip.objects.filter(user_id=u.id).first()
            if not user_vip:
                dic = {
                    "user": convert_user(u)
                }
            else:
                vip = Vip.objects.filter(id=user_vip.vip_id).first()
                dic = {
                    "user": convert_user(u),
                    "vip": convert_vip(vip)
                }
            data.append(dic)
        return self.write({"status": "success", "data": data})


@handler_define
class Friend_User_List(BaseHandler):
    @api_define("friend user list", r'/follow/friend_user_list', [
        Param('page', True, str, "1", "1", u'page'),
        Param('page_count', True, str, "10", "10", u'page_count'),
    ], description="好友列表")
    @login_required
    def get(self):
        user = self.current_user
        page = self.arg_int('page')
        page_count = self.arg_int('page_count')

        friend_users = FriendUser.objects.filter(to_id=user.id)[(page - 1) * page_count:page * page_count]
        data = []
        for friend_user in friend_users:
            u = User.objects.filter(id=friend_user.from_id).first()
            user_vip = UserVip.objects.filter(user_id=u.id).first()
            if not user_vip:
                dic = {
                    "user": convert_user(u)
                }
            else:
                vip = Vip.objects.filter(id=user_vip.vip_id).first()
                dic = {
                    "user": convert_user(u),
                    "vip": convert_vip(vip)
                }
            data.append(dic)
        return self.write({"status": "success", "data": data})


@handler_define
class IS_Follow_User(BaseHandler):
    @api_define("is follow user", r'/follow/is_follow_user', [
        Param("follow_user_id", True, str, "", "", u"follow_user_id"),
    ], description="是否关注此用户 (0: 未关注  1: 关注)")
    @login_required
    def get(self):
        user = self.current_user
        follow_user_id = self.arg_int("follow_user_id")

        follow_user = FollowUser.objects.filter(from_id=user.id, to_id=follow_user_id).first()
        if not follow_user:
            return self.write({"status": "success", "is_follow": 0})
        return self.write({"status": "success", "is_follow": 1})
