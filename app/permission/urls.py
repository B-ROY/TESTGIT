#encoding=utf-8
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
   #Examples:
   url(r'init$', 'permission.views.initialize', name=u'初始化权限'),
   url(r'user/list$', 'permission.views.user_list', name=u'用户列表'),
   url(r'user/edit$', 'permission.views.user_change', name=u'用户信息'),
   url(r'group/edit$', 'permission.views.group_change', name=u'调整组权限'),
   # url(r'user/add$', 'permission.views.user_add', name=u'添加新用户'),
)


