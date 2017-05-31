#coding=utf-8
from api.document.doc_tools import *
from api.view.base import BaseHandler
import time
from api.view.base import *
from app.customer.models.vip import *
from api.convert.convert_user import *
from app.customer.models.account import *


@handler_define
class MyVip(BaseHandler):
    @api_define("my vip info", r'/vip/my_vip', [], description="我的会员信息")

    # 需要返回 会员, 是否可以再次购买, user,  截止时间, vip等级说明图url, 会员价格38, 128

    @login_required
    def get(self):
        user_id = int(self.current_user_id)
        user = self.current_user

        # 测试
        # user_id = 3
        # user = User.objects.filter(id=user_id).first()

        vip_user = UserVip.objects.filter(user_id=user_id).first()
        vip_type = 0  # 0:非会员 1:高级会员  2: 超级会员
        allow_buy = 1  # 0: 不允许购买  1:允许
        endtime_str = ""  # 会员会显示截止日期
        vip_pic = VipIntroPic.objects.filter(pic_status=1).first()  # vip会员介绍说明图
        vips = Vip.objects.all().order_by("vip_type")
        vip_list = []  # 会员列表
        vip_name = ""  # 会员名称
        vip_icon = ""  # 会员icon
        for v in vips:
            vip_list.append(convert_vip(v))


        now = datetime.datetime.now()

        if vip_user:
            end = vip_user.end_time
            days = (end - now).days
            # 截止时间
            endtime_str = end.strftime('%Y年%m月%d日')
            vip = Vip.objects.filter(id=vip_user.vip_id).first()
            vip_type = vip.vip_type
            if days > 3:
                allow_buy = 0
            vip_name = vip.name
            vip_icon = Vip.convert_http_to_https(vip.icon_url)

        data = {
            'vip_type': vip_type,
            'allow_buy': allow_buy,
            'user': convert_user(user),
            'endtime': endtime_str,
            'vip_name': vip_name,
            'vip_icon': vip_icon,
            'vip_list': vip_list,
            'vip_detail_pic': VipIntroPic.convert_http_to_https(vip_pic.pic_url) ,  #  注意HTTPS!!!! 记得convert!
        }
        self.write({"status": "success", "data": data})


@handler_define
class Buy_Vip(BaseHandler):
    @api_define("buy vip", r'/vip/buy_vip', [
        Param("vip_id", True, str, "", "", u"vip_id"),
    ], description="购买会员")

    # 服务端 判断余额   购买  购买记录  减钱  添加道具 道具记录

    @login_required
    def get(self):
        user_id = int(self.current_user_id)
        user = self.current_user


        vip_id = self.arg("vip_id", "")
        if vip_id == "":
            self.write({"status": "failed", "error_message": "请选择会员种类", })

        status, message = UserVip.buy_vip(user_id, vip_id)

        if status == 200:
            # ========= 新的用户和用户会员信息
            vip_user = UserVip.objects.filter(user_id=user_id).first()
            vip_type = 0  # 0:非会员 1:高级会员  2: 超级会员
            allow_buy = 1  # 0: 不允许购买  1:允许
            endtime_str = ""  # 会员会显示截止日期
            vip_name = ""  # 会员名称
            vip_icon = ""  # 会员icon
            now = datetime.datetime.now()
            vip_pic = VipIntroPic.objects.filter(pic_status=1).first()  # vip会员介绍说明图

            if vip_user:
                end = vip_user.end_time
                days = (end - now).days
                # 截止时间
                endtime_str = end.strftime('%Y年%m月%d日')
                vip = Vip.objects.filter(id=vip_user.vip_id).first()
                vip_type = vip.vip_type
                if days > 3:
                    allow_buy = 0
                vip_name = vip.name
                vip_icon = Vip.convert_http_to_https(vip.icon_url)

            data = {
                'vip_type': vip_type,
                'allow_buy': allow_buy,
                'endtime': endtime_str,
                'vip_name': vip_name,
                'vip_icon': vip_icon,
                'vip_detail_pic': VipIntroPic.convert_http_to_https(vip_pic.pic_url)
            }
            self.write({"status": "success", "data": data})
        else:
            self.write({"status": "failed", "error_message": message})
