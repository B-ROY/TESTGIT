# coding=utf-8

from api.convert.convert_user import *
from api.document.doc_tools import *
from api.view.base import *
from app.customer.models.user import User
from api.handler.thridpard.sms_code.sms import SMS
from app_redis.activity.integral import Integral


@handler_define
class IntegralActivityLogin(BaseHandler):
    @api_define("Login", r'/temp/integral/login', [
        Param('user_key', True, str, "", "123456790", u'code,access_token'),
        Param('openid', True, str, "", "123456790", u'用户唯一标识,[支付宝用户id，微信用户id，微博用户id]'),
        Param("phone", True, str, "", "", u"手机号"),
        Param('sms_code', True, str, "", "", u'短信验证码'),
    ], description=u"H5提现登录接口", protocal="https")
    def get(self):
        access_token = self.arg("user_key")
        openid = self.arg("openid")
        phone = self.arg("phone")
        sms_code = self.arg("sms_code")

        if access_token == "" or openid == "":
            return self.write({"status": "fail", "error": "access_token or openid null!", "message_code": 3, })

        ucpass = SMS()
        result = ucpass.getCacheData(phone)
        ucpass.delSmsCodeCache(phone)

        if result != None:
            createDate = result['createDate']
            user_key = ucpass.get_access_token(phone, openid, createDate)
            if user_key != access_token:
                return self.write({"status": "fail", "error": _(u"非法用户"), "message_code": 3, })
            if sms_code != result['smsCode']:
                return self.write({"status": "fail", "error": _(u"验证码错误，请输入正确的验证码"), "message_code": 2, })
        else:
            return self.write({"status": "fail", "error": _(u"验证码失效"), "message_code": 2, })

        user = User.objects.filter(phone=phone).order_by("created_at").first()

        if not user:
            return self.write({"status": "fail", "error": _(u"未绑定手机号"), "message_code": 4})

        integral = Integral.select_integral(user.id)
        user_data = {
            "_uid": user.id,
            "nickname": user.nickname,
            "integral": integral,
            "uid": user.identity,
        }
        data = {
            "user": user_data,

        }
        self.auth_login(user.id)
        return self.write({"status": "success", "data": data })


@handler_define
class IntegralSignHandler(BaseHandler):
    @api_define("InteGration", r'/temp/integral', []
                , description=u"查看积分")
    def get(self):
        user_id = self.current_user_id
        if user_id:  # 已登录
            # todo 跳转积分页面
            integral = Integral.select_integral(self.current_user.id)
            nickname = self.current_user.nickname
            self.redirect('http://www.iwala.cn/integral/query_integral.html?' + "integral=" + str(integral) + "&nickname=" + str(nickname))
            pass
        else:  # 未登录
            # todo 跳转登录页面
            self.redirect('http://www.iwala.cn/integral/wx_login.html')
            pass














