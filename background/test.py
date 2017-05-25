# -*- coding: utf-8 -*-

__author__ = 'zen'
import urllib
import urllib2


def test_l1():
    params = {
        "game_id": 2,
        "appname": u'滑雪大冒险2'.encode("utf-8"),
        "source": "http://test.gamex.mobile.xxx.com/apkdowload/1450098745_XXXXX2_XXXXX2_(XX-none)XXXX_[XX][XX][XX][XX]_XXXXXXX334XXXXXX_XX_Android_480_800(854)XX_XXX(1.0.1)_XXXX.apk",
        "file_name": "1450098745_XXXXX2_XXXXX2_(XX-none)XXXX_[XX][XX][XX][XX]_XXXXXXX334XXXXXX_XX_Android_480_800(854)XX_XXX(1.0.1)_XXXX.apk",
        "size": 121212,
        "md5": '18b7238d9f8f5788014edcde92e46b35'
    }
    path = 'http://localhost:10000/l1/recieve/notice'
    data = urllib.urlencode(params)
    request = urllib2.Request(path, data=data)
    response = urllib2.urlopen(request, timeout=1).read()
    return data

if __name__ == "__main__":
    test_l1()
