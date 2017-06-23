# coding=utf-8
from django.db import models
import logging
from django.db.models import Q
from app.customer.common_util.image import UploadImage
from base.core.util.dateutils import datetime_to_timestamp
import time
import datetime
from mongoengine import *
from base.settings import CHATPAMONGO
import random
from app.util.messageque.msgsender import MessageSender
from app_redis.user.models.user import UserRedis

connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,password=CHATPAMONGO.password)


class User(Document):
    SOURCE = [
        (0, u"自有注册"),
        (1, u'微信'),
        (2, u'微博'),
        (3, u'QQ'),
        (4, u"手机"),
        (5, u"友盟微信"),
        (100, u"测试登录"),
        ("100", u"测试登录")
    ]

    SOURCE_WEIXIN = 1
    SOURCE_WEIBO = 2
    SOURCE_QQ = 3
    SOURCE_PHONE = 4
    SOURCE_YOUMENG_WEIXIN = 5

    PLATFORM = [
        (0, u'Android'),
        (1, u'IOS'),
        (2, u'其他')
    ]

    ROBOT = [
        (0, u'用户'),
        (1, u'机器人'),
        (2, u'小号'),
        (100, u'工会管理员'),
        (101, u'家族族长')
    ]

    EMOTIONAL = [
        (0, u'未填写'),
        (1, u'单身'),
        (2, u'恋爱中'),
        (3, u'已婚'),
    ]

    COMPLETE_INFO = [
        (0, u'未完善'),
        (1, u'已完善'),
    ]

    BOTTLE_SWITCH = [
        (0, u'关闭'),
        (1, u'开启'),
    ]

    NO_DISTURBB_ON =[
        (0, u'关闭'),
        (1, u'开启')
    ]

    ONLINE_STATUS = [
        (1, u'在线'),
        (2, u'离线')
    ]

    # 用户id信息
    id = IntField(verbose_name=u'id', primary_key=True)
    identity = IntField(verbose_name=u"用户id", unique=True)
    openid = StringField(verbose_name=u"openid", max_length=64, unique=True)
    is_block = IntField(verbose_name=u'是否屏蔽', default=0)
    complete_info = IntField(verbose_name=u'是否完善过个人信息', choices=COMPLETE_INFO)
    user_type = IntField(verbose_name=u'用户类型', choices=ROBOT)
    guid = StringField(verbose_name=u'用户设备号')
    is_valid = IntField(verbose_name=u'是否不入库',default=2)#不入库 2，入库
    is_vip = IntField(verbose_name=u'是否是vip',default=3)#  1高级 2 超级 3非会员

    # 个人资料
    nickname = StringField(verbose_name=u"用户昵称", max_length=32)
    desc = StringField(verbose_name=u"自我描述", max_length=280)
    phone = StringField(verbose_name=u"手机号", max_length=15)
    gender = IntField(verbose_name=u"性别", choices=((0, u"未选择"), (1, u"男"), (2, u"女")))
    image = StringField(verbose_name=u"用户图片", max_length=255, default='')
    constellation = StringField(verbose_name=u"星座", max_length=256)
    occupation = StringField(verbose_name=u"职业", max_length=256)
    blood_type = StringField(verbose_name=u"血型", max_length=64)
    birth_date = DateTimeField(verbose_name=u"生日", default=datetime.date(1995, 1, 1))
    emotional = StringField(verbose_name=u"情感状态", max_length=64)

    # 语音信息
    total_time = IntField(verbose_name=u'总时长(秒)')
    total_call_time = IntField(verbose_name=u'拨打总时长(秒)')
    total_income = IntField(verbose_name=u'总收入')
    total_amount = IntField(verbose_name=u'总订单数')
    audio_room_id = StringField(verbose_name=u"语音房间id", max_length=64)
    now_price = IntField(verbose_name=u'当前价格')#语音价格
    listen_url = StringField(verbose_name=u"试听url", max_length=256)
    url_duration = IntField(verbose_name=u"url时长")
    is_video_auth = IntField(verbose_name=u'是否是视频播主')
    # 视频信息
    video_time = IntField(verbose_name=u'视频总时长')
    video_call_time = IntField(verbose_name=u'视频拨打总时长(秒)')
    video_income = IntField(verbose_name=u'视频总收入')
    video_amount = IntField(verbose_name=u'视频总订单数')
    #video_room_id = StringField(verbose_name=u"视频房间id", max_length=64)
    video_price = IntField(verbose_name=u'视频当前价格')

    # 位置信息
    longitude = FloatField(verbose_name=u"经度")
    latitude = FloatField(verbose_name=u"纬度")
    district = StringField(verbose_name=u"区", max_length=64, default='')
    province = StringField(verbose_name=u"省份", max_length=64, default='')
    city = StringField(verbose_name=u"城市", max_length=64, default='')
    country = StringField(verbose_name=u"国家", max_length=64, default='')

    # 初始化信息
    created_at = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())
    cid = StringField(verbose_name=u"client_id(push)", max_length=128, default='')
    osver = StringField(verbose_name=u'设备系统版本号', max_length=10, default='')
    app_name = StringField(verbose_name=u'app name', max_length=20, default='')
    ip = StringField(verbose_name=u"注册ip", max_length=255, default='')
    channel = StringField(verbose_name=u"渠道", max_length=32)
    platform = IntField(verbose_name=u'平台', choices=PLATFORM)
    source = IntField(verbose_name=u'用户来源', choices=SOURCE)

    # 账户信息
    experience = IntField(verbose_name=u'经验值')
    ticket = IntField(verbose_name=u'收益')
    ticket_bonus = IntField(verbose_name=u'对应赠送钱的收益(不参与好友邀请)')
    cost = IntField(verbose_name=u'总消费')
    wealth_value = IntField(verbose_name=u"财富值", default=0)
    charm_value = IntField(verbose_name=u"魅力值", default=0)

    #个人设置
    disturb_mode = IntField(verbose_name=u'免打扰模式开关', choices=NO_DISTURBB_ON)
    bottle_switch = IntField(verbose_name=u'漂流瓶开关', choices=BOTTLE_SWITCH)

    #在线状态字段
    online_status = IntField(verbose_name=u'在线状态', choices=ONLINE_STATUS)
    current_score = FloatField(verbose_name=u'用户在线状态评分')
    #个人封面
    cover = StringField(verbose_name=u"个人封面")

    #上次登录设备
    last_guid = StringField(verbose_name=u"上次登录guid")


    class Meta:
        app_label = "customer"
        verbose_name = u"用户"
        verbose_name_plural = verbose_name

    @property
    def is_blocked(self):
        return self.is_block == 1

    @property
    def user_logo(self):
        return str(self.image) + "/logo56"  # 万象优图样式

    @property
    def user_logo_big(self):
        return str(self.image) + "/logo120"  # 万象优图样式

    @property
    def uuid(self):
        return str(self.identity)

    @property
    def sid(self):
        return str(self.id)

    @property
    def gender_desc(self):
        dic = {0: u"未知", 1: u"男", 2: u"女", }
        return dic.get(self.gender, u"女")

    @property
    def source_zh(self):
        dic = {0: u"自有注册", 1: u"微信", 2: u"微博", 3: u"QQ", 4: u"手机", 5: u"友盟微信"}
        return dic.get(self.source, u"其他")

    def get_normal_dic_info(self):

        if not self.phone:
            phone = ""
        else:
            phone = self.phone[0:3] + "*****" + self.phone[8:11]

        return {
            "_uid": self.sid,
            "uid": self.uuid,
            "is_block": self.is_block,
            "user_type": self.user_type,
            "nickname": self.nickname,
            "desc": self.desc,
            "phone": phone,
            "gender": self.gender_desc,
            "logo": self.user_logo,
            "logo_big": self.image,
            "poster": self.image,
            "district": self.district,
            "province": self.province,
            "city": self.city,
            "country": self.country,
            "constellation": self.constellation,
            "occupation": self.occupation,
            "blood_type": self.blood_type,
            "birth_date": self.birth_date.strftime('%Y-%m-%d'),
            "age": User.get_age(self.birth_date),
            "emotional": self.emotional,
            "created_at": datetime_to_timestamp(self.created_at),
            "total_time": self.total_time,
            "total_call_time": self.total_call_time,
            "total_income": self.total_income,
            "total_amount": self.total_amount,
            "audio_room_id": self.audio_room_id,
            "now_price": self.now_price,
            "listen_url": self.listen_url,
            "is_video_auth": self.is_video_auth,
            "url_duration": self.url_duration,
            "video_time": self.video_time,
            "video_call_time": self.video_call_time,
            "video_income": self.video_income,
            "video_amount": self.video_amount,
            "video_price": self.video_price,
            "experience": self.experience,
            "ticket": self.ticket,
            "ticket_bonus":self.ticket_bonus,
            "cost": self.cost,
            "wealth_value": self.wealth_value,
            "charm_value": self.charm_value,
            "bottle_switch": self.bottle_switch,
            "disturb_mode": self.disturb_mode,
            "current_score": self.current_score,
            "cover": self.cover,
            "is_valid": self.is_valid,
            "is_vip": self.is_vip,

        }

    @classmethod
    def create_user(cls, openid, source, nickname, platform=0, phone=None, gender=1, ip='', image="", channel="", guid=guid):
        from app.customer.models.account import Account
        from app.customer.models.benifit import TicketAccount
        try:
            user = cls.objects.get(source=source, openid=openid)
            if user.complete_info == 1:
                is_new = False
            else:
                is_new = True

        except User.DoesNotExist:
            if image and source != cls.SOURCE_PHONE:
                image = User.convert_http_to_https(cls.upload_logo(image,gender))

            is_new = True

            user = User(
                openid=openid,
                complete_info=0,
                is_block=0,
                user_type=0,
                guid=guid,
                nickname=nickname,
                desc=u"等待一通电话，连接你我的心。",
                phone=phone,
                gender=gender,
                image=User.convert_http_to_https(image),
                constellation=u'摩羯座',
                occupation="",
                blood_type="",
                birth_date=datetime.date(1995, 1, 1),
                emotional="",
                total_time=0,
                total_call_time=0,
                total_income=0,
                total_amount=0,
                audio_room_id="",
                now_price=10,
                listen_url="",
                is_video_auth=3,
                url_duration=0,
                video_time=0,
                video_call_time=0,
                video_income=0,
                video_amount=0,
                video_price=100,
                created_at=datetime.datetime.now(),
                ip=ip,
                channel=channel,
                platform=platform,
                source=source,
                experience=0,
                ticket=0,
                ticket_bonus=0,
                cost=0,
                wealth_value=0,
                charm_value=0,
                bottle_switch=1,
                disturb_mode=0,
                online_status=1,
                current_score=-1,
                last_guid=guid,
                is_vip=3

            )
            user.id = UserRedis.pop_user_id()
            user.identity = UserRedis.pop_user_identity()
            user.save()

            # create account
            account = Account(
                user=user,
                diamond=0,
                last_diamond=0,
                update_time=datetime.datetime.now(),
                diamond_bonus=0,
                charge=0,
            )
            account.save()

            ticket_account = TicketAccount(
                user=user,
                total_ticket=0,
                gift_ticket=0,
                call_ticket=0,
                friend_charge_ticket=0,
                friend_benifit_ticket=0,
                money_requesting=0,
                money=0,
                money_withdrawed=0,
                bonus_ticket=0,
                last_ticket=0,
                update_time=datetime.datetime.now()
            )

            ticket_account.save()

            ###########添加用户时间上报#####################
            user_heart_beat = UserHeartBeat()
            user_heart_beat.user = user
            user_heart_beat.last_report_time = int(time.time())
            user_heart_beat.current_score = user_heart_beat.last_report_time
            user_heart_beat.save()

        except Exception, e:
            logging.error("create user error " + str(e))

        return is_new, user

    @classmethod
    def create_user2(cls, openid, source, nickname, platform=0, phone=None, gender=1, ip='', image="", channel="",
                    guid=guid):
        from app.customer.models.account import Account
        from app.customer.models.benifit import TicketAccount
        try:
            user = cls.objects.get(source=source, openid=openid)
            if user.complete_info == 1:
                is_new = False
            else:
                is_new = True

        except User.DoesNotExist:
            if image and source != cls.SOURCE_PHONE:
                image = User.convert_http_to_https(cls.upload_logo(image,gender))

            if source == cls.SOURCE_PHONE:
                complete_info = 1
            else:
                complete_info = 0

            user = User(
                id=User.objects.all().count() + 1,
                openid=openid,
                complete_info=complete_info,
                is_block=0,
                user_type=0,
                guid=guid,
                nickname=nickname,
                desc=u"等待一通电话，连接你我的心。",
                phone=phone,
                gender=gender,
                image=User.convert_http_to_https(image),
                constellation=u'摩羯座',
                occupation="",
                blood_type="",
                birth_date=datetime.date(1995, 1, 1),
                emotional="",
                total_time=0,
                total_call_time=0,
                total_income=0,
                total_amount=0,
                audio_room_id="",
                now_price=10,
                listen_url="",
                is_video_auth=3,
                url_duration=0,
                video_time=0,
                video_call_time=0,
                video_income=0,
                video_amount=0,
                video_price=100,
                created_at=datetime.datetime.now(),
                ip=ip,
                channel=channel,
                platform=platform,
                source=source,
                experience=0,
                ticket=0,
                ticket_bonus=0,
                cost=0,
                wealth_value=0,
                charm_value=0,
                bottle_switch=1,
                disturb_mode=0,
                online_status=1,
                current_score=-1,
                last_guid=guid
            )

            user_identity = LuckIDInfo.objects.filter(id_assign=0, id_type=0).order_by('id').first()
            user_identity.id_assign = 1
            user_identity.save()
            user.identity = int(user_identity.user_id)
            user.save()

            # create account
            account = Account(
                user=user,
                diamond=0,
                last_diamond=0,
                update_time=datetime.datetime.now(),
                diamond_bonus=0,
                charge=0,
            )
            account.save()

            ticket_account = TicketAccount(
                user=user,
                total_ticket=0,
                gift_ticket=0,
                call_ticket=0,
                friend_charge_ticket=0,
                friend_benifit_ticket=0,
                money_requesting=0,
                money=0,
                money_withdrawed=0,
                bonus_ticket=0,
                last_ticket=0,
                update_time=datetime.datetime.now()
            )

            ticket_account.save()

            ###########添加用户时间上报#####################
            user_heart_beat = UserHeartBeat()
            user_heart_beat.user = user
            user_heart_beat.last_report_time = int(time.time())
            user_heart_beat.current_score = user_heart_beat.last_report_time
            user_heart_beat.save()
            if complete_info == 1:
                is_new = False
            else:
                is_new = True
        except Exception, e:
            logging.error("create user error " + str(e))

        return is_new, user

    @classmethod
    def upload_logo(cls, headimgurl, gender):
        import urllib2

        img = urllib2.urlopen(headimgurl)
        idata = img.read()

        if idata:
            data = UploadImage.push_binary_to_qclude(idata)
            return data.get("data", {}).get('download_url', '')
        else:
            return "https://hdlive-10048692.image.myqcloud.com/head_1497412888" if gender == 1 \
                else "https://hdlive-10048692.image.myqcloud.com/head_1497413140"

    def upload_client_id(self, cid, platform, osver, app_name):
        try:
            self.cid = cid
            self.platform = platform
            self.osver = osver
            self.app_name = app_name
            self.save()
        except Exception, e:
            logging.error("update client_id error:{0}".format(e))

    @classmethod
    def search(cls, keyword, limit=100):
        try:
            _id = int(keyword)
        except Exception:
            return cls.objects.filter(nickname__in=keyword)[0:limit]

        return cls.objects.filter(Q(identity=_id))

    def add_experience(self, _experience):
        now_experience = self.experience + _experience
        self.experience = now_experience
        self.save()

    # 封号
    def be_block(self):
        self.is_block = 1
        self.save()

    # 取消封号
    def cancel_block(self):
        self.is_block = 0
        self.save()

    # 根据生日获得星座
    @classmethod
    def zodiac(cls, birth_date):
        time_array = time.strptime(birth_date, "%Y-%m-%d")
        month = time_array[1]
        day = time_array[2]
        n = (u'摩羯座', u'水瓶座', u'双鱼座', u'白羊座', u'金牛座', u'双子座', u'巨蟹座', u'狮子座', u'处女座', u'天秤座', u'天蝎座', u'射手座')
        d = ((1, 20), (2, 19), (3, 21), (4, 21), (5, 21), (6, 22), (7, 23), (8, 23), (9, 23), (10, 23), (11, 23), (12, 23))
        return str(n[len(filter(lambda y: y <= (month, day), d)) % 12])

    # 根据生日获得年龄
    @classmethod
    def get_age(cls, birth_date):
        today = datetime.date.today()
        if birth_date.month > today.month:
            return today.year - birth_date.year - 1
        elif birth_date.month < today.month:
            return today.year - birth_date.year
        else:
            if birth_date.day > today.day:
                return today.year - birth_date.year - 1
            else:
                return today.year - birth_date.year

    # 转换url为https
    @classmethod
    def convert_http_to_https(cls, url):
        if "https" in url:
            return url
        else:
            return url.replace("http", "https")
            # return url

    @classmethod
    def update_location(cls, user_id, country, province, city, district, longitude, latitude):
        try:
            user = cls.objects.get(id=user_id)
            if user.user_type == 2: # 小号禁止修改
                return False
            user.country = country
            user.province = province
            user.city = city
            user.district = district
            user.longitude = longitude
            user.latitude = latitude
            user.save()
            return True
        except Exception,e:
            logging.error("update location error:{0}".format(e))
            return False

    @classmethod
    def set_disturb_mode(cls, user_id, disturb_mode):
        try:
            user = User.objects.get(id=user_id)
            user.disturb_mode = disturb_mode
            user.save()
            return True
        except Exception, e:
            logging.error("set disturb_mode error{0}".format(e))
            return False

    @classmethod
    def complete_personal_info(cls, user, nickname, gender, img, birth_date):
        if not nickname:
            nickname = user.sid
        if not img:
            if gender == 1:
                img = "https://hdlive-10048692.image.myqcloud.com/head_1497412888"
            else:
                img = "https://hdlive-10048692.image.myqcloud.com/head_1497413107"
        if not birth_date or birth_date == "null":
            birth_date = "1995-01-01"

        try:
            user.nickname = nickname
            user.gender = gender
            user.image = User.convert_http_to_https(img)
            user.birth_date = datetime.datetime.strptime(birth_date, '%Y-%m-%d')
            user.constellation = User.zodiac(birth_date)
            user.complete_info = 1
            user.save()
            return True
        except Exception,e:
            logging.error("complete personal info error:{0}".format(e))
            return False



class ThridPard(Document):
    user_id = IntField(verbose_name=u'用户', primary_key=True)

    weixin_openid = StringField(verbose_name=u"weixin_openid", max_length=128)
    weixin_access_token = StringField(verbose_name=u"weixin_openid", max_length=65535)

    sina_openid = StringField(verbose_name=u"sina_openid", max_length=128)
    sina_access_token = StringField(verbose_name=u"sina_openid", max_length=65535)

    qq_openid = StringField(verbose_name=u"qq_openid", max_length=128)
    qq_access_token = StringField(verbose_name=u"qq_openid", max_length=65535)

    class Meta:
        app_label = "customer"
        verbose_name = u"第三方绑定"
        verbose_name_plural = verbose_name

    @classmethod
    def get_by_user(cls, user_id):
        thrid = cls.objects.filter(user_id=user_id).first()
        if not thrid:
            thrid = ThridPard(user_id=user_id)
            thrid.save()

        return thrid

    def update_weixin_info(self, openid, access_token):
        if not self.weixin_openid:
            self.weixin_openid = openid
            self.weixin_access_token = access_token
            self.save()


"""
号码资源库
"""
class LuckIDInfo(Document):
    NUMBER_TYPE = [
        (0, u'普通'),
        (1, u'特殊'),
        (2, u'靓号'),
    ]
    NUMBERTYPE_NOR = 0  # 普通
    NUMBERTYPE_SPE = 1  # 特殊
    NUMBERTYPE_LUK = 2  # 靓号

    NUMBER_LEVEL = [
        (0, u'无级别'),
        (1, u'一级'),
        (2, u'二级'),
        (3, u'三级'),
        (4, u'四级'),
        (5, u'五级'),
    ]
    NUMBERLEVEL_0 = 0
    NUMBERLEVEL_1 = 1
    NUMBERLEVEL_2 = 2
    NUMBERLEVEL_3 = 3
    NUMBERLEVEL_4 = 4
    NUMBERLEVEL_5 = 5

    NUMBER_ASSIGN = [
        (0, u'为分配'),
        (1, u'已分配'),
    ]
    NUMBER_UNASSIGN = 0
    NUMBER_ASSIGNED = 1

    id = IntField(primary_key=True)
    user_id = StringField(verbose_name=u"用户id", max_length=30)
    id_type = IntField(verbose_name=u"号码类型", choices=NUMBER_TYPE, required=True)
    id_level = IntField(verbose_name=u"号码级别", choices=NUMBER_LEVEL, required=True)
    id_assign = IntField(verbose_name=u"分配情况", choices=NUMBER_ASSIGN, required=True)

    class Meta:
        app_label = "customer"
        managed = False
        verbose_name = u"号码资源库"
        verbose_name_plural = verbose_name

    def normal_info(self):
        return {
            "user_id": self.user_id,
            "id_type": self.id_type,
            "id_level": self.id_level,
            "id_assign": self.id_assign,
        }


class PhonePassword(Document):
    phone = StringField(verbose_name=u"手机号", unique=True, max_length=16)
    password = StringField(verbose_name=u"password", max_length=128)

    class Meta:
        app_label = "customer"
        verbose_name = u"手机号密码"
        verbose_name_plural = verbose_name

    def normal_info(self):
        return {
            "phone": self.phone,
            "password": self.password,
        }

    @classmethod
    def create_phone(cls, phone):
        try:
            user = User.objects.filter(phone=phone)
            if user:
                return False, phone
            else:
                user_phone = PhonePassword.objects.filter(phone=phone)
                if not user_phone.first():
                    phone_pass = PhonePassword(
                        phone=phone,
                    )
                    phone_pass.save()
                return True, phone
        except Exception, e:
            logging.error("create phone error:{0}".format(e))
            return False, 0

    @classmethod
    def update_password(cls, phone, password):
        try:
            phone_pass = PhonePassword.objects.get(phone=phone)
            phone_pass.password = password
            phone_pass.save()
            return True
        except Exception, e:
            logging.error("update password error:{0}".format(e))
            return False

    @classmethod
    def check_phone_password(cls, phone, password):
        try:
            phone_pass = PhonePassword.objects.get(phone=phone)
            if phone_pass.password == password:
                return True, phone
            else:
                return False, phone
        except PhonePassword.DoesNotExist:
            return False, 0

    @classmethod
    def reset_password_check(cls, phone):
        user = User.objects.filter(phone=phone)
        if user:
            return True
        phone_pass = PhonePassword.objects.filter(phone=phone)
        if phone_pass and phone_pass.first().password:
            return True
        else:
            return False

    @classmethod
    def bind_user_check(cls, phone, user_id):
        user = User.objects.filter(phone=phone)
        phone_user = User.objects.get(id=user_id)
        if user:
            return True, None
        if phone_user.phone:
            return True, phone_user.phone
        phone_pass = PhonePassword.objects.filter(phone=phone)
        if phone_pass and phone_pass.first().password:
            return True, None
        else:
            return False, None

    @classmethod
    def bind_user(cls, phone, user_id, password):
        user = User.objects.get(id=user_id)
        phone_password = PhonePassword.objects.filter(phone=phone)
        if not phone_password:
            phone_password = PhonePassword(
                phone=phone,
                password=password,
            )
            phone_password.save()
        else:
            if phone_password.first().password:
                return False
            else:
                phone_password = phone_password.first()
                phone_password.password = password
                phone_password.save()

        user.phone = phone
        user.save()
        return True


class UserDefaultImg(Document):
    picture_url = StringField(verbose_name=u"password", max_length=255)
    gender = IntField(verbose_name=u"性别")
    #todo 先写成常量
    '''
    "https://hdlive-10048692.image.myqcloud.com/activity_1493191693",
    "https://hdlive-10048692.image.myqcloud.com/activity_1493192160",
    "https://hdlive-10048692.image.myqcloud.com/activity_1493192253",
    "https://hdlive-10048692.image.myqcloud.com/activity_1493192294",
    "https://hdlive-10048692.image.myqcloud.com/activity_1493192331",
    "https://hdlive-10048692.image.myqcloud.com/activity_1493192404",
    "https://hdlive-10048692.image.myqcloud.com/activity_1493192428",
    "https://hdlive-10048692.image.myqcloud.com/activity_1493192477",
    "https://hdlive-10048692.image.myqcloud.com/activity_1493192498",
    "https://hdlive-10048692.image.myqcloud.com/activity_1493192518",
    '''
    Picture_info = [
        "https://hdlive-10048692.image.myqcloud.com/head_1497411985",
        "https://hdlive-10048692.image.myqcloud.com/head_1497412054",
        "https://hdlive-10048692.image.myqcloud.com/head_1497412888",
        "https://hdlive-10048692.image.myqcloud.com/head_1497412931",
        "https://hdlive-10048692.image.myqcloud.com/head_1497412994",
        "https://hdlive-10048692.image.myqcloud.com/head_1497413045",
        "https://hdlive-10048692.image.myqcloud.com/head_1497413074",
        "https://hdlive-10048692.image.myqcloud.com/head_1497413107",
        "https://hdlive-10048692.image.myqcloud.com/head_1497413140",
        "https://hdlive-10048692.image.myqcloud.com/head_1497413150"
    ]
    User_gender=[1, 1, 1, 1, 1, 2, 2, 2, 2, 2]
    class Meta:
        app_label = "customer"
        verbose_name = u"用户默认头像"
        verbose_name_plural = verbose_name

    def normal_info(self):
        return {
            "picture_url": self.picture_url,
            "gender": self.gender,
        }

    @classmethod
    def create_default_img(cls, picture_url, gender):
        try:
            picture = UserDefaultImg(
                picture_url=picture_url,
                gender=gender,
            )
            picture.save()
            return True
        except Exception,e:
            logging.error("create default img error:{0}".format(e))
            return False

    @classmethod
    def get_all_defaults_img(cls):
        # todo 先本地写死 之后改为数据库
        """
        pictures = UserDefaultImg.objects.all()
        return pictures
        """
        pictures =[]
        for i in range(0,len(cls.Picture_info)):
            picture = UserDefaultImg()
            picture.picture_url = cls.Picture_info[i]
            picture.gender = cls.User_gender[i]
            pictures.append(picture)
        return pictures


class UserInviteCode(Document):
    user_id = IntField(verbose_name=u"用户id")
    invite_id = IntField(verbose_name=u"邀请人id")
    invite_date = DateTimeField(verbose_name=u"邀请时间", default=datetime.datetime.now())
    user_guid = StringField(verbose_name=u'用户设备号')

    class Meta:
        app_label = "customer"
        verbose_name = u"用户邀请"
        verbose_name_plural = verbose_name

    @classmethod
    def create_invite_code(cls, user_id, invite_id,user_guid):
        try:
            invite = UserInviteCode(user_id=user_id, invite_id=invite_id, invite_date=datetime.datetime.now(),
                                    user_guid=user_guid)
            invite.save()
            return True
        except Exception,e:
            logging.error("create invite code error:{0}".format(e))
            return False

    @classmethod
    def invite_code_check(cls, user_id, invite_code, user_guid):
        try:
            invite_user = User.objects.filter(identity=int(invite_code)).first()
            if not invite_user:
                return 0, 10001  # 没有该用户
            else:
                if invite_user.id == int(user_id):
                    return 0, 10002  # 不能邀请自己
                elif invite_user.guid == user_guid:
                    return 0, 10003  # 同一设备不能邀请自己
                else:
                    guid = UserInviteCode.objects.filter(user_guid=user_guid)
                    if not guid:
                        return invite_user.id, 0  # 成功
                    else:
                        return 0, 10004   # 同一设备只能邀请一次
        except Exception, e:
            logging.error("invite code check error:{0}".format(e))
            return 0, 10001

    @classmethod
    def get_invite_list(cls, invite_id):
        try:
            invite_list = []
            invites = UserInviteCode.objects.filter(invite_id=invite_id).order_by("-invite_date")
            for invite in invites:
                user = User.objects.get(id=invite.user_id)
                if user.is_block == 0:
                    invite_list.append(user)
            return invite_list
        except Exception,e:
            logging.error("get friends revenue error:{0}".format(e))
            return []


class RealNameVerify(Document):

    VERIFY_STATUS = [
        (0, u"审核中"),
        (1, u"通过"),
        (2, u"未通过"),
    ]

    user_id = IntField(verbose_name=u"用户id")
    real_name = StringField(verbose_name=u"真实姓名", max_length=32)
    identity_code = StringField(verbose_name=u"身份证号", max_length=32)
    picture_one = StringField(verbose_name=u"身份证正面照片", max_length=256)
    picture_two = StringField(verbose_name=u"身份证背面照片", max_length=256)
    picture_three = StringField(verbose_name=u"手持身份证照片", max_length=256)
    verify_time = DateTimeField(verbose_name=u"上传时间", default=datetime.datetime.now())
    feedback_reason = StringField(verbose_name=u"审核反馈", max_length=256)
    status = IntField(verbose_name=u"审核状态", choices=VERIFY_STATUS)

    class Meta:
        app_label = "customer"
        verbose_name = u"实名认证"
        verbose_name_plural = verbose_name

    @classmethod
    def create_real_name_verify(cls, user_id, real_name, identity_code, picture_one, picture_two, picture_three):
        try:
            verify = RealNameVerify(
                user_id=user_id,
                real_name=real_name,
                identity_code=identity_code,
                picture_one=picture_one,
                picture_two=picture_two,
                picture_three=picture_three,
                verify_time=datetime.datetime.now(),
                status=0,
            )
            verify.save()
            desc = u"<html><p>亲爱的播主您好，认证申请已成功提交，请等待工作人员审核（1-2工作日）</p></html>"
            MessageSender.send_system_message(str(user_id), desc)
            return True
        except Exception,e:
            logging.error("create real name verify error:{0}".format(e))
            return False

    @classmethod
    def check_user_verify(cls, user_id):
        verify = cls.objects(user_id=user_id, status__lt=2).order_by("-verify_time").first()
        if verify:
            return verify.status
        else:
            return 3


class VideoManagerVerify(Document):

    VERIFY_STATUS = [
        (0, u"认证中"),
        (1, u"认证通过"),
        (2, u"认证未通过"),
    ]

    user_id = IntField(verbose_name=u"用户id")
    avtar_auth = StringField(verbose_name=u"头像认证照片", max_length=256)
    active_auth = StringField(verbose_name=u"动作认证照片", max_length=256)
    create_time = DateTimeField(verbose_name=u"上传时间", default=datetime.datetime.now())
    verify_time = DateTimeField(verbose_name=u"确认时间", default=datetime.datetime.now())
    feedback_reason = StringField(verbose_name=u"认证审核反馈", max_length=256)
    status = IntField(verbose_name=u"认证状态", choices=VERIFY_STATUS)

    class Meta:
        app_label = "customer"
        verbose_name = u"视频播主认证"
        verbose_name_plural = verbose_name


    @classmethod
    def create_video_manager_verify(cls, user_id, avtar_auth, active_auth,
                                    feedback_reason="", status=0):
        try:
            verify = VideoManagerVerify(
                user_id=user_id,
                avtar_auth=avtar_auth,
                active_auth=active_auth,
                feedback_reason=feedback_reason,
                create_time=datetime.datetime.now(),
                status=status,
            )
            verify.save()
            user = User.objects.get(id=int(user_id))
            user.is_video_auth = 0
            user.save()
            desc = u"<html><p>亲爱的用户您好，认证申请已成功提交，请等待工作人员审核（1-2工作日）</p></html>"
            MessageSender.send_system_message(user.sid, desc)
            return True
        except Exception, e:
            logging.error("create real videoManager verify error:{0}".format(e))
            return False


    @classmethod
    def check_video_manager_verify(cls, user_id):
        verify = cls.objects(user_id=user_id, status__lt=2).order_by("-create_time, -verify_time").first()
        if verify:
            return verify.status
        else:
            return 3


class UserHeartBeat(Document):
    REPORT_INTERVAL = 60
    PLATFORM = [
        (0, u'Android'),
        (1, u'IOS'),
        (2, u'其他')
    ]

    user = GenericReferenceField("User", verbose_name=u"用户id", primary_key=True)
    last_report_time = IntField(verbose_name=u"心跳最后上报时间")
    app_name = StringField(verbose_name=u"app名称")
    app_version = StringField(verbose_name=u"app版本号")
    platform = IntField(verbose_name=u"平台", choices=PLATFORM)


    @classmethod
    def get_bottle_users_count(self):
        import time
        time = int(time.time())
        three_days_ago = time - 1 * 24 * 60 * 60
        return UserHeartBeat.objects(last_report_time__gt=three_days_ago).count()


class RegisterInfo():
    ADJECTIVE = [
        "傲慢", "倔强", "漫不经心", "脆弱", "急躁", "缺乏安全感", "乐观", "爽朗", "豪放", "勇敢", "表情丰富",
        "兴奋", "精力充沛", "强烈", "乐观", "率直", "冲动",  "暴躁", "倔强", "内向", "沉静", "谨慎", "稳重",
        "语言动作迟缓", "不易暴露", "善良", "友爱", "好心肠", "善交际", "开朗", "活泼", "风趣", "易激动",
        "安静", "寡言", "抑郁", "脆弱", "安静", "谨慎", "一本正经", "不懂幽默","唠叨", "逆反", "怨恨", "保守",
        "健忘", "直率", "挑剔", "胆小", "好插嘴", "躁急", "内向",  "顽固", "大嗓门", "孤僻", "懒惰", "烦躁",
        "善变", "狡猾", "浪漫", "有趣", "快乐", "灵巧", "沉着", "热情"
    ]

    NOUN = [
        "马铃薯", "红萝卜", "洋葱", "茄子芹菜", "包心菜", "紫菜", "黄瓜蕃茄", "红萝卜", "白萝卜西洋菜", "玉米",
        "白花菜," "葱", "大蒜", "姜", "白菜芥菜", "青椒", "红椒黄椒","洋菇", "绿花菜", "南瓜", "香菜", "四季豆",
        "长形平豆", "莴苣菜," "芜菁", "秋葵", "芋头", "蕃薯", "菠菜", "绿豆芽", "胡椒甜椒", "柿子椒", "番茄",
        "西红柿", "芦笋", "黄瓜", "茄子", "鲍鱼菇", "金针菇", "木耳菜豆", "甜菜", "马铃薯","苹果", "梨", "杏",
        "桃", "葡萄", "香蕉", "菠萝", "李子", "西瓜", "橙", "柠檬", "芒果", "草莓", "枇杷", "桑椹", "油桃", "樱桃",
        "石榴", "柑子", "柿子", "胡桃", "榛子", "枣", "粟", "子醋粟", "黑莓", "鳄梨", "红醋栗", "红橙", "香橼",
        "大马士革李", "番木瓜", "覆盆子", "荔枝", "弥猴桃", "小熊猫", "疣猪", "羚羊", "驯鹿", "考拉", "犀牛" "猞猁",
        "穿山甲", "长颈鹿", "熊猫", "食蚁兽", "猩猩", "海牛", "水獭", "灵猫", "海豚", "海象", "鸭嘴兽", "刺猬",
        "北极狐", "无尾熊", "北极熊", "袋鼠", "犰狳", "河马", "海豹", "鲸鱼"
    ]

    @classmethod
    def make_nickname(cls):
        return cls.ADJECTIVE[random.randint(0, len(cls.ADJECTIVE)-1)] + u"的" +cls.NOUN[random.randint(0, len(cls.NOUN)-1)]




class UserAppealRecord(Document):
    user = GenericReferenceField("User", verbose_name=u"用户")
    reason = StringField(verbose_name=u"申诉理由")
    phone = StringField(verbose_name=u"手机号码")
    create_time = DateTimeField(verbose_name=u"申诉时间")

    feedback = StringField(verbose_name=u"运营反馈")
    feedback_time = DateTimeField(verbose_name=u"运营")
    
    @classmethod
    def create_user_appeal_record(cls, user, reason, phone):
        _obj = cls()
        _obj.user = user
        _obj.reason = reason
        _obj.phone = phone
        _obj.create_time = datetime.datetime.now()
        _obj.save()















