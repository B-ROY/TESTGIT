# coding=utf-8


from app.customer.models.tools import *


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


# 会员
class Vip(Document):

    VIP_TYPE = (
        (1, u"高级会员"),
        (2, u"超级会员"),
    )

    STATUS = (
        (0, u"关闭"),
        (1, u"开启"),
    )


    name = StringField(max_length=64, verbose_name=u"会员名称")
    icon_url = StringField(max_length=256, verbose_name=u'icon图片')
    vip_type = IntField(verbose_name=u"会员等级")
    days = IntField(verbose_name=u"会员天数")
    vip_flag = IntField(verbose_name=u"尊贵标识", choices=STATUS, default=1)
    tools_data = StringField(max_length=512, verbose_name=u"道具增值服务,字典 字符串 格式")
    pic_chat = IntField(verbose_name=u"聊天图片功能", choices=STATUS, default=1)
    video_chat = IntField(verbose_name=u"聊天视频功能", choices=STATUS, default=1)
    price = IntField(verbose_name=u"会员价格(分)")
    original_price = IntField(verbose_name=u"原价 会员价格(分)")
    worth = IntField(verbose_name=u"价值(分)")
    is_valid = IntField(verbose_name=u"是否有效")  # 0:删除   1:未删除

    def normal_info(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "icon_url": Vip.convert_http_to_https(self.icon_url),
            "vip_type": self.vip_type,
            "vip_flag": self.vip_flag,
            "tools_data": self.tools_data,
            "pic_chat": self.pic_chat,
            "video_chat": self.video_chat,
            "price": self.price,
            "worth": self.worth,
            "original_price": self.original_price,
        }

    @classmethod
    def convert_http_to_https(cls, url):
        if "https" in url:
            return url
        else:
            return url.replace("http", "https")


class UserVip(Document):

    user_id = IntField(verbose_name=u'用户id', required=True)
    vip_id = StringField(verbose_name=u"会员id", required=True)
    create_time = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())
    end_time = DateTimeField(verbose_name=u"会员截止时间")


    # 用户购买会员
    @classmethod
    def buy_vip(cls, user_id, vip_id):
        user = User.objects.filter(id=user_id).first()
        account = Account.objects.filter(user=user).first()
        vip = Vip.objects.filter(id=vip_id).first()
        status = 200
        message = "success"

        if not vip:
            status = -1
            message = "此会员等级不存在"
            return status, message

        if account.diamond < vip.price:
            status = -1
            message = "您的账户余额不足"
            return status, message

        try:
            # 用户账号余额
            account.diamond_trade_out(price=vip.price, desc=u"购买会员, 会员id=%s" %
                                                            (str(vip.id)), trade_type=TradeDiamondRecord.TradeTypeVIP)

            # 用户会员
            user_vip = UserVip.objects.filter(user_id=user_id).first()
            now = datetime.datetime.now()
            if user_vip:
                user_vip.vip_id = vip_id
            else:
                user_vip = UserVip()
                user_vip.user_id = user_id
                user_vip.vip_id = vip_id

            user_vip.create_time = now
            if now.month == 6:
                end_time = now + datetime.timedelta(days=61)
            else:
                end_time = now + datetime.timedelta(days=31)
            user_vip.end_time = end_time
            user_vip.save()

            # 更新user表
            user.is_vip = vip.vip_type
            user.save()


            # 购买会员记录
            vip_record = UserVipRecord()
            vip_record.user_id = user_id
            vip_record.vip_id = vip_id
            vip_record.create_time = now
            vip_record.save()

            # 添加道具, 道具记录
            tool_str = vip.tools_data
            tool_dic = eval(tool_str)
            for key, value in tool_dic.items():
                tools = Tools.objects.filter(tools_type=int(key)).first()  # 道具
                # 限时的 (累加  当然每天会被清掉,每天是可以累加的)
                user_tools = UserTools.objects.filter(user_id=user_id, time_type=0, get_type=1, tools_id=str(tools.id)).first()
                record_time_type = 0
                if user_tools:
                    user_tools.tools_count += int(value)
                    user_tools.save()
                else:
                    user_tools = UserTools()
                    user_tools.user_id = user_id
                    user_tools.tools_id = str(tools.id)
                    user_tools.tools_count = int(value)
                    user_tools.time_type = 0  # 限时
                    user_tools.get_type = 1  # 会员自动发放
                    invalid_time = now + datetime.timedelta(days=1)
                    user_tools.invalid_time = invalid_time
                    user_tools.save()

                tools_record = UserToolsRecord()
                tools_record.user_id = user_id
                tools_record.tools_id = str(tools.id)
                tools_record.tools_count = int(value)
                tools_record.time_type = record_time_type
                tools_record.oper_type = 3
                tools_record.create_time = now
                tools_record.save()

            return status, message
        except Exception,e:
            status = -1
            message = e.message
            print "error:", e.message
            return status, message

class UserVipRecord(Document):
    user_id = IntField(verbose_name=u'用户id', required=True)
    vip_id = StringField(verbose_name=u"会员id", required=True)
    create_time = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())
    opttype = IntField(verbose_name=u'添加方式')#1:后台添加


class VipIntroPic(Document):
    PIC_STATUS = (
        (0, u"不可用"),
        (1, u"可用"),
    )

    pic_url = StringField(max_length=512, verbose_name=u"会员等级介绍图")
    pic_status = IntField(verbose_name=u"是否可用", choices=PIC_STATUS)
    name = StringField(verbose_name=u"说明")

    @classmethod
    def convert_http_to_https(cls, url):
        if "https" in url:
            return url
        else:
            return url.replace("http", "https")

class VipAdv(Document):

    ADV_STATUS = (
        (0, u"不可用"),
        (1, u"可用"),
    )

    name = StringField(max_length=64, verbose_name=u"vip 广告 名称")
    img_url = StringField(max_length=512, verbose_name=u"vip adv　图片地址")
    adv_status = IntField(verbose_name=u"是否可用", choices=ADV_STATUS)

    @classmethod
    def convert_http_to_https(cls, url):
        if "https" in url:
            return url
        else:
            return url.replace("http", "https")






