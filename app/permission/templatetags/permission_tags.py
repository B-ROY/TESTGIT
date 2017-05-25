#encoding=utf8

from django import template
from django.conf import settings
import copy
import re
from app.permission.models import PagePermission,UserPerms,GroupPerms

register = template.Library()


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
    perm_ids = set([up.perm_id for up in ups]+ [gup.perm_id for gup in gups])
    perms = PagePermission.objects.filter(id__in=perm_ids)
    perm_codes = [perm.code for perm in perms]

    return perm_codes


def gen_menu_tree(user):

    if user.is_superuser:
        return settings.MENU_CONFIG

    perm_codes = get_user_perm_codes(user)

    user_menu = []
    for root in settings.MENU_CONFIG:
        if root.has_key("path"):
            if has_perm(perm_codes,root["path"]):
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
def show_user_top_menu(context):

    li_html = u''
    user = context["request"].user
    user_menu = gen_menu_tree(user)

    for m in user_menu:
        if m.get("divider"):
            li_html += m.get("html")
        elif m.has_key("path"):
            li_html += u'<li><a id="%s" href="%s" target="%s">%s</a></li>' % (m["id"], m["path"],
                                                                              m.get("target", ''), m["name"])
        else:
            _sub_ul_html = u""
            for c in m.get("children",[]):

                if c.get("divider"):
                    _sub_ul_html += c.get("html")
                else:
                    _sub_ul_html += u'<li><a href="%s">%s</a></li>' % (c["path"],c["name"])

            li_html += u'<li class="dropdown"><a id="%s" href="#" class="dropdown-toggle" data-toggle="dropdown">%s<b class="caret"></b></a><ul class="dropdown-menu" role="menu" aria-labelledby="%s">%s</ul></li>' % (m["id"],m["name"],m["id"],_sub_ul_html)

    return li_html





@register.simple_tag(takes_context=True)
def show_user_left_navi(context):
    """
    <li class="nav-header">Sidebar</li>
                      <li class="active"><a href="#">Link</a></li>
                      <li><a href="#">Link</a></li>

                      <li class="nav-header">Sidebar</li>
                      <li><a href="#">Link</a></li>
                      <li><a href="#">Link</a></li>

                      <li class="nav-header">Sidebar</li>
                      <li><a href="#">Link</a></li>
    """
    li_html = u''
    user = context["request"].user
    cur_path = context["request"].path
    user_menu = gen_menu_tree(user)
    active_css = u'class="active" '

    def _get_m():
        for m in user_menu:
            if m.has_key("path"):
                if cur_path.startswith(m["path"]):
                    return m
            else:
                for c in m.get("children",[]):
                    if c.has_key("path"):
                        if c["path"].startswith(cur_path):
                            return m

    m = _get_m()
    if m:
        if m.has_key("path"):
            li_html += u'<li class="nav-header" %s><a href="%s" >%s</a></li>' % (active_css,m['path'],m["name"])

        else:
            _sub_html = u'<li class="nav-header">%s</li>' % m['name']
            for c in m.get("children",[]):
                if c.has_key("path"):
                    if c["path"].startswith(cur_path):
                        if cur_path == "/":
                            if c['path'] == cur_path:
                                _sub_html += u'<li %s><a href="%s" >%s</a></li>' % (active_css,c['path'],c['name'])
                            else:
                                _sub_html += u'<li ><a href="%s" >%s</a></li>' % (c['path'],c['name'])
                        else:
                            _sub_html += u'<li %s><a href="%s" >%s</a></li>' % (active_css,c['path'],c['name'])
                    else:
                        _sub_html += u'<li><a href="%s"  >%s</a></li>' % (c['path'],c['name'])
            li_html += _sub_html

    return li_html


@register.simple_tag(takes_context=True)
def show_user_left_navi_bootstrap3(context):
    """
    <li class="nav-header">Sidebar</li>
                      <li class="active"><a href="#">Link</a></li>
                      <li><a href="#">Link</a></li>

                      <li class="nav-header">Sidebar</li>
                      <li><a href="#">Link</a></li>
                      <li><a href="#">Link</a></li>

                      <li class="nav-header">Sidebar</li>
                      <li><a href="#">Link</a></li>
    """
    li_html = u''
    user = context["request"].user
    cur_path = context["request"].path
    user_menu = gen_menu_tree(user)
    active_css = u'class="active" '

    def _get_m():
        for m in user_menu:
            if m.has_key("path"):
                if cur_path.startswith(m["path"]):
                    return m
            else:
                for c in m.get("children", []):
                    if c.has_key("path"):
                        if c["path"].startswith(cur_path):
                            return m

    m = _get_m()
    if m:
        if m.has_key("path"):
            li_html += u'<li %s><a href="%s">%s</a></li>' % (active_css, m['path'], m["name"])

        else:
            _sub_html = u'<li class="disabled"><a href="#">%s</a></li>' % m['name']
            for c in m.get("children", []):
                if c.has_key("path"):
                    if c["path"].startswith(cur_path):
                        if cur_path == "/":
                            if c['path'] == cur_path:
                                _sub_html += u'<li %s><a href="%s" >%s</a></li>' % (active_css, c['path'], c['name'])
                            else:
                                _sub_html += u'<li ><a href="%s" >%s</a></li>' % (c['path'], c['name'])
                        else:
                            _sub_html += u'<li %s><a href="%s" >%s</a></li>' % (active_css, c['path'], c['name'])
                    else:
                        _sub_html += u'<li><a href="%s"  >%s</a></li>' % (c['path'], c['name'])
            li_html += _sub_html

    return li_html




