#coding=utf-8
from api.document.doc_tools import *
from api.view.base import *
from app.live.models import *
from django.conf import settings
from api.convert.convert_user import *
from app.customer.models.user import *
# from PIL import Image
import urlparse
import hashlib
import base64
import time
import json
import hmac

secret = "c7c8bea31297601bb7b901d9e3e61121"
@handler_define
class CheckAdmin(BaseHandler):
    @api_define("check admin", r'/live/admin/verify', [
        Param('user_id', True, str, "", "", u'user_id,当前的用ID'),
        Param('time', True, str, "", "", u'time'),
    ], description=u"检查是否为管理员接口",)
    @login_required
    def get(self):
        t = self.arg("time")
        user_id = self.arg("user_id",self.current_user_id)
        msg = 'user_id=' + user_id + '&time=' + t
        sign_su = msg + "ss" + secret
        sign_fa = msg + "fl" + secret
        m1 = hashlib.md5()
        m2 = hashlib.md5()
        m1.update(sign_su)
        m2.update(sign_fa)
        sign_su = m1.hexdigest()
        sign_fa = m2.hexdigest()

        if user_id != self.current_user_id:
            return self.write({'status': sign_fa})

        if not User.check_is_super_admin(user_id):
            return self.write({'status': sign_fa})

        extime = int(time.time()) - int(t)
        if extime > 5 or extime < -5:
            return self.write({'status': sign_fa})

        self.write({'status': sign_su})
