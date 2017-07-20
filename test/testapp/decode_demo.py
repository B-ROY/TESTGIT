# coding=utf-8
from urllib import urlencode
import sys
# defaultencoding = 'utf-8'
# if sys.getdefaultencoding() != defaultencoding:
#     reload(sys)
#     sys.setdefaultencoding(defaultencoding)

adv_info = "http://www.qqhqf.cn/vip_activity/"
data ={
    "lp_share_img" :"https://heydopic-10048692.image.myqcloud.com/1497603976_c1632889d74fe72d6909002b2d32ef42",
    "lp_share_title" : "会员荣耀上线 优惠狂欢6月",
    "lp_share_desc" : "会员充一送一 还有惊喜红包等你拿"
}


str2 = urlencode(data)

print adv_info + "?" + str2