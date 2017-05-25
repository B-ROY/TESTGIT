#encoding=utf8

import re
from django.core.exceptions import PermissionDenied
from django.core import urlresolvers
from models import PagePermission,UserPerms, GroupPerms
from django.conf import settings


resolver = urlresolvers.get_resolver(None)
url_patterns = resolver.url_patterns
initial_regex = re.compile("^/", re.UNICODE)


def get_path_perm_code(path, pattern = resolver):

    perm_code = ""

    for sub_pattern in pattern.url_patterns:
        try:
            sub_match = sub_pattern.regex.search(path)
        except urlresolvers.Resolver404, e:
            pass
        else:
            if sub_match:
                _perm_code = sub_pattern.regex.pattern
                if _perm_code.startswith("^"):
                    _perm_code = _perm_code[1:]
                perm_code += _perm_code
                if type(sub_pattern) == urlresolvers.RegexURLResolver:
                    new_path = path[sub_match.end():]
                    perm_code += get_path_perm_code(new_path,sub_pattern)

    return perm_code



class PermMiddleware(object):


    def process_request(self, request):
        #如果用户未登录
        if not request.user.is_authenticated():
            return

        #超级用户拥有所有权限
        if request.user.is_superuser:
            return

        path = request.path
        #初始化path
        match = initial_regex.search(path)
        path = path[match.end():]

        perm_code = get_path_perm_code(path)
        if perm_code in settings.ALWAYS_ALLOWED_PERMS:
            return

        #如果用户登录
        user_obj = request.user
        try:
            perm = PagePermission.objects.get(code = perm_code)
        except PagePermission.DoesNotExist,e:
            return
        else:
            try:
                UserPerms.objects.get(user=user_obj, perm=perm)
            except UserPerms.DoesNotExist:
                #查看组权限
                groups = user_obj.groups.all()
                group_ids = [g.id for g in groups]
                ugps = GroupPerms.objects.filter(perm=perm, group_id__in=group_ids)[:1]
                if len(ugps) > 0:
                    return
            else:
                #用户有权限，直接返回
                return

            raise PermissionDenied


