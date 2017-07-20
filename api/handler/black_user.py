#coding=utf-8
from api.document.doc_tools import *
from api.view.base import BaseHandler
import time
from api.view.base import *
from api.convert.convert_user import *
from api.handler.thridpard.qcloud.im import *
from app.customer.models.black_user import *
from app.customer.models.vip import *


@handler_define
class Black_User(BaseHandler):
    @api_define("black user", r'/black/black_user', [
        Param("black_user_id", True, str, "", "", u"black_user_id"),
        Param("black_type", True, str, "", "", u"black_type:  1: 拉黑   2: 取消拉黑"),
    ], description=u"拉黑(取消)用户<br>"
                   u"black_type    0:互相拉黑   1:已把对方拉黑  2:对方把您拉黑  3:均未拉黑")
    @login_required
    def get(self):
        user_id = int(self.current_user_id)
        user = self.current_user
        black_user_id = self.arg_int("black_user_id")
        black_type = self.arg_int("black_type")
        black_user = User.objects.filter(id=black_user_id).first()

        if black_type == 1:
            # 拉黑
            db_black_user = BlackUser.objects.filter(from_id=user_id, to_id=black_user_id).first()
            if db_black_user:
                return self.write({"status": "failed", "error": "You have already blacked this user"})
            BlackUser.black_add(user, black_user)
        elif black_type == 2:
            # 取消拉黑
            BlackUser.black_delete(user, black_user)

        black_type = BlackUser.is_black(user.id, black_user_id)

        return self.write({"status": "success", "black_type": black_type})

@handler_define
class Black_User_List(BaseHandler):
    @api_define("black user list", r'/black/black_user_list', [
        Param('page', True, str, "1", "1", u'page'),
        Param('page_count', True, str, "10", "10", u'page_count'),
    ], description="黑名单列表")
    @login_required
    def get(self):
        user = self.current_user
        page = self.arg_int('page')
        page_count = self.arg_int('page_count')

        black_users = BlackUser.black_user_list(user)[(page - 1) * page_count:page * page_count]
        data = []
        for black_user in black_users:
            u = User.objects.filter(id=black_user.to_id).first()
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
class IS_Black_User(BaseHandler):
    @api_define("is black user", r'/black/is_black_user', [
        Param("black_user_id", True, str, "", "", u"black_user_id"),
    ], description="判断某用户是否被拉黑 (0: 互相拉黑  1:把对方拉黑  2:对方把您拉黑   3:均未拉黑)")
    @login_required
    def get(self):
        user = self.current_user
        black_user_id = self.arg_int("black_user_id")
        black_type = BlackUser.is_black(user.id, black_user_id)

        return self.write({"status": "success", "black_type": black_type})

