#coding=utf-8


PLATFORM_ANDROID = 1
PLATFORM_IOS = 2
PLATFORM_WP = 3
PLATFORM_OTHER = 4

class FilterItem(object):
    KEYS = ()
    # KEYS = (
    #     {'id': 2, 'name': 'slider', 'desc': u'轮播图视频'},
    # )
    @classmethod
    def all(cls):
        return cls.KEYS

    @classmethod
    def to_s(cls, type_id):
        _id = int(type_id) if type_id else 0
        d_type = cls.id_to_dict(_id)
        if d_type:
            return d_type['name']
        else:
            return ''

    @classmethod
    def to_i(cls, type_name):
        d_type = cls.name_to_dict(type_name)
        if d_type:
            return d_type['id']
        else:
            return 0

    @classmethod
    def to_zh(cls, type_id):
        _id = int(type_id) if type_id else 0
        d_type = cls.id_to_dict(_id)
        if d_type:
            return d_type['desc']
        else:
            return ''

    @classmethod
    def name_to_dict(cls, type_name):
        d_type = {}
        for item in cls.KEYS:
            if type_name == item['name']:
                d_type = item
                break
        return d_type

    @classmethod
    def id_to_dict(cls, type_id):
        d_type = {}
        for item in cls.KEYS:
            if type_id == item['id']:
                d_type = item
                break
        return d_type

class UserSource(FilterItem):
    KEYS = [
        {'id': 0, 'name': 'self', 'desc': u'自有注册'},
        {'id': 1, 'name': 'wx', 'desc': u'微信'},
        {'id': 2, 'name': 'blog', 'desc': u'微博'},
        {'id': 3, 'name': 'qq', 'desc': u'QQ'},
        {'id': 4, 'name': 'phone', 'desc': u'手机'},
    ]


class OrderKey(FilterItem):
    KEYS = [
        {'id': 0, 'name': 'created_at', 'desc': u'注册时间'},
        {'id': 1, 'name': 'contribute_experience', 'desc': u'贡献'},
        {'id': 2, 'name': 'experience', 'desc': u'热度'},
    ]

class FillType(FilterItem):
    KEYS = [
        {'id': 0, 'name': 'ali', 'desc': u'支付宝'},
        {'id': 1, 'name': 'we_chat', 'desc': u'微信'},
        {'id': 2, 'name': 'apple_pay', 'desc': u'苹果'},
        {'id': 3, 'name': 'we_chat_jsapi', 'desc': u'微信JSAPI'},
        {'id': 4, 'name': 'union_pay', 'desc': u'银联'},
        {'id': 5, 'name': 'other', 'desc': u'其他'},
        {'id': 6, 'name': 'backend_add', 'desc': u'后台添加'},
    ]

class WithdrawFillType(FilterItem):
    KEYS = [
        {'id': 0, 'name': 'ali', 'desc': u'支付宝'},
        {'id': 1, 'name': 'we_chat', 'desc': u'微信'},
        {'id': 2, 'name': 'apple_pay', 'desc': u'苹果'},
        {'id': 3, 'name': 'we_chat_jsapi', 'desc': u'微信JSAPI'},
        {'id': 4, 'name': 'union_pay', 'desc': u'银联'},
        {'id': 5, 'name': 'other', 'desc': u'其他'},
        {'id': 6, 'name': 'backend_add', 'desc': u'后台添加'},
    ]