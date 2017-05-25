#encoding=utf8

from django import template
import copy
import re
from app.permission.models import PagePermission ,UserPerms, GroupPerms

register = template.Library()

MENU_CONFIG = [
    {
        "id": "file upload",
        "name": "上传",
        "icon": '''<i class="fa  fa-upload fa-fw"></i>''',
        "path": "/thirdpart/upload/view",

    },

    {
        "id": "file upload",
        "icon": '''<i class="fa fa-history fa-fw"></i>''',
        "name": "上传历史",
        "path": "/thirdpart/upload/history",
    },

    {
        "id": "secret",
        "name": "内部审核",
        "icon": '''<i class="fa  fa-check fa-fw"></i>''',
        "is_super": True,
        "path": "/thirdpart/check"
    },

    {
        "icon": '''<i class="fa fa-gear fa-fw"></i>''',
        "id": "menu_admin",
        "name": "系统管理",
        "path": "/admin",
        'target': "_blank",
        "is_super": True,
    },
]


def has_perm(perm_codes, path):

    if path.startswith("/"):
        path = path[1:]
    for perm_code in perm_codes:
        if re.compile("^"+perm_code).search(path):
            return True
    return False


def get_user_perm_codes(user):

    gids = [g.id for g in user.groups.all()]
    gups = GroupPerms.objects.filter(group_id__in=gids)
    ups = UserPerms.objects.filter(user=user)
    perm_ids = set([up.perm_id for up in ups] + [gup.perm_id for gup in gups])
    perms = PagePermission.objects.filter(id__in=perm_ids)
    perm_codes = [perm.code for perm in perms]
    return perm_codes


def gen_menu_tree(user):

    #如果是管理员返回所有权限
    if user.is_superuser:
        return MENU_CONFIG

    perm_codes = get_user_perm_codes(user)
    user_menu = []

    for root in MENU_CONFIG:
        if root.has_key("path"):
            if has_perm(perm_codes, root["path"]):
                user_menu.append(root)
        else:
            valid_children = []
            if len(root.get("children",[])) > 0:
                for child in root.get("children"):
                    if child.has_key("path"):
                        if has_perm(perm_codes,child["path"]):
                            valid_children.append(child)

            if valid_children:
                _root = copy.deepcopy(root)
                _root["children"] = valid_children
                user_menu.append(_root)
    return user_menu


@register.simple_tag(takes_context=True)
def load_sidebar(context):
    ret_html = ''
    li_html_template = '''<li class="dropdown">{a}{ul}</li>'''
    user = context["request"].user

    url_nodes = gen_menu_tree(user)
    for url_node in url_nodes:
        if url_node.has_key('path'):
            a = '''<a href="{path}">{icon}  {name}</a>'''.format(
                icon=url_node.get('icon',''),
                name=url_node.get('name', ''),
                path=url_node.get('path', ''))
            li_html = li_html_template.format(a=a, ul='')

        elif url_node.has_key('children'):

            a = '''<a class="" href="#">{icon}  {name}
            <i class="fa fa-caret-down"></i></a>'''.format(
                icon=url_node.get('icon'),
                name=url_node.get('name'))

            children_li = ''
            node_childen = url_node.get('children',[])
            for node_child in node_childen:
                if node_child.has_key('path'):
                    children_li += '''<li><a href="{path}">{name}</a></li>'''.format(
                        name=node_child.get('name', ''),
                        path=node_child.get('path', ''),
                    )

            ul = '''<ul class="nav nav-second-level">{childen_li}</ul>'''.format(
                childen_li=children_li
            )
            li_html = li_html_template.format(a=a, ul=ul)

        ret_html += li_html

    return ret_html



