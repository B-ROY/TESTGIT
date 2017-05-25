#encoding=utf8

from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User,Group
from django.core import urlresolvers
from app.permission.models import PagePermission, UserPerms,GroupPerms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


def _get_named_patterns():
    "Returns list of (pattern-name, pattern) tuples"

    resolver = urlresolvers.get_resolver(None)

    patterns = [
        (key, value[0][0][0], value[1])
        for key, value in resolver.reverse_dict.items()
        if isinstance(key, basestring)
    ]
    return patterns


@login_required
def initialize(request):
    patterns = _get_named_patterns()
    r = HttpResponse("initialized", content_type = 'text/plain')
    for i1,i2,i3 in patterns:
        #Perm.objects.create(name = i1,code = i3,url_regex = i3,action = i1)
        try:
            PagePermission.objects.get(code=i3)

        except ObjectDoesNotExist:
            p= PagePermission()
            p.name = i1
            p.code = i3
            p.url_regex = i3
            p.action = i1
            p.save()
    return r


@login_required
def user_change(request):

    if request.method == 'GET':
        userid = request.GET.get('uid')
        #get user infomation

        user = User.objects.get(id=userid)
        #user permisson list for template
        perm_qs = PagePermission.objects.all()
        perms = [
            dict(id=perm.id, name=perm.name, selected=False)
            for perm in perm_qs]

        #user permisson list for template
        #group_qs = Group.objects.all()
        # groups = [
        #     dict(id=group.id, name=group.name, selected=False)
        #     for group in group_qs
        # ]

        #add selected if user has permission
        user_perms_qs = UserPerms.objects.filter(user=user)
        user_perms_ids = [user_perm.perm_id for user_perm in user_perms_qs]
        for i in perms:
            if i['id'] in user_perms_ids:
                i['has_perm'] = True

        #add selected if user in these groups
        # user_group_qs = user.groups.all()
        # user_group_ids = [user_group.id for user_group in user_group_qs]
        #
        # for j in groups:
        #     if j['id'] in user_group_ids:
        #         j['selected'] = True

        #render the template
        return render(request, 'user/change_user.html',
                      {"perms": perms, 'user':user})


    elif request.method == 'POST':

        userid = request.POST.get('uid')
        perm_ids = request.POST.getlist('permission_list[]')
        group_ids = request.POST.getlist('group_list[]')
        user = User.objects.get(id=userid)

        #删除以前的权限
        UserPerms.objects.filter(
            user_id=userid,).delete()

        #添加新权限
        perm_ids = [long(permid) for permid in perm_ids]
        for perm_id in perm_ids:
            up = UserPerms()
            up.perm_id = perm_id
            up.user_id = userid
            up.save()

        #删除用户组
        old_groups = user.groups.all()
        for og in old_groups:
            user.groups.remove(og)
            user.save()

        #添加新组
        groups = Group.objects.filter(id__in=group_ids)
        for g in groups:
            user.groups.add(g)
            user.save()

        return HttpResponseRedirect('/perm/user/edit?uid=%s' % userid)


@login_required
def group_change(request):

    if request.method == 'GET':
        gid = request.GET.get('gid')
        #get user infomation

        group = Group.objects.get(id=gid)
        #user permisson list for template
        perm_qs = PagePermission.objects.all()
        perms = [
            dict(id=perm.id, name=perm.name, selected=False)
            for perm in perm_qs]


        group_perms_qs = GroupPerms.objects.filter(group=group)
        group_perms_ids = [group_perm.perm_id for group_perm in group_perms_qs]

        for i in perms:
            if i['id'] in group_perms_ids:
                i['has_perm'] = True

        #add selected if user in these groups

        #render the template
        return render(request, 'user/group_change.html',
                      {"perms": perms, 'group': group})


    elif request.method == 'POST':

        gid = request.POST.get('gid')
        perm_ids = request.POST.getlist('permission_list[]')
        group = Group.objects.get(id=gid)

        #删除以前的权限
        GroupPerms.objects.filter(
            group_id=gid,).delete()

        #添加新权限
        perm_ids = [long(permid) for permid in perm_ids]
        for perm_id in perm_ids:
            gp = GroupPerms()
            gp.perm_id = perm_id
            gp.group_id = gid
            gp.save()


        return HttpResponseRedirect('/perm/group/edit?gid=%s' % gid)


@login_required
def user_list(request):


    key = request.GET.get('kw')
    if key:
        qs = User.objects.filter(username__contains=key)
    else:
        qs = User.objects.all()
    page = request.GET.get('page')
    paginator = Paginator(qs, 20)
    try:
        show_users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        show_users = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        show_users = paginator.page(paginator.num_pages)

    param = "pz=20&search_kw="+key if key else "pz=20"

    return render(request, 'user_list.html', {'lines': show_users,"otherparam": param})


#
# def initialize(request):
#     patterns = _get_named_patterns()
#     r = HttpResponse("initialized", content_type = 'text/plain')
#     for i1,i2,i3 in patterns:
#         #Perm.objects.create(name = i1,code = i3,url_regex = i3,action = i1)
#         try:
#             Perm.objects.get(code=i3)
#
#         except ObjectDoesNotExist:
#             p= Perm()
#             p.name = i1
#             p.code = i3
#             p.url_regex = i3
#             p.action = i1
#             p.save()
#     return r
#
#
#
# def _get_named_patterns():
#     "Returns list of (pattern-name, pattern) tuples"
#     resolver = urlresolvers.get_resolver(None)
#
#     for url_ptn in  resolver.url_patterns:
#         print url_ptn
#
#     for key, value in resolver.reverse_dict.items() :
#         if isinstance(key, basestring):
#             print key,value
#     patterns = [
#         (key, value[0][0][0],value[1])
#         for key, value in resolver.reverse_dict.items()
#         if isinstance(key, basestring)
#     ]
#     return patterns
#
#
#
# def edit(request):
#
#
#     if request.method == "GET":
#         perms = Perm.objects.all()
#         uids = request.GET.get("uids","")
#         gids = request.GET.get("gids","")
#         if uids:
#             member = User.objects.get(id = uids)
#             _user_perms = UserPerms.objects.filter(user = member)
#             given_perm_ids =  [up.perm_id for up in _user_perms]
#         elif gids:
#             member = Group.objects.get(id = gids)
#             _usergroup_perms = UserGroupPerms.objects.filter(group = member.id)
#             given_perm_ids =  [up.perm_id for up in _usergroup_perms]
#
#         return render_to_response("admin/edit_perms.html",locals())
#     else:
#         uids = request.POST.get("uids")
#         gids = request.POST.get("gids")
#
#         chosen_perms = map(int,request.POST.getlist("chosen_perms"))
#
#         if uids:
#             former_perms = UserPerms.objects.filter(user__id = uids)
#             former_perm_ids = [up.perm_id for up in former_perms]
#             to_delete_perms = set(former_perm_ids) - set(chosen_perms)
#             to_add_perms = set(chosen_perms) - set(former_perm_ids)
#
#             UserPerms.change_perm(uids,to_delete_perms,to_add_perms)
#
#         if gids:
#             former_perms = UserGroupPerms.objects.filter(group__id = gids)
#             former_perm_ids = [ugp.perm_id for ugp in former_perms]
#             to_delete_perms = set(former_perm_ids) - set(chosen_perms)
#             to_add_perms = set(chosen_perms) - set(former_perm_ids)
#
#             UserGroupPerms.change_perm(gids,to_delete_perms,to_add_perms)
#
#         return HttpResponse("EDIT PERMS")