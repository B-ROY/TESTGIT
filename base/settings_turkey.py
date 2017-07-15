#coding=utf-8
import sys
import os.path

reload(sys)
sys.setdefaultencoding('utf-8')

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "site-packages"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "..", ".."))

from django.core.management import execute_from_command_line
from django.conf import settings as django_settings
from django.utils import importlib


class CHATPAMONGO():
    db = "mini_version"
    host = "172.31.7.150"
    port = 27017
    username = "mini_admin"
    password = "jop*(Oh(&799783"


# class CHATPALOGSMONGO():
#     db = "mini_version"
#     host = "10.141.15.92"
#     port = 27017
#     username = "mini_admin"
#     password = "bw890905"

def execute(*modules):
    load_django_settings(*modules)
    execute_from_command_line()


def load_django_settings(*modules):
    settings = {'MODULES': modules}
    kwargs = {}
    mods = []

    for module in modules:
        try:
            mods.append(importlib.import_module('%s.settings' % module))
        except ImportError, err:
            raise ImportError("Could not import settings '%s' (Is it on sys.path?): %s" % (module, err))

    for module in modules:
        try:
            mods.append(importlib.import_module('%s.my_settings' % module))
        except ImportError:
            pass

    for mod in mods:
        if hasattr(mod, 'inti_params'):
            kwargs.update(getattr(mod, 'inti_params')())

    for mod in mods:
        if hasattr(mod, 'load_settings'):
            getattr(mod, 'load_settings')(settings, **kwargs)

    for mod in mods:
        if hasattr(mod, 'check_settings'):
            getattr(mod, 'check_settings')(settings)

    django_settings.configure(**settings)


def load_settings(settings, debug=False, **kwargs):
    ugettext = lambda s: s
    settings.update({

#        "QCLOUD_LIVE_SDK_APP_ID": "1400011479" , #黑洞互动直播测试key，后面可以进行替换
        "QCLOUD_LIVE_SDK_APP_ID": "1400035387",  # 聊啪APPID
        "QCLOUD_LIVE_SDK_APP_SECRECTs": "e6683b957f7a448c" ,
        'SPHINXES': {
            "host": 'localhost', #连接mogodb，进行用户快速搜索，但目前没有写完业务逻辑
            "port": 9312,
            "maxmatches":200
        },
        'redis_settings': {
            "MQUEUE_BACKEND": {
                "servers": '172.31.7.150',
                "port": 6379,
                "db": 0,
                "password": "@JIcjec0(H780&NIP",
            },
        },

        'DEBUG': False,
        'TEMPLATE_DEBUG': False,
    
        'ALLOWED_HOSTS': ['*','182.254.138.87','localhost'],
        #TODO:这里需要把微信等域名加入进来
        #'ALLOWED_HOSTS':[
        #    '*.heydo.tv',
        #    'api.mobile.heydo.tv',
        #    'cms.mobile.heydo.tv',
        #    'stat.mobile.heydo.tv',
        #    'api.mch.weixin.qq.com',
        #    'api.weixin.qq.com',
        #    '182.254.138.87',
        #    '10.141.15.84',
        #    '10.141.20.129',
        #    '10.141.22.154',
        #    '10.141.108.216',
        #    '10.66.109.88',
        #    '10.66.109.98',
        #    '10.66.150.243',
        #    '123.206.1.186',
        #    'localhost'
        #],
        'DATABASES': {

        },

        'DISABLE_TRANSACTION_MANAGEMENT' : False,
        'LANGUAGES': [
            ('en', ugettext('English')),
            ('zh-cn', ugettext('Chinese')),
        ],

        'TRANSMETA_DEFAULT_LANGUAGE': 'zh-cn',
        'TIME_ZONE': 'Asia/Shanghai',
        'LANGUAGE_CODE': 'zh_cn',
        'SITE_ID': 1,
        'USE_I18N': True,
        'USE_L10N': True,
        'MEDIA_ROOT': '',
        'MEDIA_URL': '',
        'STATIC_ROOT': '',
        'STATIC_URL': '/static/',
        'ADMIN_MEDIA_PREFIX': '/static/admin/',
        'STATICFILES_FINDERS': [
            'django.contrib.staticfiles.finders.FileSystemFinder',
            'django.contrib.staticfiles.finders.AppDirectoriesFinder',
            'django.contrib.staticfiles.finders.DefaultStorageFinder',
        ],
        #Heydo gen key
        'SECRET_KEY':'&=e@@kz@&-qp0g(=3)kz%l1#w$t#0c%1c=(u$vd(vt6ub@_f&g',
        #'SECRET_KEY': 'ovvxva)f_gx7$ldaasbn+l2asdfaadfdsafasdf2##sdfsa',
        'TEMPLATE_LOADERS': ((
            'django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',)),
        ),
        'MIDDLEWARE_CLASSES': [
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.transaction.TransactionMiddleware',
        ],
        'AUTHENTICATION_BACKENDS': (
            "django.contrib.auth.backends.ModelBackend",
            #"app.user.backends.LDAPBackend",
        ),
        'TEMPLATE_CONTEXT_PROCESSORS': (
            "django.core.context_processors.debug",
            "django.core.context_processors.i18n",
            "django.core.context_processors.media",
            "django.core.context_processors.request",
            'django.core.context_processors.static',
            "django.contrib.auth.context_processors.auth",),

        'ROOT_URLCONF': 'base.urls',
        'INSTALLED_APPS': [
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'django_admin_bootstrapped',
            'django.contrib.admin',
            'django.contrib.admindocs',
        ],
        'DATE_FORMAT': 'Y-m-d',
        'DATETIME_FORMAT': 'Y-m-d H:i',
        'TIME_FORMAT': 'H:i',
        "PROXY_MEMCACHE": False,

        "memcache_settings": {
            'func_cache': ['127.0.0.1:11211'],
            'page_cache': ['127.0.0.1:11211'],
            'fragment_cache': ['127.0.0.1:11211'],
            'user_cache': ['127.0.0.1:11211'],
        },
        'enable_memcached': True,
        'apple_verify': True,

        # 缓存超时时间, 单位秒
        'cache_expire_1M'   :60,
        'cache_expire_5M'   :60 * 5,
        'cache_expire_15M'  :60 * 15,
        'cache_expire_30M'  :60 * 30,
        'cache_expire_1H'   :60 * 60,
        'cache_expire_2H'   :60 * 60 * 2,
        'cache_expire_12H'  :60 * 60 * 12,
        'cache_expire_1D'   :60 * 60 * 24,
        'cache_expire_2D'   :60 * 60 * 24 * 2,


        #'Tencent_APP_ID': 1400012778,
        'Agora_AppId': "69c9a8a700ba456ca1c47d411c3bcaa9",
        'Agora_appCertificate': "bd5b264786384dabad44fdcb1b32630b",
        'RabbitQueue_name': "chatpa",
        'Weixin_pay_notifyurl': "http://123.207.175.223/api/live/wepay/notice",
        'Alipay_notifyurl' : "http://123.207.175.223/api/live/alipay/notice",
        'Message_Tornado_host': "backapi.b4ij.cn",


        # 腾讯云 签名工具配置
        "SIG_TOOL_PATH": "/mydata/python/live_video/api/util/tencenttools/tls_sig_api-linux-64/tools",
        "SIG_KEY_PATH": "/mydata/python/live_video/api/util/tencenttools/keys_turkey",
        "SIG_PATH": '/mydata/python/live_video/api/util/tencenttools/tls_sig_api-linux-64/tools',

        "INTERNATIONAL_TYPE": 1,
        "SHARE_URL": "http://52.29.158.14/share/",
        "INVITE_URL": "http://52.29.158.14/share/",
    },


)
