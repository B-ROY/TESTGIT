# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'app.thirdpart.views.main', name='首页'),
    # url(r'^item/detail/$', 'app.thirdpart.views.item_detail', name='详情'),
    # url(r'^mysite/', include('mysite.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    #/admin/auth/user/

    url(r'^$', 'app.customer.views.user.base'),
    url(r'^homepage/$', 'app.customer.views.user.homepage'),
    # url(r'^stat$', 'statistics.views.index.index', name="statistics_index"),
    url(r'^audio/', include('app.audio.urls')),
    url(r'^add/top', 'app.customer.views.user.add_top'),
    url(r'^del/top', 'app.customer.views.user.delete_top'),
    url(r'^top/position', 'app.customer.views.user.save_top_position'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^customer/', include('app.customer.urls')),

    url(r'^signin/$', 'django.contrib.auth.views.login', {'template_name': 'signin.html'}, name="signin"),
    url(r'^signout/$', 'django.contrib.auth.views.logout_then_login',  name="signout"),

    ###################################################################################################################
    #  定义静态文件处理函数
    ###################################################################################################################
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT,}),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

