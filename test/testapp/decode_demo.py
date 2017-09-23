# coding=utf-8
from urllib import urlencode
import sys
# defaultencoding = 'utf-8'
# if sys.getdefaultencoding() != defaultencoding:
#     reload(sys)
#     sys.setdefaultencoding(defaultencoding)

# adv_info = "http://www.qqhqf.cn/vip_activity/"
# data ={
#     "lp_share_img" :"https://heydopic-10048692.image.myqcloud.com/1497603976_c1632889d74fe72d6909002b2d32ef42",
#     "lp_share_title" : "会员荣耀上线 优惠狂欢6月",
#     "lp_share_desc" : "会员充一送一 还有惊喜红包等你拿"
# }
#
#
# str2 = urlencode(data)
#
# print adv_info + "?" + str2


# alist = []
#
# dic1 = {
#     "id": "aaa",
#     "count": 1
# }
#
# dic2 = {
#     "id": "bbb",
#     "count": 2
# }
#
# alist.append(dic1)
# alist.append(dic2)
#
# for a in alist:
#     if a["id"] == "aaa":
#         print "yes"
#         a["count"] = 5
#
# print alist

import datetime
import time

# now = datetime.datetime.now()
# # 转换成时间戳
# temp_time = now.strftime("%Y-%m-%d %H:%M:%S")
# timeArray = time.strptime(temp_time, "%Y-%m-%d %H:%M:%S")
# timestamp = time.mktime(timeArray)
# print int(timestamp)
#
#
# d = datetime.datetime.fromtimestamp(timestamp)
# print d


class WeightRandom:

    def __init__(self, items):
        weights = [w for _, w in items]
        self.goods = [x for x, _ in items]
        self.total = sum(weights)
        self.acc = list(self.accumulate(weights))

    def accumulate(self, weights):  # 累和.如accumulate([10,40,50])->[10,50,100]
        cur = 0
        for w in weights:
            cur = cur+w
            yield cur

    def __call__(self):
        import bisect
        import random
        print self.acc
        return self.goods[bisect.bisect_right(self.acc, random.uniform(0, self.total))]


# from app.customer.models.game import TurnTable

# wr = WeightRandom([('1钻石', 200), ('9钻石', 50), ('99金币', 10), ('很遗憾', 200), ('很遗憾', 32),
#                    ('937金币', 200), ('1753金币', 80), ('37846金币', 10), ('门禁卡', 50), ('漂流瓶', 20),
#                    ('千里眼', 20), ('一天VIP', 1), ('观影券', 2), ('1观影碎片', 100), ('2观影碎片', 20),
#                    ('4观影碎片', 5),
#                    ])

# wr = WeightRandom([(1, 200), (2, 50), (3, 10), (4, 200), (5, 32),
#                    (6, 200), (7, 80), (8, 10), (9, 50), (10, 20),
#                    (11, 20), (12, 1), (13, 2), (14, 100), (15, 20),
#                    (16, 5)
#                    ])
# def test():
#     tables = TurnTable.objects.all()
#     obj_list = []
#     for table in tables:
#         data = (table.id, table.num)
#         obj_list.append(data)
#
#     wr = WeightRandom(obj_list)
#
#     print wr()

m, s = divmod(3700, 60)
h, m = divmod(m, 60)
print ("%02d:%02d:%02d" % (h, m, s))
