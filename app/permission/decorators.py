#encoding=utf-8
__author__ = 'zen'

from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

import logging

AUTO_UPDATE_PERM_NAME = True


def reg_view_perm(app_label, perm_code, perm_name):

    assert app_label
    assert perm_code
    assert perm_name

    content_type = None

    #判断app_label 是否在
    try:
        content_type = ContentType.objects.get(app_label = app_label)
    except ContentType.DoesNotExist,e:
        print "App label %s not foud!" % app_label
        raise e

    def _wrapfunc(_view_func):
        def func(request, *args, **kwargs):
            user_obj = request.user

            if not user_obj.is_active:
                raise PermissionDenied

            codename = perm_code +"_" + app_label
            perm, created = Permission.objects.get_or_create(content_type=content_type, codename=codename)
            if (not created) and AUTO_UPDATE_PERM_NAME and perm.name != perm_name:
                perm.name = perm_name
                perm.save()
                print u"perm %s updated codename:%s" % (perm.id,perm_name)
            perm_str = content_type.app_label + "." + codename
            if user_obj.has_perm(perm_str):
                return _view_func(request,*args,**kwargs)
            else:
                raise PermissionDenied


        return func

    return _wrapfunc
