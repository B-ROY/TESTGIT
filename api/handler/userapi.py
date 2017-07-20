# coding=utf-8
import base64
import json

from api.convert.convert_user import *
from api.document.doc_tools import *
from api.handler.thridpard.qq import QQAPI
from api.handler.thridpard.sms_code.sms import SMS
from api.handler.thridpard.weibo import WeiBoAPI
from api.handler.thridpard.weixin import WexinAPI
from api.util.tencenttools.signature import gen_signature
from api.view.base import *
# from PIL import Image
# from app.customer.models.rank import *
# from app.customer.models.account import *
from app.customer.models.adv import Adv
from app.customer.models.block_user_device import *
from app.customer.models.feedback import *
from app.customer.models.message import *
from app.customer.models.online_user import *
from app.customer.models.personal_tags import *
from app.customer.models.rank import *
from app.customer.models.share import *
from app.customer.models.user import UserAppealRecord
from app.customer.models.vip import *
from app.picture.models.picture import *
from app.redismodel.onlinecount import OnlineCount
import international
# from background.audit_handler.audit_handler import *
from app.util.shumeitools.shumeitools import *
from app.customer.models.shumeidetect import *
from app.customer.models.follow_user import *
from app.customer.models.black_user import *
from app.customer.models.community import *

class ThridPardLogin(BaseHandler):
    def create_user(self, openid, access_token, phone, userinfo, source, channel, site_openid=''):
        #获取改用户的guid
        guid = self.arg("guid")
        if source == User.SOURCE_PHONE or source==User.SOURCE_FACEBOOK or User.SOURCE_TWITTER:
            userinfo={}
            userinfo["nickname"] = RegisterInfo.make_nickname()
            gender = userinfo.get("sex", 1)
            if gender == 1:
                img_url = "https://hdlive-10048692.image.myqcloud.com/head_1497413045"
            else:
                img_url = "https://hdlive-10048692.image.myqcloud.com/head_1497413074"
            is_new,user= User.create_user(
                openid=openid,
                source=source,
                nickname=userinfo.get("nickname")[0:18],
                gender=gender,
                phone=phone,
                ip=self.user_ip,
                image=userinfo.get("headimgurl",
                                   img_url),
                channel=channel,
                guid=guid
            )
        else:
            #创建新用户
            # openid, source, nickname, platform=0, image="", channel=""
            is_new, user = User.create_user(
                openid=openid,
                source=source,
                nickname=userinfo.get("nickname")[0:18],
                gender=userinfo.get("gender", 1),
                phone=phone,
                ip=self.user_ip,
                image=userinfo.get("headimgurl", "https://hdlive-10048692.image.myqcloud.com/5c8ff8bdc5a3645edcd8d4f9313f29e7"),
                channel=channel,
                guid = guid
            )

            if source != User.SOURCE_PHONE:
                third_part = ThridPard.get_by_user(user_id=user.id)
                third_part.update_weixin_info(site_openid, access_token)

        return is_new, user

    def create_user2(self, openid, access_token, phone, userinfo, source, channel, site_openid=''):
        #获取改用户的guid
        guid = self.arg("guid")
        gender = userinfo.get("sex", 1)
        if gender == 1:
            img_url = "https://hdlive-10048692.image.myqcloud.com/head_1497413045"
        else:
            img_url = "https://hdlive-10048692.image.myqcloud.com/head_1497413074"
        #创建新用户
        # openid, source, nickname, platform=0, image="", channel=""
        is_new, user = User.create_user2(
            openid=openid,
            source=source,
            nickname=userinfo.get("nickname")[0:18],
            gender=gender,
            phone=phone,
            ip=self.user_ip,
            image=userinfo.get("headimgurl", img_url),
            channel=channel,
            guid = guid
        )

        return is_new, user


    def weixin_login(self):
        code = self.arg("user_key")
        ua = self.request.headers.get('User-Agent')
        uas = ua.split(";")
        if uas[2] == "iPhone" or uas[2] == "iPad":
            channel = "AppStore"
        else:
            channel = uas[5]

        #1. code 2 access token
        data = WexinAPI.get_access_token(code)
        #print data
        access_token = data.get("access_token", "")
        openid = data.get("openid", "")
        unionid = data.get("unionid", "")
        scope = data.get("scope", "")
        expires_in = data.get("expires_in", 7200)
        efresh_token = data.get("efresh_token", "")

        if access_token == "" or openid == "":
            raise Exception("access_token or openid null!")

        userinfo = WexinAPI.get_user_info(access_token, openid)
        site_openid = openid
        openid = userinfo.get("unionid")
        if not userinfo.get("nickname"):
            raise Exception("nickname null!")

        return self.create_user(openid, access_token, None,userinfo, User.SOURCE_WEIXIN, channel, site_openid)

    def weixin_youmeng_login(self):
        access_token = self.arg("user_key", "")
        openid = self.arg("openid", "")
        ua = self.request.headers.get('User-Agent')
        uas = ua.split(";")
        if uas[2] == "iPhone" or uas[2] == "iPad":
            channel = "AppStore"
        else:
            channel = uas[5]

        if access_token == "" or openid == "":
            raise Exception("access_token or openid null!")

        if self.arg("platform") == "h5":
            userinfo = WexinAPI.get_h5_user_info(access_token, openid)
        else:
            userinfo = WexinAPI.get_user_info(access_token, openid)

        if not userinfo.get("nickname"):
            raise Exception("nickname null!")

        #app 统一
        site_openid = openid
        openid = userinfo.get("unionid")
        print openid,site_openid

        #创建新用户
        return self.create_user(openid, access_token, None, userinfo, User.SOURCE_WEIXIN , channel, site_openid)


    def weibo_login(self):
        access_token = self.arg("user_key", "")
        uid = self.arg("openid","")
        ua = self.request.headers.get('User-Agent')
        uas = ua.split(";")
        if uas[2] == "iPhone" or uas[2] == "iPad":
            channel = "AppStore"
        else:
            channel = uas[5]

        if access_token == "" :
            raise Exception("access_token or openid null!")

        token_info = WeiBoAPI.get_token_info(access_token,uid)

        if uid != str(token_info.get("id")):
            raise Exception("user not Auth")
        userinfo = {"nickname":str(token_info.get("name")),"sex":2,"province":"","city":"","country":"","headimgurl":str(token_info.get("avatar_large"))}

        #print userinfo

        openid = base64.b64encode(uid)

        #创建新用户
        return self.create_user(openid, access_token, None, userinfo, User.SOURCE_WEIBO, channel,openid)


    def qq_login(self):

        access_token = self.arg("user_key", "")
        openid = self.arg("openid", "")
        ua = self.request.headers.get('User-Agent')
        uas = ua.split(";")
        if uas[2] == "iPhone" or uas[2] == "iPad":
            channel = "AppStore"
        else:
            channel = uas[5]
        #print access_token,openid

        if access_token == "" or openid == "":
            raise Exception("access_token or openid null!")

        userinfo = QQAPI.get_user_info(access_token, openid, self.arg("platform","ios"))
        #print userinfo

        if not userinfo.get("nickname"):
            raise Exception("nickname null!")

        #创建新用户
        return self.create_user(openid, access_token, None, userinfo, User.SOURCE_QQ, channel, openid)

    def phone_login(self):
        access_token = self.arg("user_key")
        openid = self.arg("openid")
        phone = self.arg("phone")
        sms_code = self.arg("sms_code")
        ua = self.request.headers.get('User-Agent')
        uas = ua.split(";")
        if uas[2] == "iPhone" or uas[2] == "iPad":
            channel = "AppStore"
        else:
            channel = uas[5]

        ucpass = SMS()

        result = ucpass.getCacheData(phone)

        if result != None:
            createDate = result['createDate']
            user_key = ucpass.get_access_token(phone, openid, createDate)
            if user_key != access_token:
                raise Exception(u"非法用户")
            if sms_code != result['smsCode']:
                raise Exception(u"验证码输入错误")
        else:
            raise Exception(u"验证码失效")

        user = User.objects.filter(phone=phone).first()
        if user:
            return False, user
        else:
            return self.create_user(openid=openid, access_token=access_token,phone=phone,userinfo=None,
                                source=User.SOURCE_PHONE, channel=channel, site_openid=openid)

    def facebook_login(self):
        access_token = self.arg("user_key", "")
        openid = self.arg("openid", "")
        ua = self.request.headers.get('User-Agent')
        uas = ua.split(";")
        app_name = uas[0]
        if app_name == "liaoai_teyue" or app_name == "liaoai_lizhen":
            channel = "AppStore"
        else:
            channel = uas[5]
        # print access_token,openid

        if access_token == "" or openid == "":
            raise Exception("access_token or openid null!")

        return self.create_user(openid=openid, access_token=access_token, phone="", userinfo=None,
                         source=User.SOURCE_FACEBOOK, channel=channel, site_openid=openid)

    def twitter_login(self):
        access_token = self.arg("user_key", "")
        openid = self.arg("openid", "")
        ua = self.request.headers.get('User-Agent')
        uas = ua.split(";")
        app_name = uas[0]
        if app_name == "liaoai_teyue" or app_name == "liaoai_lizhen":
            channel = "AppStore"
        else:
            channel = uas[5]
        # print access_token,openid
        print access_token
        print openid
        if access_token == "" or openid == "":
            raise Exception("access_token or openid null!")

        return self.create_user(openid=openid, access_token=access_token, phone="", userinfo=None,
                         source=User.SOURCE_TWITTER, channel=channel, site_openid=openid)

    def test_login(self,username,source="100"):
        #创建新用户
        is_new, user = User.create_user(
            openid="1234567890",
            source=source,
            nickname=username,
            gender=1,
            ip=self.request.remote_ip,
            image="",
            channel="test",
            guid="test"
        )

        return is_new, user

    def heydo_login(self, password, source=0):
        #创建新用户
        is_new, user = User.create_user(
            openid=password,
            source=source,
            nickname='',
            gender=1,
            ip=self.request.remote_ip,
            image="",
            channel="heydo",
        )
        if is_new:
            user.nickname = '%s%s' % (u'黑洞用户', user.identity)
            user.save()
        return is_new, user

@handler_define
class Login(ThridPardLogin):
    @api_define("Login", r'/live/login', [
        Param('user_key', True, str, "", "123456790", u'code,access_token'),
        Param('openid', True, str, "", "123456790", u'用户唯一标识,[支付宝用户id，微信用户id，微博用户id]'),
        Param('source', True, str, "", "100", u'用户来源[微信:1,微博:2,QQ:3，手机:4,友盟微信:5，facebook:6, twitter:7, 测试:100]'),
        Param('nickname', False, str, "", "testuser3", u'用户名'),
        Param('sms_code',False,str,"","",u'短信验证码'),
        Param('createdate',False,str,"","",u'申请验证码时间'),
        Param('platform', True, str, "ios", "ios", u'可选:ios,android,h5'),
        Param('phone',False, str, "", "", u'电话号码')
    ], description=u"登录接口",protocal="https")
    def get(self):
        #获取参数
        source = self.arg_int('source')
        if source == User.SOURCE_WEIXIN:
            try:
                is_new, user = self.weixin_login()
            except Exception, e:
                logging.error("weixin login error:%s" % str(e))
                return self.write({"status": "fail", "error": "%s" % (e.message)})
        elif source == User.SOURCE_QQ:
            try:
                is_new, user = self.qq_login()
            except Exception, e:
                logging.error("qq login error:%s" % str(e))
                return self.write({"status": "fail", "error": "%s" % (e.message)})
        elif source == User.SOURCE_YOUMENG_WEIXIN:
            try:
                is_new, user = self.weixin_youmeng_login()
            except Exception, e:
                logging.error("youmeng login error:%s" % str(e))
                return self.write({"status": "fail", "error": "%s" % (e.message)})
        elif source == User.SOURCE_WEIBO:
            try:
                is_new, user = self.weibo_login()
            except Exception, e:
                logging.error("weibo login error:%s" % str(e))
                return self.write({"status": "fail", "error": "%s" % (e.message)})
        elif source == User.SOURCE_PHONE:
            try:
                is_new, user = self.phone_login()
            except Exception,e:
                logging.error("phone login error:%s" % str(e))
                return self.write({"status": "fail", "error": "%s" % (e.message)})
        elif source == User.SOURCE_FACEBOOK:
            try:
                is_new, user = self.facebook_login()
            except Exception, e:
                logging.error("facebook login error:%s" % str(e))
                return self.write({"status": "fail", "error": "%s" % (e.message)})
            pass
        elif source == User.SOURCE_TWITTER:
            try:
                is_new, user = self.twitter_login()
            except Exception, e:
                logging.error("titter login error:%s" % str(e))
                return self.write({"status": "fail", "error": "%s" % (e.message)})
            pass
        elif source == 100:
            is_new, user = self.test_login("test100","100")
        elif source == 101:
            is_new, user = self.test_login("test101","101")
        else:
            return self.write({"status": "fail", "error": ":("})

        if user.is_blocked:
            logging.error("login error: blocked user")
            return self.write({"status":"fail", "error":_(u"经系统检测，您的账号存在违规行为，已经被服务器暂时封停；如您存在疑问请点击下方申诉或联系客服QQ：3270745762"),"errcode":"2001", "_uid":user.id})

        # 判断封设备
        guid = self.arg("guid")
        block_dev = BlockUserDev.objects.filter(status__ne=3, devno=guid, reason_type__ne=4).first()
        if block_dev:
            return self.write({"status": "fail", "error": _(u"经系统检测，您的账号存在违规行为，设备已经被服务器暂时封停；如您存在疑问请点击下方申诉或联系客服QQ：3270745762"),"errcode":"2002", "_uid":user.id})


        #convert user info
        data = {}
        data["user"] = convert_user(user)
        data["user"]["diamond"] = Account.objects.get(user=user).diamond
        data['is_new'] = is_new
        if is_new:
            data.update(generate_default_info())
        else:
            AudioRoomRecord.create_roomrecord(user_id=user.id, open_time=datetime.datetime.now())
            user.update(set__last_guid=self.arg("guid"))

        #set cookie
        self.auth_login(user.id)
        app_id = settings.QCLOUD_LIVE_SDK_APP_ID

        data['sig'] = gen_signature(app_id, user.sid)
        data["status"] = "success"

        #清除验证码的缓存
        if source == User.SOURCE_PHONE:
            ucpass = SMS()
            ucpass.delSmsCodeCache(self.arg_int('phone'))

        #audio_status = AudioRoomRecord.get_room_status(user_id=user.id)
        #if audio_status == 4:
        #    AudioRoomRecord.set_room_status(user_id=user.id, status=1)

        self.write(data)


@handler_define
class CompletePersonalInfo(BaseHandler):
    @api_define("complete personal info", r"/live/complete/personal_info", [
        Param('img', False, str, "", "", u"用户头像"),
        Param('gender', True, str, "", "", u"性别(1男,2女)"),
        Param('birth_date', False, str, "", "", u"出生日期(回传字符串类型如'2016-01-01')"),
        Param('nickname', False, str, "", "", u"昵称"),
        Param('invite_code', False, str, "", "", u"邀请码(传用户长id)"),
    ], description=u"完善个人资料", protocal="https")
    @login_required
    def get(self):
        user = self.current_user
        img = self.arg("img", "")
        nickname = self.arg("nickname","")

        # 用户昵称 鉴黄

        if self.has_arg("nickname"):
            ret, duration = shumei_text_spam(text=user.nickname, timeout=1, user_id=user.id, channel=1, nickname=nickname,
                                                                phone=user.phone, ip=self.user_ip)
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
                # user.update(set__nickname="爱聊用户" + str(user.identity))
                text_detect = TextDetect()
                text_detect.user = user
                text_detect.text_channel = 1
                text_detect.text = user.nickname
                text_detect.created_time = datetime.datetime.now()
                text_detect.save()
                return self.write({'status': "fail",
                                   "error_code": 10005,
                                   'error_message': u"经系统检测,您的昵称内容涉及违规因素,请重新编辑"})


        birth_date = self.arg("birth_date", "1995-01-01")
        gender = self.arg_int("gender", 2)
        invite_code = self.arg("invite_code", "0")
        user_guid = self.arg("guid")

        if invite_code.isdigit():
            invite_code = int(invite_code)
        else:
            invite_code = 0

        if invite_code != 0:
            invite_id, result_code = UserInviteCode.invite_code_check(user_id=user.id, invite_code=invite_code, user_guid=user_guid)
            if not result_code:
                UserInviteCode.create_invite_code(user_id=user.id, invite_id=invite_id, user_guid=user_guid)
            elif result_code == 10001:
                return self.write({"status": "failed", "error_code": 10001, "error_message": _(u"邀请码填写错误,请重新填写")})
            elif result_code == 10002:
                return self.write({"status": "failed", "error_code": 10002, "error_message": _(u"不能邀请自己")})
            elif result_code == 10003:
                return self.write({"status": "failed", "error_code": 10003, "error_message": _(u"同一个设备不能邀请自己")})
            elif result_code == 10004:
                return self.write({"status": "failed", "error_code": 10004, "error_message": _(u"同一个设备仅能邀请1次")})

        status = User.complete_personal_info(user, nickname, gender, img, birth_date)
        if status:
            AudioRoomRecord.create_roomrecord(user_id=user.id, open_time=datetime.datetime.now())
            return self.write({"status": "success"})
        else:
            return self.write({"status": "failed", "error_message": _(u"完善用户资料是失败")})


def generate_default_info():
    data = {}
    data["birth_date"] = '1995-01-01'
    data["nickname"] = RegisterInfo.make_nickname()
    pictures = UserDefaultImg.get_all_defaults_img()
    pic_list = []
    for picture in pictures:
        dic = {
            "picture_url": picture.picture_url,
            "gender": picture.gender,
        }
        pic_list.append(dic)
    data["pictures"] = pic_list
    return data

@handler_define
class PhoneRegister(BaseHandler):
    @api_define("Phone Register", "/live/phone/register", [
        Param('user_key', True, str, "", "123456790", u'code,access_token'),
        Param('openid', True, str, "", "123456790", u'用户唯一标识,[支付宝用户id，微信用户id，微博用户id]'),
        Param("phone", True, str, "", "", u"手机号"),
        Param("sms_code", True, str, "", "", u"短信验证码"),
        Param("platform", True, str, "ios", "ios", u"ios,android,h5"),
    ], description=u"手机注册接口", protocal="https")
    def get(self):
        access_token = self.arg("user_key")
        openid = self.arg("openid")
        phone = self.arg("phone")
        sms_code = self.arg("sms_code")

        if access_token == "" or openid == "":
            return self.write({"status": "fail", "error": "access_token or openid null!", "message_code": 3, })

        ucpass = SMS()
        result = ucpass.getCacheData(phone)

        if result != None:
            createDate = result['createDate']
            user_key = ucpass.get_access_token(phone, openid, createDate)
            if user_key != access_token:
                return self.write({"status": "fail", "error": _(u"非法用户"), "message_code": 3, })
            if sms_code != result['smsCode']:
                return self.write({"status": "fail", "error": _(u"验证码错误，请输入正确的验证码"), "message_code": 2, })
        else:
            return self.write({"status": "fail", "error": _(u"验证码失效"), "message_code": 2, })

        status, user_phone = PhonePassword.create_phone(phone)


        ucpass.delSmsCodeCache(phone)

        if status:
            self.set_cookie("phone", phone, max_age=600)
            self.set_cookie("openid", openid, max_age=600)
            self.set_cookie("access_token", access_token, max_age=600)

            data = {}
            data["phone"] = phone\

            data.update(generate_default_info())

            return self.write({"status": "success", "data": data, })
        else:
            if user_phone:
                return self.write({"status": "fail", "error": _(u"该手机号已注册"), "message_code": 1, })
            else:
                return self.write({"status": "fail", "error": _(u"注册失败"), "message_code": 3, })


@handler_define
class PhonePersonalInfo(ThridPardLogin):
    @api_define("Phone Personal Info", "/live/phone/personal_info", [
        Param("password", False, str, "", "", u"密码"),
        Param("img", False, str, "", "", u"头像"),
        Param("nickname", False, str, "", "", u"昵称"),
        Param("birth_date", False, str, "", "", u"出生日期(回传字符串类型如'2016-01-01')"),
        Param("gender", True, str, "", "", u"性别"),
        Param("invite_code", False, str, "", "", u"邀请码(用户长id)"),
    ], description=u"手机注册设置个人信息", protocal="https")
    def get(self):
        password = self.arg("password", "")
        img = self.arg("img", "")
        nickname = self.arg("nickname", "")
        birth_date = self.arg("birth_date", "1995-01-01")
        gender = self.arg_int("gender", 2)
        user_guid = self.arg("guid")

        invite_code = self.arg("invite_code", "0")

        phone = self.get_cookie("phone")
        access_token = self.get_cookie("access_token")
        openid = self.get_cookie("openid")
        self.clear_cookie("phone")
        ua = self.request.headers.get('User-Agent')

        if birth_date == "null":
            birth_date = "1995-01-01"
        if invite_code.isdigit():
            invite_code = int(invite_code)
        else:
            invite_code = 0
        if not password:
            password = "SDF89SI2"
        if ua.split(";")[2] == "iPhone" or ua.split(";")[2] == "iPad":
            channel = "AppStore"
        else:
            channel = ua.split(";")[5]
        if not phone:
            return self.write({"status": "fail", "error": _(u"创建个人信息超时")})

        if access_token == "" or openid == "":
            return self.write({"status": "fail", "error": "access_token or openid null!"})
        self.clear_cookie("access_token")
        self.clear_cookie("openid")

        try:
            userinfo = {"nickname": nickname, "sex": gender, "province": "", "city": "", "country": "", "headimgurl": img}
            is_new, user = self.create_user2(openid, access_token, phone, userinfo, User.SOURCE_PHONE, channel, openid)

            user.birth_date = datetime.datetime.strptime(birth_date, '%Y-%m-%d')
            user.constellation = User.zodiac(birth_date)
            user.save()

            if invite_code != 0:
                invite_id, result_code = UserInviteCode.invite_code_check(user_id=user.id, invite_code=invite_code, user_guid=user_guid)
                if not result_code:
                    UserInviteCode.create_invite_code(user_id=user.id, invite_id=invite_id, user_guid=user_guid)
                elif result_code == 10001:
                    return self.write({"status": "failed", "error_code": 10001, "error_message": _(u"邀请码填写错误,请重新填写")})
                elif result_code == 10002:
                    return self.write({"status": "failed", "error_code": 10002, "error_message": _(u"不能邀请自己")})
                elif result_code == 10003:
                    return self.write({"status": "failed", "error_code": 10003, "error_message": _(u"同一个设备不能邀请自己")})
                elif result_code == 10004:
                    return self.write({"status": "failed", "error_code": 10004, "error_message": _(u"同一个设备仅能邀请1次")})

            data = {}
            data["user"] = convert_user(user)
            data['is_new'] = is_new

            # set cookie
            self.auth_login(user.id)
            app_id = settings.QCLOUD_LIVE_SDK_APP_ID

            data['sig'] = gen_signature(app_id, user.sid)
            data["status"] = "success"

            status = PhonePassword.update_password(phone, password)
            if not status:
                return self.write({"status": "fail", "error": _(u"创建密码失败")})

            AudioRoomRecord.create_roomrecord(user_id=user.id, open_time=datetime.datetime.now())
            return self.write(data)
        except Exception,e:
            logging.error("phone personal info error:%s" % str(e))
            return self.write({"status": "fail", "error": "%s" % str(e)})


@handler_define
class PhoneLogIn(BaseHandler):
    @api_define("Phone Log In", "/live/phone/login", [
        Param("phone", True, str, "", "", u"手机号"),
        Param("password", True, str, "", "", u"密码"),
    ], description=u"手机号登录", protocal="https")
    def get(self):
        phone = self.arg("phone")
        password = self.arg("password")

        status, user_phone = PhonePassword.check_phone_password(phone, password)
        if status:
            user = User.objects.get(phone=phone)

            if user.is_blocked:
                logging.error("phone login error: blocked user")
                return self.write({"status": "fail", "error": _(u"经系统检测，您的账号存在违规行为，已经被服务器暂时封停；如您存在疑问请点击下方申诉或联系客服QQ：3270745762"), "errcode": "2001", "_uid":user.id})

            # 判断封设备
            guid = self.arg("guid")
            block_dev = BlockUserDev.objects.filter(status__ne=3, devno=guid, reason_type__ne=4).first()
            if block_dev:
                return self.write({"status": "fail", "error": _(u"经系统检测，您的账号存在违规行为，设备已经被服务器暂时封停；如您存在疑问请点击下方申诉或联系客服QQ：3270745762"),"errcode":"2002", "_uid":user.id})

            # convert user info
            data = {}
            data["user"] = convert_user(user)
            data["user"]["diamond"] = Account.objects.get(user=user).diamond
            data['is_new'] = False

            # set cookie
            self.auth_login(user.id)
            app_id = settings.QCLOUD_LIVE_SDK_APP_ID

            data['sig'] = gen_signature(app_id, user.sid)
            data["status"] = "success"

            #audio_status = AudioRoomRecord.get_room_status(user_id=user.id)
            #if audio_status == 4:
            #    AudioRoomRecord.set_room_status(user_id=user.id, status=1)
            AudioRoomRecord.create_roomrecord(user_id=user.id, open_time=datetime.datetime.now())
            user.update(set__last_guid=self.arg("guid"))
            return self.write(data)
        else:
            if user_phone:
                return self.write({"status": "fail", "error": _(u"密码有误，请重新输入!"), "message_code": 2, })
            else:
                return self.write({"status": "fail", "error": _(u"该账号不存在"), "message_code": 1, })



@handler_define
class PhoneResetCheck(BaseHandler):
    @api_define("Phone Reset Check", "/live/phone/reset/check", [
        Param('user_key', True, str, "", "123456790", u'code,access_token'),
        Param('openid', True, str, "", "123456790", u'用户唯一标识,[支付宝用户id，微信用户id，微博用户id]'),
        Param("phone", True, str, "", "", u"手机号"),
        Param("sms_code", True, str, "", "", u"短信验证码"),
    ], description=u"重置密码检查", protocal="https")
    def get(self):
        access_token = self.arg("user_key")
        openid = self.arg("openid")
        phone = self.arg("phone")
        sms_code = self.arg("sms_code")

        if access_token == "" or openid == "":
            return self.write({"status": "fail", "error": "access_token or openid null!", "message_code": 3, })

        ucpass = SMS()
        result = ucpass.getCacheData(phone)

        if result != None:
            createDate = result['createDate']
            user_key = ucpass.get_access_token(phone, openid, createDate)
            if user_key != access_token:
                return self.write({"status": "fail", "error": _(u"非法用户"), "message_code": 3, })
            if sms_code != result['smsCode']:
                return self.write({"status": "fail", "error": _(u"验证码错误，请输入正确的验证码"), "message_code": 2, })
        else:
            return self.write({"status": "fail", "error": _(u"验证码失效"), "message_code": 2, })


        ucpass.delSmsCodeCache(phone)

        status = PhonePassword.reset_password_check(phone)
        if status:
            self.set_cookie("phone", phone, max_age=600)
            return self.write({"status": "success", "phone": phone, })
        else:
            return self.write({"status": "fail", "error": _(u"该手机号未注册"), "message_code": 1, })


# 已登录的用户修改密码检查
@handler_define
class LoginUserResetCheck(BaseHandler):
    @api_define("Phone Reset Check", "/live/phone/login_user/check", [
        Param('user_key', True, str, "", "123456790", u'code,access_token'),
        Param('openid', True, str, "", "123456790", u'用户唯一标识,[支付宝用户id，微信用户id，微博用户id]'),
        Param("sms_code", True, str, "", "", u"短信验证码"),
    ], description=u"已登录用户重置密码检查", protocal="https")
    @login_required
    def get(self):
        phone = self.current_user.phone
        access_token = self.arg("user_key")
        openid = self.arg("openid")
        sms_code = self.arg("sms_code")

        if access_token == "" or openid == "":
            return self.write({"status": "fail", "error": "access_token or openid null!", "message_code": 3, })

        ucpass = SMS()
        result = ucpass.getCacheData(phone)

        if result != None:
            createDate = result['createDate']
            user_key = ucpass.get_access_token(phone, openid, createDate)
            if user_key != access_token:
                return self.write({"status": "fail", "error": _(u"非法用户"), "message_code": 3, })
            if sms_code != result['smsCode']:
                return self.write({"status": "fail", "error": _(u"验证码错误，请输入正确的验证码"), "message_code": 2, })
        else:
            return self.write({"status": "fail", "error": _(u"验证码失效"), "message_code": 2, })

        ucpass.delSmsCodeCache(phone)

        status = PhonePassword.reset_password_check(phone)
        if status:
            self.set_cookie("phone", phone, max_age=600)
            return self.write({"status": "success", "phone": phone, })
        else:
            return self.write({"status": "fail", "error": _(u"该手机号未注册"), "message_code": 1, })



@handler_define
class PhoneResetPassword(BaseHandler):
    @api_define("phone reset password", "/live/phone/reset/password", [
        Param("password", True, str, "", "", u"密码"),
    ], description=u"重置密码", protocal="https")
    def get(self):
        password = self.arg("password")
        phone = self.get_cookie("phone")
        self.clear_cookie("phone")
        if not phone:
            return self.write({"status": "fail", "error": "更改密码超时", })

        status = PhonePassword.update_password(phone, password)
        if status:
            user = User.objects.get(phone=phone)

            if user.is_blocked:
                logging.error("phone login error: blocked user")
                return self.write({"status": "fail", "error": _(u"您已被封号！请遵守用户协议！"), "errcode": "2001"})

            # convert user info
            data = {}
            data["user"] = convert_user(user)
            data['is_new'] = False

            # set cookie
            self.auth_login(user.id)
            app_id = settings.QCLOUD_LIVE_SDK_APP_ID

            data['sig'] = gen_signature(app_id, user.sid)
            data["status"] = "success"

            return self.write(data)
        else:
            return self.write({"status": "fail", "error": _(u"更改密码失败"), })


@handler_define
class SmsCode(ThridPardLogin):
    @api_define("",r'/live/sms/login',[
        Param('phone', False, str,"","18600023711",u'手机号'),
        Param('method', True, str, "0", "0", u"获取方式(0为注册,1为找回密码,2为修改密码,3为绑定手机号,4为提现登录)"),
        Param('sms_type', False, int, 1, 1, u"验证码类型（0为短信，1为语音)")
    ],description=u"获取验证码接口",protocal="https")
    def get(self):
        method = self.arg_int("method", 0)
        sms_type = self.arg_int("sms_type", 0)
        if method == 0:
            phone = self.arg('phone')
            status, user_phone = PhonePassword.create_phone(phone=phone)
            if not status:
                if user_phone:
                    return self.write({"status": "fail", "error": _(u"该手机号已注册"), "message_code": 1, })
                else:
                    return self.write({"status": "fail", "error": _(u"获取验证码失败"), "message_code": 3, })

        elif method == 1:
            phone = self.arg('phone')
            status = PhonePassword.reset_password_check(phone=phone)
            if not status:
                return self.write({"status": "fail", "error": _(u"该手机号未注册"), "message_code": 1, })

        elif method == 2:
            current_user = self.current_user
            if not current_user:
                return self.write({"status": "fail", "error": _(u"未登录"), "message_code": 3, })

            phone = current_user.phone
            if phone == "" or not phone:
                return self.write({"status": "fail", "error": _(u"未绑定手机号"), "message_code": 3, })
        elif method == 3:
            user_id = self.current_user_id
            phone = self.arg('phone')
            status, user_phone = PhonePassword.bind_user_check(phone=phone, user_id=user_id)
            if status:
                if user_phone:
                    return self.write({"status": "fail", "error": _(u"您已绑定过手机号"), "message_code": 3, })
                else:
                    return self.write({"status": "fail", "error": _(u"该手机号已被绑定, 请输入其他手机号"), "message_code": 1, })

        elif method == 4:
            phone = self.arg('phone')

        else:
            return self.write({"status": "fail", "error": _(u"获取验证码失败"), "message_code": 3, })
        if sms_type == 0:
            print 0
            usms = SMS()
        else:
            print 1
            usms = SMS(sms_type=1)
        reg = {}
        result = {}
        reg = usms.sendRegiesterCode(phone, method, sms_type)

        if reg['is_success'] != 1:
            return self.write({"status": "fail", "error": _(u"获取验证码失败"), "message_code": 3, })

        if reg['is_success'] == 1:
            result['status'] = "success"
            result['openId'] = reg['openId']
            result['user_key'] = reg['user_key']

        return self.write(result)


@handler_define
class BindVerifyCode(BaseHandler):
    @api_define("bind verify code", r'/live/user/bind/verify', [
        Param('user_key', True, str, "", "123456790", u'code,access_token'),
        Param('openid', True, str, "", "123456790", u'用户唯一标识,[支付宝用户id，微信用户id，微博用户id]'),
        Param("phone", True, str, "", "", u"手机号"),
        Param("sms_code", True, str, "", "", u"短信验证码"),
    ], description=u"绑定手机号验证")
    @login_required
    def get(self):
        access_token = self.arg("user_key")
        openid = self.arg("openid")
        phone = self.arg("phone")
        sms_code = self.arg("sms_code")

        if access_token == "" or openid == "":
            return self.write({"status": "fail", "error": "access_token or openid null!", "message_code": 3, })

        ucpass = SMS()
        result = ucpass.getCacheData(phone)

        if result != None:
            createDate = result['createDate']
            user_key = ucpass.get_access_token(phone, openid, createDate)
            if user_key != access_token:
                return self.write({"status": "fail", "error": _(u"非法用户"), "message_code": 3, })
            if sms_code != result['smsCode']:
                return self.write({"status": "fail", "error": _(u"验证码错误，请输入正确的验证码"), "message_code": 2, })
        else:
            return self.write({"status": "fail", "error": _(u"验证码失效"), "message_code": 2, })

        ucpass = SMS()
        ucpass.delSmsCodeCache(phone)

        return self.write({"status": "success", "phone": phone, })


@handler_define
class BindPhoneUser(BaseHandler):
    @api_define("Bind phone user", r'/live/user/bind/phone_user', [
        Param("phone", True, str, "", "", u"手机号"),
        Param("password", True, str, "", "", u"密码"),
    ], description=u"用户绑定手机号(设置密码)")
    @login_required
    def get(self):
        phone = self.arg("phone")
        password = self.arg("password")

        user_id = self.current_user_id
        status = PhonePassword.bind_user(phone=phone, user_id=user_id, password=password)

        phone = phone[0:3] + "*****" + phone[8:11]

        if status:
            return self.write({"status": "success", "phone": phone})
        else:
            return self.write({"status": "fail", "error": "绑定手机号失败", "message_code": 3, })


@handler_define
class BindWX(ThridPardLogin):
    """对微信传user_key就行了"""
    @api_define("BindWX", r'/live/user/bind_wx', [
        Param('user_key', True, str, "", "123456790", u'code,access_token'),
        Param('openid', True, str, "", "123456790", u'用户唯一标识,[支付宝用户id，微信用户id，微博用户id]'),
        Param('source', True, str, "", "1", u'用户来源[微信:1,微博:2,QQ:3，手机:4,友盟微信:5，测试:100]'),
        Param('nickname', False, str, "", "testuser3", u'用户名'),
        # Param('thumb', True, str, "", "", u'用户头像'),
    ], description=u"绑定微信")
    @login_required
    def get(self):
        source = self.arg_int('source')
        if not source == User.SOURCE_WEIXIN:
            return self.write({"status": "fail", "error": ":("})
        try:
            access_token = 'test_access_token'
            openid = 'test_openid'

            third_part = ThridPard.get_by_user(user_id=self.current_user_id)
            third_part.update_weixin_info(openid, access_token)

            self.write({"status": "success"})

        except Exception, e:
            return self.write({"status": "fail", "error": e.message})





@handler_define
class Logout(BaseHandler):
    @api_define("Logout", r'/live/logout', [
    ], description=u"注销接口")
    @login_required
    def get(self):
        user = self.current_user

        user.cid = ""
        user.save()
        self.auth_logout()
        # room_status = AudioRoomRecord.get_room_status(user_id=user.id)
        # if room_status == 1:
        #   AudioRoomRecord.set_room_status(user_id=user.id, status=1)
        #获取参数
        self.write({'status': "success"})


@handler_define
class UpdateSig(BaseHandler):
    @api_define("Update Sig", r'/sig/refresh', [
    ], description=u"更新腾讯云[独立]登录签名接口,会刷新cookie")
    @login_required
    def get(self):
        self.auth_login(self.current_user_id)
        app_id = settings.QCLOUD_LIVE_SDK_APP_ID
        data = {}
        data['sig'] = gen_signature(app_id, str(self.current_user.sid))
        data["status"] = "success"
        if self.current_user.complete_info == 0:
            data["is_new"] = True
            data.update(generate_default_info())
        else:
            data["is_new"] = False

        self.write(data)


@handler_define
class AUserInfo(BaseHandler):
    @api_define("User Info", r'/live/userinfo', [
        Param('uid', False, str, "", "", u'uid，默认当前用户信息'),
    ], description=u"获得用户信息")
    @login_required
    def get(self):

        if not self.has_arg('uid'):
            user = self.current_user
        else:
            user = User.objects.filter(id=self.arg('uid')).first()

        if self.current_user.is_blocked:
            return self.write({"status":"fail","error":_(u"您已被封号！请遵守用户协议！"),"errcode":"2001"})

        data = {"status": "success"}

        # TODO: 性能问题
        dic = {}
        dic = convert_user(user)
        dic["diamond"] = Account.objects.get(user=user).diamond
        dic["ticket"] = TicketAccount.objects.get(user=user).total_ticket
        dic["picture_count"] = PictureInfo.objects.filter(user_id=user.id, status=0).count()
        dic["audio_status"] = AudioRoomRecord.get_room_status(user_id=user.id)
        dic["check_real_name"] = RealNameVerify.check_user_verify(user_id=user.id)

        # 判断是否是vip
        user_vip = UserVip.objects.filter(user_id=user.id).first()
        if user_vip:
            vip = Vip.objects.filter(id=user_vip.vip_id).first()
            dic["vip"] = convert_vip(vip)

        data.update(dic)

        self.write(data)


# 个人主页
@handler_define
class UserHomepageV1(BaseHandler):
    @api_define("User homepage v1", r'/live/user/homepage_v1', [
        Param('home_id', True, str, "", "", u'个人主页用户id'),
    ], description=u"新版个人主页v1 <br>"
                   u"black_type    0:互相拉黑   1:已把对方拉黑  2:对方把您拉黑  3:均未拉黑<br>"
                   u"follow_type   0:未关注     1:已关注")
    def get(self):
        user_id = self.current_user_id

        home_id = self.arg_int('home_id')
        home_user = User.objects.get(id=home_id)

        personal_tags = UserTags.get_usertags(user_id=home_id)
        if not personal_tags:
            personal_tags = []

        data = {}
        data_pic = []
        pictures = PictureInfo.objects.filter(user_id=home_id, status=0).order_by('-created_at')
        for picture in pictures:
            if not user_id:
                is_like = False
                is_purchase = False
            else:
                is_purchase = PictureInfo.check_is_purchase(picture.id, user_id)
                is_like = PictureInfo.check_is_like(picture.id, user_id)

            if picture.lock_type == 0:
                is_purchase = True

            if is_purchase:
                dic = {
                    "picture": convert_picture(picture),
                    "is_purchase": is_purchase,
                    "is_like": is_like,
                    "user": convert_user(home_user),
                }
            else:
                dic = {
                    "picture": convert_picture(picture),
                    "is_purchase": is_purchase,
                    "is_like": is_like,
                    "user": convert_user(home_user),
                }
            data_pic.append(dic)

        if home_user.audio_room_id:
            audioroom = AudioRoomRecord.objects.get(id=home_user.audio_room_id)
        else:
            audioroom = None

        dic = {}
        dic["user"] = convert_user(home_user)
        if not audioroom:
            dic["audio"] = []
            dic["audio_status"] = 0
        else:
            dic["audio"] = convert_audioroom(audioroom=audioroom)
            dic["audio_status"] = AudioRoomRecord.get_room_status(user_id=home_id)
        dic["personal_tags"] = personal_tags
        dic["user"]["picture_count"] = PictureInfo.objects.filter(user_id=home_id, status=0).count()
        dic["picture"] = data_pic

        user_vip = UserVip.objects.filter(user_id=home_id).first()
        if user_vip:
            vip = Vip.objects.filter(id=user_vip.vip_id).first()
            dic["vip"] = convert_vip(vip)

        # 是否在线 查看心跳
        import time
        time = int(time.time())
        pre_time = time - 120
        user_beat = UserHeartBeat.objects.filter(user=home_user, last_report_time__gte=pre_time).first()
        if user_beat:
            is_online = 1
        else:
            is_online = 0

        # 判断是否了黑此用户
        black_type = BlackUser.is_black(user_id, home_id)

        # 判断是否关注此用户
        follow_type = FollowUser.is_follow_user(user_id, home_id)

        dic["follow_type"] = follow_type
        dic["black_type"] = black_type

        dic["is_online"] = is_online
        data.update(dic)

        self.write({"status": "success", "data": data, })


# 新版个人主页_new
@handler_define
class UserHomepageV2(BaseHandler):
    @api_define("User homepage v1", r'/live/user/homepage_v2', [
        Param('home_id', True, str, "", "", u'个人主页用户id'),
    ], description=u"精简_新版个人主页v2 <br>"
                   u"black_type    0:互相拉黑   1:已把对方拉黑  2:对方把您拉黑  3:均未拉黑<br>"
                   u"follow_type   0:未关注     1:已关注")
    def get(self):
        user_id = self.current_user_id

        home_id = self.arg_int('home_id')
        home_user = User.objects.get(id=home_id)

        personal_tags = UserTags.get_usertags(user_id=home_id)
        if not personal_tags:
            personal_tags = []

        data = {}
        data_pic = []
        pictures = PictureInfo.objects.filter(user_id=home_id, status=0).order_by('-created_at')
        for picture in pictures:
            pic_url = picture.picture_url
            if pic_url:
                data_pic.append(pic_url)

        dic = {}
        if home_user.audio_room_id:
            audioroom = AudioRoomRecord.objects.get(id=home_user.audio_room_id)
        else:
            audioroom = None

        dic["user"] = convert_user(home_user)
        if not audioroom:
            dic["audio"] = []
            dic["audio_status"] = 0
        else:
            dic["audio"] = convert_audioroom(audioroom=audioroom)
            dic["audio_status"] = AudioRoomRecord.get_room_status(user_id=home_id)

        dic["user"] = convert_user(home_user)
        dic["personal_tags"] = personal_tags
        dic["user"]["picture_count"] = PictureInfo.objects.filter(user_id=home_id, status=0).count()
        dic["picture_list"] = data_pic
        user_vip = UserVip.objects.filter(user_id=home_id).first()
        if user_vip:
            vip = Vip.objects.filter(id=user_vip.vip_id).first()
            dic["vip"] = convert_vip(vip)

        # 是否在线 查看心跳
        import time
        time = int(time.time())
        pre_time = time - 120
        user_beat = UserHeartBeat.objects.filter(user=home_user, last_report_time__gte=pre_time).first()
        if user_beat:
            is_online = 1
        else:
            is_online = 0

        # 判断是否了黑此用户
        black_type = BlackUser.is_black(user_id, home_id)

        # 判断是否关注此用户
        follow_type = FollowUser.is_follow_user(user_id, home_id)

        dic["follow_type"] = follow_type
        dic["black_type"] = black_type

        dic["is_online"] = is_online

        # 我的动态相关
        temp_moments = UserMoment.objects.filter(user_id=home_id, show_status__ne=2, delete_status=1).order_by("-create_time")
        count = 0
        moment_img_list = []
        moment_count = UserMoment.objects.filter(user_id=home_id, show_status__ne=2, delete_status=1).count()
        for moment in temp_moments:
            if count > 10:
                break

            imgs = moment.img_list
            if not imgs:
                continue

            for img in imgs:
                if img["status"] == 1:
                    moment_img_list.append(img["url"])
                    count += 1
                    break
        if not moment_img_list:
            moment = UserMoment.objects.filter(user_id=home_id, show_status__ne=2, delete_status=1).order_by("-create_time").first()
            if moment:
                dic["content"] = moment.content
            else:
                dic["content"] = ""

        dic["moment_img_list"] = moment_img_list
        dic["moment_count"] = moment_count
        data.update(dic)
        self.write({"status": "success", "data": data, })


# 用户照片
@handler_define
class AUserPicture(BaseHandler):
    @api_define("User picture", r'/live/user/picture', [
        Param('user_id', True, str, "", "", u'用户id'),
        Param('page', False, str, "1", "1", u'page'),
        Param('page_count', False, str, "10", "10", u'page_count'),
    ], description=u"用户照片列表")
    def get(self):
        user_id = self.arg('user_id')
        current_user_id = self.current_user_id
        page = self.arg_int('page', 1)
        page_count = self.arg_int('page_count', 20)
        pictures = PictureInfo.get_user_picture(user_id=user_id, page=page, page_count=page_count)
        data = []
        for picture in pictures:
            if not current_user_id:
                is_like = False
                is_purchase = False
            else:
                is_purchase = PictureInfo.check_is_purchase(picture.id, current_user_id)
                is_like = PictureInfo.check_is_like(picture.id, current_user_id)

            if picture.lock_type == 0:
                is_purchase = True
            user = User.objects.get(id=user_id)
            if is_purchase:
                dic = {
                    "picture": convert_picture(picture),
                    "user": convert_user(user),
                    "is_purchase": is_purchase,
                    "is_like": is_like,
                }
            else:
                dic = {
                    "picture": convert_picture(picture),
                    "user": convert_user(user),
                    "is_purchase": is_purchase,
                    "is_like": is_like,
                }
            data.append(dic)

        self.write({"status": "success", "data": data, })


@handler_define
class BatchUserInfo(BaseHandler):
    @api_define("Batch User Info", r'/live/batch/get/userinfo', [
        Param('uids', False, str, "", "", u'用户_uid逗号分隔，例如：1,2,3，腾讯云是identity'),
    ], description=u"批量获取用户信息")
    def get(self):
        try:
            uids = self.arg("uids")
            uids = uids.split(",")

            results = []
            users = User.objects.filter(id__in=uids)
            for user in users:
                results.append(convert_user(user))

            data = {"status": "success", "results": results}

            self.write(data)
        except Exception, e:
            self.write({"status":"fail", "desc": e.message})


# 更新用户cid
@handler_define
class UpdateClientID(BaseHandler):
    @api_define("User Update Client ID", r'/live/clientid', [
        Param('client_id', True, str, "", "", u'push使用的Client ID'),
        Param('platform', True, str, "", "", u'设备系统（android:0/IOS:1/其他:2）'),
        Param('osver', True, str, "", "", u'设备系统版本号'),
    ], description=u"更新用户push相关信息")
    @login_required
    def get(self):
        user = self.current_user
        cid = self.arg("client_id")
        platform = self.arg_int("platform")
        osver = self.arg("osver")
        ua = self.request.headers.get('User-Agent')
        app_name = ua.split(";")[0]
        if user:
            user.upload_client_id(cid, platform, osver, app_name)
            data = {"status": "success"}
        else:
            data = {"status": "fail", "error": "need login"}
        self.write(data)


# 更新用户个人信息
@handler_define
class UpdateUserInfo(BaseHandler):
    @api_define("UpdateUserInfo", r'/live/user/edit', [
        Param('desc', True, str, "", "", u'描述'),
        Param('gender', True, str, "", "", u'性别 1男，2女'),
        Param('nickname', True, str, "", "", u'昵称'),
        Param('logo', True, str, "", "", u'logo'),
        Param('area', True, str, "", "", u'area'),
        Param('occupation', True, str, "", "", u'职业'),
        Param('blood_type', True, str, "", "", u'血型'),
        Param('birth_date', True, str, "", "", u'生日'),  # 回传字符串类型如'2016-01-01'
        Param('emotional', True, str, "", "", u'情感状态'),
        Param('cover', False, str, "", "", u'封面')
    ], description=u"更新用户信息")
    @login_required
    def get(self):
        user = self.current_user

        is_change = False
        is_nickname_change = False
        is_desc_change = False
        is_image_change = False
        is_cover_change = False

        if self.has_arg("desc") and user.desc != self.arg("desc"):
            if len(self.arg("desc")) > 32:
                return self.write({'status': "fail",
                                   'param': 'desc',
                                   'error': "Desc length needs to be less than 32"})
            if self.arg("desc") != user.desc:
                is_desc_change = True
                user.desc = self.arg("desc")

            is_change = True

        if self.has_arg("gender"):
            user.gender = self.arg_int("gender")
            is_change = True

        if self.has_arg("logo"):
            # user.image = self.arg("logo")
            logo = User.convert_http_to_https(self.arg("logo"))
            if logo != user.image:
                is_image_change = True
                user.image = User.convert_http_to_https(self.arg("logo"))
            is_change = True

        if self.has_arg("nickname"):
            if len(self.arg("nickname")) > 16:
                return self.write({'status': "fail",
                                   'param': 'nickname',
                                   'error': "Nickname length needs to be less than 16"})
            if self.arg("nickname")!= user.nickname:
                is_nickname_change = True
                nickname = self.arg("nickname")

                # 昵称鉴黄
                ret, duration = shumei_text_spam(text=user.nickname, timeout=1, user_id=user.id, channel=1, nickname=nickname,
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
                    # user.update(set__nickname="爱聊用户" + str(user.identity))
                    text_detect = TextDetect()
                    text_detect.user = user
                    text_detect.text_channel = 1
                    text_detect.text = user.nickname
                    text_detect.created_time = datetime.datetime.now()
                    text_detect.save()
                    return self.write({'status': "fail",
                                       'param': 'nickname',
                                       'error': u"经系统检测,您的昵称内容涉及违规因素,请重新编辑"})
                user.nickname = nickname
                is_change = True

        if self.has_arg("area"):
            if len(self.arg("area")) > 10:
                return self.write({'status': "fail",
                                   'param': 'area',
                                   'error': "Area length needs to be less than 10"})
            user.area = self.arg("area")
            is_change = True

        if self.has_arg("occupation"):
            if len(self.arg("occupation")) > 32:
                return self.write({'status': "fail",
                                   'param': 'occupation',
                                   'error': "Occupation length needs to be less than 32"})
            user.occupation = self.arg("occupation")
            is_change = True

        if self.has_arg("blood_type"):
            user.blood_type = self.arg("blood_type")
            is_change = True

        if self.has_arg("birth_date"):
            birth_date = self.arg("birth_date")
            user.birth_date = datetime.datetime.strptime(birth_date, '%Y-%m-%d')
            user.constellation = User.zodiac(birth_date)
            is_change = True

        if self.has_arg("emotional"):
            emotional = self.arg("emotional")
            user.emotional = emotional
            is_change = True
        if self.has_arg("cover"):
            cover = User.convert_http_to_https(self.arg("cover"))
            if cover != user.cover and self.arg("cover") != user.cover:
                user.cover = self.arg("cover")
                is_cover_change = True
            is_change = True
        if is_change:
            user.save()

        # if is_nickname_change:
        #     MessageSender.send_text_check(user.nickname, user.id, 1, self.user_ip)
        if is_desc_change:
            MessageSender.send_text_check(user.desc, user.id, 3, self.user_ip)
        if is_image_change:
            MessageSender.send_picture_detect(pic_url=user.image, user_id=user.id, pic_channel=2, source=1)
        if is_cover_change:
            MessageSender.send_picture_detect(pic_url=user.cover, user_id=user.id, pic_channel=1, source=1)


        self.write({'status': "success"})


# 漂流瓶开关
@handler_define
class ChangeBottleSwitch(BaseHandler):
    @api_define("update bottle switch", r'/live/user/bottle_switch', [
        Param("bottle_switch", True, str, "", "", u"漂流瓶开关(0关闭, 1开启)")
    ], description=u"漂流瓶开关(0关闭, 1开启)")
    @login_required
    def get(self):
        user = self.current_user
        bottle_switch = self.arg_int("bottle_switch", 1)

        user.bottle_switch = bottle_switch
        user.save()
        self.write({"status": "success", })


# 展示所有个人标签
@handler_define
class ShowPersonalTags(BaseHandler):
    @api_define("Show personal tags", r'/live/user/personal_tags',[], description=u"所有个人标签")
    @login_required
    def get(self):
        tags = TagTimes.get_taglist()
        data = []
        for tag in tags:
            dic = {
                "tag_name": tag.tag_name,
            }
            data.append(dic)

        self.write({"status": "success", "data": data, })


# 修改个人标签
@handler_define
class UpdatePersonalTags(BaseHandler):
    @api_define("Update personal tags", r'/live/user/update/personal_tags', [
        Param('tag_str', True, str, "", "", u'personal_tag')
    ], description=u"修改个人标签")
    @login_required
    def get(self):
        user_id = self.current_user_id
        tag_str = self.arg("tag_str", "")
        status = UserTags.update_usertags(user_id=user_id, tag_str=tag_str)
        if status:
            self.write({"status": "success", })
        else:
            self.write({"status": "failed", })


@handler_define
class GetSign(BaseHandler):
    @api_define("Image Get Sign", r'/live/image/get/sign', [
        Param('type', True, str, "upload", "upload", u'type'),
        Param('file_id', True, str, "ceshi", "ceshi", u'fileid'),
    ], description="万象获得sig")
    def get(self):
        import tencentyun
        from tencentyun import conf
        import time

        # TODO: heydoshow 加入了token，导致样式需要验证才能通过，所以暂时先修改为hdlive
        bucket = 'pornverify'
        secret_id = 'AKIDgknyBYkNKnpONeweTRwK9t6Nn0jn78yG'
        secret_key = 'fBCXVJK1PpWPtYizb7vIGVMIJFm90GBa'
        conf.set_app_info(
            appid='10048692',
            secret_id=secret_id,
            secret_key=secret_key,

        )

        file_id = self.get_argument('file_id', 'dd')
        expired = int(time.time()) + 999

        # url = image.generate_res_url_v2(bucket, userid, file_id)
        auth = tencentyun.Auth(secret_id, secret_key)
        sign = auth.get_app_sign_v2(bucket, file_id, expired)
        ret = {'status':'success', 'sign': sign, 'bucket':bucket}
        self.write(ret)


@handler_define
class OpenIDRegister(BaseHandler):
    @api_define("unionid id is Register", r'/live/get/openid/isregister', [
        Param('unionid', True, str, "", "", u'unionid'),
    ], description="unionid是否注册过，微信渠道")
    def get(self):
        user = User.objects.filter(source=User.SOURCE_WEIXIN,openid=self.arg("unionid")).first()
        if user:
            data = {"status": "success","is_new":False,"user":convert_user(user)}
        else:
            data = {"status": "success","is_new":True}

        self.write(data)


@handler_define
class ReportLog(BaseHandler):
    @api_define("report error logs", r'/live/report/logs', [
        Param('user_id', False, str, "", "", u'user_id'),
        Param('message',False,str,"","",u'message'),
    ], description=u"上传错误日志")
    @login_required
    def get(self):
        try:
            user_id = self.arg("user_id")
            guid = self.arg("guid")
            message = self.arg("message")
            t = self.arg("t")
            sig = self.arg("sig")
            data  = 'IOS LOG: user_id=%s;message=%s' % (user_id,message)
            logging.error(data)
            self.write({'status': "success"})
        except Exception,e:
            self.write({'status': "fail"})


@handler_define
class ReportIOSLog(BaseHandler):
    @api_define("report error ioslogs", r'/live/report/ioslogs', [
        Param('filename', False, str, "", "", u'filename'),
        Param('data',False,str,"","",u'data'),
    ], description=u"上传错误日志")
    @login_required
    def post(self):
        try:
            filename = self.get_argument("filename")
            data = self.get_argument("data")
            upload_path=os.path.join(os.path.dirname("/mydata/logs/"),filename)

            up = open(upload_path,'wb')
            up.write(data)
            up.close()

            self.write({'status': "success"})
        except Exception,e:
            self.write({'status': "fail"})


# 用户反馈
@handler_define
class CreateFeedback(BaseHandler):
    @api_define("create feedback", r'/live/feedback',[
        Param("desc", True, str, "", "", u'反馈描述'),
        Param("feedbackphone", False, str, "", "", u'反馈手机号码'),
        Param("feedbackqq", False, str, "", "", u'反馈人的QQ号码')
        #Param("mobile_type", True, str, "", "", u'手机类型'),
    ], description=u"创建用户反馈")
    @login_required
    def get(self):
        user_id = self.current_user_id
        desc = self.arg("desc", "")
        ua = self.request.headers.get('User-Agent')
        phone_number = self.arg("feedbackphone", "")
        qq_number = self.arg("feedbackqq", "")
        created_at = datetime.datetime.now()
        status = FeedbackInfo.check_feedback(user_id=user_id, created_at=created_at)
        if status:
            self.write({"status": "success", "error_message": "每天只能发送一次", })

        else:
            feedback_id = FeedbackInfo.create_feedback(user_id=user_id, created_at=created_at, ua=ua,
                                                       desc=desc,phone_number=phone_number,qq_number=qq_number)
            if feedback_id:
                desc = u"<html><p>" + _(u"尊敬的%s，感谢您的建议，您的建议就是我们进步的动力" % self.current_user.nickname) + u"</p></br></html>"

                MessageSender.send_system_message(user_id, desc)
                self.write({"status": "success", "feedback_id": feedback_id, })
            else:
                self.write({"status": "failed", "error_message": "创建反馈失败", })


# 登录成功改为上线
@handler_define
class CheckAudio(BaseHandler):
    @api_define("check audio", r'/live/checkaudio', [], description=u"检查语音是否离线")
    @login_required
    def get(self):
        user_id = self.current_user_id
        audio_status = AudioRoomRecord.get_room_status(user_id=user_id)
        if audio_status == 4:
            status = AudioRoomRecord.set_room_status(user_id=user_id, status=1)
            if status:
                self.write({"status": "success", "audio":"set room status success" })
            else:
                self.write({"status": "failed", "error": "set room status error"})
        else:
            self.write({"status": "success", })


# 用户地理位置更新
@handler_define
class UpdateLocation(BaseHandler):
    @api_define("update location", r'/live/update_location', [
        Param("country", False, str, "CN", "CN", u'国家'),
        Param("province", False, str, "Beijing", "Beijing", u"省"),
        Param("city", False, str, "Beijing", "Beijing", u"城市"),
        Param("district", False, str, "", "", u"区"),
        Param("longitude", False, str, "", "", u"经度"),
        Param("latitude", False, str, "", "", u"纬度"),
    ], description=u"更新用户地理位置")
    @login_required
    def get(self):
        user_id = self.current_user_id
        country = self.arg("country", "")
        province = self.arg("province", "")
        city = self.arg("city", "")
        district = self.arg("district", "")
        longitude = float(self.arg("longitude", "0.00"))
        latitude = float(self.arg("latitude", "0.00"))

        status = User.update_location(user_id, country, province, city, district, longitude, latitude)

        if status:
            self.write({"status": "success", })
        else:
            self.write({"status": "failed", })


# 腾讯云上下线回调
@handler_define
class IMOnlineOfflineCallback(BaseHandler):
    @api_define("IM online/offline callback", r'/live/user/imcallback', [], description=u"腾讯上下线回调")
    def post(self):

        body = self.request.body
        result = json.loads(body)
        user_info = result.get("Info")

        user_id = int(user_info.get("To_Account", 0))
        action = user_info.get("Action")
        if user_id:  # 正式服id从2500开始 测试服id从1开始
            user = User.objects.get(id=user_id)

            status = OnlineUser.update_online_user(user_id=user_id, action=action)
            if status:
                self.write({"status": "success"})
            else:
                self.write({"status": "failed"})
        else:
            self.write({"status": "failed"})


# 新版在线列表
@handler_define
class OnlineUserListV1(BaseHandler):
    @api_define("Online user list v1", r'/live/user/online_user_v1', [
        Param('method', True, str, "0", "0", u"排序方式(0默认,1男性,2女性)"),
        Param('page', True, str, "1", "1", u'page'),
        Param('page_count', True, str, "10", "10", u'page_count'),
        Param('time_stamp', False, str, "", "", u'最后一个人的时间戳(page=1不用传)'),
    ], description=u"新版在线列表")
    def get(self):
        page = self.arg_int('page')
        page_count = self.arg_int('page_count')
        method = self.arg_int('method', 0)

        result_advs = []
        if page == 1:
            advs = Adv.get_list()
            for adv in advs or []:
                result_advs.append(adv.normal_info())

        if page == 1:
            query_time = datetime.datetime.now()
        else:
            time_stamp = float(self.arg('time_stamp'))
            query_time = datetime.datetime.fromtimestamp(time_stamp)

        online_user = OnlineUser.get_list_v1(query_time=query_time, method=method, page=page, page_count=page_count)
        data = []
        for user in online_user:
            dic = {
                "user": convert_user(user.user),
                "audio_status": AudioRoomRecord.get_room_status(user.user.id),
                "time_stamp": OnlineUser.get_timestamp(user.user),
            }
            data.append(dic)

        self.write({"status": "success", "data": data, "banners": result_advs, })


# 分享
@handler_define
class ShareHandler(BaseHandler):
    @api_define("share handler", r'/live/user/share', [
        Param('share_channel', True, str, "", "", u"分享渠道(0微信好友, 1朋友圈, 2QQ好友, 3QQ空间, 4微博)")
    ], description=u"分享")
    @login_required
    def get(self):
        user_id = int(self.current_user_id)
        guid = self.arg("guid")
        share_channel = self.arg_int("share_channel", 0)

        share_status = ShareInfo.check_shareinfo(guid=guid, user_id=user_id, share_channel=share_channel)
        if share_status:
            ShareInfo.create_shareinfo(guid=guid, user_id=user_id, share_channel=share_channel)
            return self.write({"status": "success", "share_status": 2, })
        else:
            status = ShareInfo.create_shareinfo(guid=guid, user_id=user_id, share_channel=share_channel)
            if status:
                GiftManager.share_bill(user_id=user_id, diamon=50)
                return self.write({"status": "success", "share_status": 1, "share_money": 50, })
            else:
                return self.write({"status": "fail", "share_status": 0, })


# 消息门槛
@handler_define
class MessageCheck(BaseHandler):
    @api_define("message check", r'/live/user/message/check', [
        Param("receive_id", True, str, "", "", u"收礼人用户id"),
    ], description=u"消息门槛检测")
    @login_required
    def get(self):
        send_id = int(self.current_user_id)
        send_user = self.current_user
        receive_id = self.arg_int("receive_id")
        if send_user.gender == 2:
            return self.write({"status": "success", "friend_status": True, })

        status, friend_status = ChatMessageLimit.check_friends(send_id=send_id, receive_id=receive_id)
        if status:
            if friend_status:
                return self.write({"status": "success", "friend_status": True, })
            else:
                message_gift = Gift.objects.filter(gift_type=3, status=1).first()
                data = {
                    "id": str(message_gift.id),
                    "name": message_gift.name,
                    "price": message_gift.price,
                    "logo": message_gift.logo,
                    "logo_small": message_gift.logo_small,
                    "wealth_value": message_gift.wealth_value,
                    "charm_value": message_gift.charm_value,

                }

                return self.write({"status": "success", "friend_status": False, "gift":data})
        else:
            return self.write({"status": "fail",})


# 消息门槛检测_v1
@handler_define
class MessageCheckV1(BaseHandler):
    @api_define("message check v1", r'/live/user/message/check_v1', [
        Param("receive_id", True, str, "", "", u"收礼人用户id"),
    ], description=u"消息门槛检测_V1")
    @login_required
    def get(self):
        send_id = int(self.current_user_id)
        send_user = User.objects.filter(id=send_id).first()
        receive_id = self.arg_int("receive_id")

        # 判断是否是主播.主播没有门槛
        if send_user.is_video_auth == 1:
            return self.write({"status": "success", "chat_status": True})

        tool = Tools.objects.filter(tools_type=0).first()
        record = SendToolsRecord.objects.filter(send_id=send_id, receive_id=receive_id, tools_id=str(tool.id)).first()
        if record:
            return self.write({"status": "success", "chat_status": True})

        tools_count = UserTools.objects.filter(user_id=send_id, tools_id=str(tool.id)).sum("tools_count")
        data = {
            "tool": convert_tools(tool),
            "count": tools_count
        }
        return self.write({"status": "success", "chat_status": False, "data": data})


# 消息门槛送礼物
@handler_define
class MessageSendGift(BaseHandler):
    @api_define("message send gift", r'/live/user/message/send_gift', [
        Param("receive_id", True, str, "", "", u"收礼人用户id"),
    ], description=u"消息门槛送礼物")
    @login_required
    def get(self):
        send_id = int(self.current_user_id)
        receive_id = self.arg_int("receive_id")
        #此处暂有一个门槛礼物 写死100
        bill_status, return_money = GiftManager.message_bill(send_id=send_id, receive_id=receive_id, money=100)
        if not bill_status:
            return self.write({"status": "fail", "error": u"支付失败", })
        else:
            if return_money == 0:
                return self.write({"status": "fail", "error": _(u"余额不足"), })
            else:
                return self.write({"status": "success", })


# 消息门槛送礼物 新版 发道具
@handler_define
class MessageSendToolV1(BaseHandler):
    @api_define("message send gift_v1", r'/live/user/message/send_tool_v1', [
        Param("receive_id", True, str, "", "", u"收礼人用户id"),
    ], description=u"消息门槛送礼物_v1 新版")
    @login_required
    def get(self):
        send_id = int(self.current_user_id)
        receive_id = self.arg_int("receive_id")

        tool = Tools.objects.filter(tools_type=0).first()

        # 判断道具, 有就发道具
        status = UserTools.has_tools(send_id, str(tool.id))
        if status == 1:
            # 消耗道具
            UserTools.reduce_tools(send_id, str(tool.id))
            # 添加记录
            SendToolsRecord.add(send_id, receive_id, str(tool.id), 1)
            return self.write({"status": "success"})
        else:
            return self.write({"status": "fail", "error": _(u"无可用门槛道具"), })



@handler_define
class RealNameInfoSubmit(BaseHandler):
    @api_define("real_name_verify", r'/live/user/real_name', [
        Param("uid", True, str, "", "", u"用户id"),
        Param("uName", True, str, "", "", u"姓名"),
        Param("IdNum", True, str, "", "", u"身份证号"),
        Param("pic_1", True, str, "", "", u"实名认证图片1"),
        Param("pic_2", True, str, "", "", u"实名认证图片2"),
        Param("pic_3", True, str, "", "", u"实名认证图片3"),
    ], description=u"实名认证")
    def get(self):
        user_id = self.arg_int("uid")
        user_name = self.get_argument("uName")
        id_num = self.get_argument("IdNum")

        if not user_id or not user_name or not id_num:
            return self.write({"status": "failed", "error": "no detail", })

        if self.has_arg("pic_1") and self.has_arg("pic_2") and self.has_arg("pic_3"):
            url_1 = self.arg("pic_1")
            url_2 = self.arg("pic_2")
            url_3 = self.arg("pic_3")
            status = RealNameVerify.create_real_name_verify(user_id=user_id, real_name=user_name, identity_code=id_num,
                                                            picture_one=url_1, picture_two=url_2, picture_three=url_3)
            if status:
                return self.write({"status": "success", })
            else:
                return self.write({"status": "failed", "error": "create verify error", })
        else:
            return self.write({"status": "failed", "error": "file no enough", })



@handler_define
class RealNameCheck(BaseHandler):
    @api_define("real name check", r'/live/user/real_name/check', [], description=u"实名认证检查 0:审核中 1:通过 2:未通过 3:未审核")
    @login_required
    def get(self):
        user = self.current_user
        status = RealNameVerify.check_user_verify(user_id=user.id)

        self.write({"status": "success", "check_real_name": status, })

#@handler_define
#class H5VideoCheck(BaseHandler):
    #@api_define("video check", r'/live/video/check',
               # [])


@handler_define
class VideoAuthCheck(BaseHandler):
    @api_define("video manager define", r'/live/user/video/auth/check',
                [],
                description=u"视频播主认证检查")
    @login_required
    def get(self):
        user = self.current_user
        status = VideoManagerVerify.check_video_manager_verify(user_id=user.id)
        self.write({
            "status": "success", "check_video_auth": status,
        })


@handler_define
class VideoAuthInfoSubmit(BaseHandler):
    @api_define("video auth info submit", r'/live/user/video/auth/submit',
                [Param("user_id", True, int, "", "", u'实名认证用户id'),
                 Param("avatar_pic", True, str, "", "", u'头像图片'),
                 Param("active_pic", False, str, "", "", u'动作图片'),
                ],
                description=u"视频播主信息提交"
                )
    def get(self):
        user_id = self.arg_int("user_id")
        avatar_auth = self.arg("avatar_pic")
        active_auth = self.arg("active_pic", "")

        if not user_id or not avatar_auth :
            return self.write({
                "status": "falied",
                "error": "lack argument",
            })
        else:
            status = VideoManagerVerify.create_video_manager_verify(user_id=user_id, avtar_auth=avatar_auth,
                                                                    active_auth=active_auth)
            if status:
                self.write({
                    "status": "success",
                })
            else:
                self.write({
                    "status": "failed",
                    "error": "create real name failed",
                })

@handler_define
class NoDisturbSwitch(BaseHandler):
    @api_define("set no_disturb_mode", r"/live/user/disturb/setting",[
                Param("disturb_mode", True, int, 0, 0, u"勿扰模式 0：可以打扰 1：勿扰")
                ], description=u"勿扰模式"  )
    @login_required
    def get(self):
        user_id = self.current_user_id
        disturb_mode = self.arg_int("disturb_mode")
        result = User.set_disturb_mode(user_id, disturb_mode)
        if result:
            self.write({
                "status": "success",
            })
        else:
            self.write({
                "status": "failed",
            })


@handler_define
class UserHeartBeatReport(BaseHandler):
    @api_define("user hearbeat", r"/live/user/heartbeat",[
        Param("user_id", False, str, 0, 0, description=u"当前用户uid")
    ], description=u"用户上报心跳")
    def get(self):
        user_id = self.current_user_id
        if self.has_arg("user_id"):# androi多进程导致token可能是上一个登录的人的token
            user_id = self.arg("user_id")
        ua = self.request.headers.get('User-Agent')
        uas = ua.split(";")
        if uas[2] == "iPhone" or uas[2] == "iPad":
            platform = 1
        elif uas[2]=="Android":
            platform = 0
        else:
            platform = 2
        user = User.objects.get(id=int(user_id))
        heart_beat = UserHeartBeat.objects.get(user=user)
        heart_beat.last_report_time = int(time.time())
        heart_beat.app_name = uas[0]
        heart_beat.app_version = uas[1]
        heart_beat.platform = platform
        # todo 下面的report_report 需要减去当天0点的秒数
        coefficient = 2 if heart_beat.user.is_video_auth == 1 else 1
        heart_beat.user.current_score = random.random() + heart_beat.last_report_time / (5 * UserHeartBeat.REPORT_INTERVAL) * coefficient
        heart_beat.user.save()
        heart_beat.save()
        self.write({"status": "success"})

@handler_define
class UserReport(BaseHandler):
    @api_define("report", r'/live/user/report',[
        Param("user_id", True, int, 0, 1, description=u"举报人id"),
        Param("report_uid",False, int, 0, 1, description=u"举报用户的id"),
        Param("content", False, str, "0", "this is a test report", description=u"举报用户的id")
    ],description=u"举报接口")
    @login_required
    def post(self):
        return self.write({"status": "success"})

@handler_define
class RichUserList(BaseHandler):
    @api_define("rich user list ", r'/live/user/rich_list', [], description=u"千里眼 土豪列表 5个")

    @login_required
    def get(self):

        # 查看此人是否有千里眼道具
        user_id = int(self.current_user_id)
        user = User.objects.filter(id=user_id).first()
        tool = Tools.objects.filter(tools_type=2).first()
        tools_count = UserTools.objects.filter(tools_id=str(tool.id), user_id=user_id).count()
        if tools_count == 0:
            account = Account.objects.filter(user=user).first()
            try:
                account.diamond_trade_out(price=tool.price, desc=u"千里眼消耗金额", trade_type=TradeDiamondRecord.TradeTypeClairvoyant)
            except ApiException, e:
                return self.write({"status": "success", "error": _(u"余额不足")})

        else:
            # 用户减少一个道具,  消耗道具记录
            UserTools.reduce_tools(user_id, str(tool.id))

        temp_ranks = ClairvoyantRank.objects.all()

        user_ids = []
        for r in temp_ranks:
            user_ids.append(r.user_id)

        # 判断本人是否在列表中
        if user_id in user_ids:
            user_ids.remove(user_id)
        else:
            user_ids = user_ids[:5]


        data = []
        if user_ids:
            for userid in user_ids:
                user = User.objects.filter(id=userid).first()
                user_vip = UserVip.objects.filter(user_id=userid).first()
                account = Account.objects.filter(user=user).first()
                if not user_vip:
                    dic = {
                        "user": convert_user(user),
                        "diamond": account.diamond
                    }
                else:
                    vip = Vip.objects.filter(id=user_vip.vip_id).first()
                    dic = {
                        "user": convert_user(user),
                        "diamond": account.diamond,
                        "vip": convert_vip(vip)
                    }
                data.append(dic)

        data.reverse()

        return self.write({"status": "success", "data": data, "has_tools": 1})


@handler_define
class OnlineChargeCount(BaseHandler):
    @api_define("online charge count", "/live/user/online_charge_count",
                [], description=u"聊友在线人数,土豪充值人数")
    def get(self):

        count = OnlineCount.objects.all().first()
        if not count:
            count = OnlineCount()
            online_count = random.randint(500, 1000)
            charge_count = random.randint(200, 500)
            count.online_count = online_count
            count.charge_count = charge_count
            count.update_time = datetime.datetime.now()
            count.save()
        else:
            now = datetime.datetime.now()
            if count.update_time + datetime.timedelta(minutes=1) > now:
                online_count = count.online_count
                charge_count = count.charge_count

            else:
                online_delta = random.randint(-20, 20)
                charge_delta = random.randint(-10, 10)

                count.update(inc__online_count=online_delta)
                count.update(inc__charge_count=charge_delta)
                online_count = count.online_count
                charge_count = count.charge_count
                count.update(set__update_time=now)

        return self.write({
            "status": "success",
            "online_count": online_count,
            "charge_count": charge_count
        })


#Post 需要测试负载均衡
@handler_define
class UserAppeal(BaseHandler):
    @api_define("user appeal ", "/live/user/appeal", [
        Param("user_id", True, int, 0, 1, description=u"用户id"),
        Param("reason", False, str, "", "", description=u"申诉理由"),
        Param("phone", False, str, "", "", description=u"手机号码")

    ], description=u"申诉接口")
    def get(self):
        user_id = self.arg_int("user_id")
        reason = self.arg("reason", "")
        phone = self.arg("phone", "")
        guid = self.arg("guid", "")

        user = User.objects.get(id=user_id)
        UserAppealRecord.create_user_appeal_record(user, reason, phone, guid)



@handler_define
class AliAuthRedirect(BaseHandler):
    @api_define("ali auth redirect", "/live/user/aliAuth",[], description=u"支付包授权回调")
    def post(self):
        pass


#  猜你喜欢.  先从表中取,如果>3 条记录符合.直接返回. 如果不足,再重新获取,补足三条
@handler_define
class RecommendUserList(BaseHandler):
    @api_define("recommend user list ", "/live/recommend_user/list", [], description=u"猜你喜欢")
    def get(self):
        data = []
        user_ids = []
        recommend_list = RecommendUser.objects.filter(is_valid=1)
        # 获取当前时间的前五分钟
        import time
        time = int(time.time())
        pre_time = time - 60 * 2
        for recommend_user in recommend_list:
            user_id = recommend_user.user_id
            user = User.objects.filter(id=user_id).first()
            user_beat = UserHeartBeat.objects.filter(user=user, last_report_time__gte=pre_time)
            if user_beat:
                user_vip = UserVip.objects.filter(user_id=user_id).first()
                if not user_vip:
                    dic = {
                        "user": convert_user(user)
                    }
                else:
                    vip = Vip.objects.filter(id=user_vip.vip_id).first()
                    dic = {
                        "user": convert_user(user),
                        "vip": convert_vip(vip)
                    }
                data.append(dic)
                user_ids.append(user_id)

        count = len(data)

        if count < 3:
            need_count = 3 - count
            users = User.objects.filter(is_video_auth=1, gender=2, audio_room_id__ne="", disturb_mode=0,
                                        id__nin=user_ids).order_by("-current_score")[0:need_count]
            for u in users:
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





