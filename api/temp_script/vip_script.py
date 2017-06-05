# coding=utf-8
from app.customer.models.vip import *

def init_vip():

    vip = Vip()
    dic1 = {
        "master_key": "2",
        "bottle": "2",
        "clairvoyant": "5"
    }
    vip.name = u"高级会员"
    vip.icon_url = ""
    vip.vip_type = 1
    vip.days = 30
    vip.vip_flag = 1
    vip.tools_data = str(dic1)
    vip.pic_chat = 1
    vip.video_chat = 1
    vip.price = 3800
    vip.worth = 80000
    vip.save()

    vip2 = Vip()
    dic2 = {
        "master_key": "5",
        "bottle": "5",
        "clairvoyant": "15"
    }
    vip2.name = u"超级会员"
    vip2.icon_url = ""
    vip2.vip_type = 1
    vip2.days = 30
    vip2.vip_flag = 1
    vip2.tools_data = str(dic2)
    vip2.pic_chat = 1
    vip2.video_chat = 1
    vip2.price = 12800
    vip2.worth = 170000
    vip2.save()


def init_user_vip():
    user_vip = UserVip()
    user_vip.user_id = 3
    user_vip.vip_id = "5928e5ee2040e4079fff2322"
    now = datetime.datetime.now()
    end_time = now + datetime.timedelta(days=31)
    user_vip.end_time = end_time
    user_vip.save()


def init_vip_intro_pic():
    vip_pic = VipIntroPic()
    vip_pic.pic_url = "http://heydopic-10048692.image.myqcloud.com/1495853739_c2fbe949f7043cc9e2a5355eb407c5fd"
    vip_pic.pic_status = 1
    vip_pic.name = "会员等级说明"
    vip_pic.save()

def add_vip_adv():
    adv = VipAdv()
    adv.img_url = "http://heydopic-10048692.image.myqcloud.com/1496403505_805a3c7cf6a4787978e80f60928c0596"
    adv.name = "办理vip,无限量加好友"
    adv.adv_status = 1
    adv.save()

