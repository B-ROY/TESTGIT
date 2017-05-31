# coding=utf-8

import datetime

# now = datetime.datetime.now()
# date = now.strftime('%Y年%m月%d日')
# print date


dic1 = {
    "master_key": "2",
    "bottle": "2",
    "clairvoyant": "5"
}

# s = str(dic1)
# d1 = eval(s)
# print d1.get("bottle")
# print s

# now = datetime.datetime.now()
# end_time = now + datetime.timedelta(days=30)
# print end_time

# TOOLS_TYPE = (
#     (0, u'万能钥匙'),
#     (1, u'漂流瓶'),
#     (2, u'千里眼'),
# )
# print TOOLS_TYPE[2][0]

now = datetime.datetime.now()
yesterday = now - datetime.timedelta(days=1)
yesterday_start = yesterday.strftime("%Y-%m-%d 00:00:00")
yesterday_end = yesterday.strftime("%Y-%m-%d 23:59:59")

print yesterday_start
print yesterday_end
