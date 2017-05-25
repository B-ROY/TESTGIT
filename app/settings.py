#coding=utf-8
import os, sys 

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "site-packages"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "..", ".."))


def load_settings(settings, debug=False, **kwargs):
    ugettext = lambda s: s
    settings.update(
        {
            'TEMPLATE_LOADERS': (
                ('django.template.loaders.cached.Loader', (
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                )),
            ),
            'DEBUG': True,
            'TEMPLATE_DEBUG': True,
            'ALLOWED_HOSTS' : ['*'],
            'TEST': False,
            'PROJECT_ROOT': PROJECT_ROOT,
            'TEMPLATE_DIRS': (
                os.path.join(PROJECT_ROOT, "templates"),
            ),

            'ROOT_URLCONF': 'app.urls',
            'STATICFILES_FINDERS': [
                'django.contrib.staticfiles.finders.FileSystemFinder',
                'django.contrib.staticfiles.finders.AppDirectoriesFinder',
                # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
            ],

            'STATICFILES_DIRS': (
                os.path.join(PROJECT_ROOT, 'static'),
            ),
            'STATIC_ROOT': '/static/',
            'STATIC_URL': '/static/',
            'ADMIN_MEDIA_PREFIX': '/static/admin/',

            'TEMPLATE_CONTEXT_PROCESSORS': (
                "django.core.context_processors.debug",
                "django.core.context_processors.i18n",
                "django.core.context_processors.media",
                "django.core.context_processors.request",
                'django.core.context_processors.static',
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ),

            'MIDDLEWARE_CLASSES': [
                'django.middleware.common.CommonMiddleware',
                'django.contrib.sessions.middleware.SessionMiddleware',
                'django.contrib.auth.middleware.AuthenticationMiddleware',
                'app.permission.middleware.PermMiddleware',
                'django.contrib.messages.middleware.MessageMiddleware',
                'django.middleware.transaction.TransactionMiddleware',
            ],

            'INSTALLED_APPS': [
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.messages',
                'django.contrib.staticfiles',
                'django_admin_bootstrapped',
                'django.contrib.admin',
                'django.contrib.admindocs',
                'customer',
                'audio',
                'picture',
                'video',
                ],

            "LOGIN_URL": "/signin",
            "LOGIN_REDIRECT_URL": "/",
            "DEBUG": True,
            "ALWAYS_ALLOWED_PERMS": ("signout/$", "signin/$"),

            "BIG_GIFT_THRESHOLD": 5200,

        }
    )


def check_settings(settings):
    pass

