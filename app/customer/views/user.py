from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from app.customer.models.user import *
from app.customer.models.platform import *
from app.customer.models.channel import *
import datetime

class Pages:
    def __init__(self, objects, count):
        self.pages = Paginator(objects, count)

    def pages_to_show(self, page):
        # pages_wanted stores the pages we want to see, e.g.
        #  - first and second page always
        #  - two pages before selected page
        #  - the selected page
        #  - two pages after selected page
        #  - last two pages always
        #
        # Turning the pages into a set removes duplicates for edge
        # cases where the "context pages" (before and after the
        # selected) overlap with the "always show" pages.
        pages_wanted = set([1, 2,
                            page - 2, page - 1,
                            page,
                            page + 1, page + 2,
                            self.pages.num_pages - 1, self.pages.num_pages])

        # The intersection with the page_range trims off the invalid
        # pages outside the total number of pages we actually have.
        # Note that includes invalid negative and >page_range "context
        # pages" which we added above.
        pages_to_show = set(self.pages.page_range).intersection(pages_wanted)
        pages_to_show = sorted(pages_to_show)

        # skip_pages will keep a list of page numbers from
        # pages_to_show that should have a skip-marker inserted
        # after them.  For flexibility this is done by looking for
        # anywhere in the list that doesn't increment by 1 over the
        # last entry.
        skip_pages = [x[1] for x in zip(pages_to_show[:-1],
                                        pages_to_show[1:])
                      if (x[1] - x[0] != 1)]

        # Each page in skip_pages should be follwed by a skip-marker
        # sentinel (e.g. -1).
        for i in skip_pages:
            pages_to_show.insert(pages_to_show.index(i), -1)

        return pages_to_show
        


@login_required
def base(request):
    return render(request, 'index.html', )

@login_required
def homepage(request):
    return render(request, 'homepage.html', )


@login_required
def user_list(request):
    key = request.GET.get('search_kw', '')
    order_key = request.GET.get('order_kw', '')
    # top_users = User.objects.all().order_by('created_at')
    # top_user_ids = [t.user_id for t in top_users]

    #query user
    users = User.objects.all().filter(user_type=0)
    if key:
        try:
            skey = int(key)
            users = users.filter(id=skey)
            if not users:
                users = User.objects.filter(identity=skey)
        except Exception, e:
            users = users.filter(nickname__contains=key)

    if order_key:
        users = users.order_by('-' + OrderKey.to_s(order_key))

    else:
        users = users.order_by('-created_at')

    date = request.GET.get('search_date', '')
    if date:
        oneday = datetime.timedelta(days=1)
        _date = datetime.datetime.strptime(date, "%Y-%m-%d")
        users = users.filter(created_at__gte=_date, created_at__lt=_date + oneday).order_by('-created_at')

    pages = Pages(users, 20)
    page = request.GET.get('page')

    try:
        show_users = pages.pages.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        show_users = pages.pages.page(1)
        page = 1
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        show_users = pages.pages.page(pages.num_pages)

    param = "search_kw=" + key if key else ""

    return render(
        request, 'user/user_list.html',
        {'users': show_users, 'pages_to_show': pages.pages_to_show(int(page)),
         'order_kw': order_key, 'search_kw': key, 'search_date': date, 
         'extra1': "&order_kw=%s" % order_key, 'extra2': "&search_kw=%s" % key, 'extra3': "&search_date=%s" % date, }
    )

@login_required
def show(request,user_id):
    user = User.objects.get(id=user_id)
    search_kw = request.GET.get('search_kw', '')
    order_kw = request.GET.get('order_kw', '')
    page = request.GET.get('page', 1)
    params_list = []
    if search_kw:
        params_list.append("search_kw=" + search_kw)
    if order_kw:
        params_list.append("order_kw=" + order_kw)
    if page:
        params_list.append("page=%s" + page)
    other_params = "&".join(params_list)
    return render(request, 'user/show.html',
                  {'user': user, 'search_kw': search_kw, 'order_kw': order_kw, 'page': page,
                   'other_params': other_params})


@login_required
def check_identity(request):
    allow_add = 1
    edit_identity = request.GET.get('edit_identity', '')
    user = User.objects.filter(identity=edit_identity)
    if user:
        allow_add = 0
    return HttpResponse(json.dumps({'code': allow_add}), content_type="application/json")


@login_required
def update_identity(request):
    user_id = request.POST.get('user_id', 0)
    edit_identity = request.POST.get('edit_identity')
    user = User.objects.get(pk=user_id)
    if edit_identity:
        user.update_identity(edit_identity)
    response = {'status': 'success'}
    return HttpResponse(json.dumps(response), content_type="application/json")

@login_required
def update_nickname(request):
    user_id = request.POST.get('user_id', 0)
    nickname = request.POST.get('nickname')
    user = User.objects.get(pk=user_id)
    if nickname:
        user.nickname = nickname
        user.save()
    response = {'status': 'success'}
    return HttpResponse(json.dumps(response), content_type="application/json")

@login_required
def update_desc(request):
    user_id = request.POST.get('user_id', 0)
    desc = request.POST.get('desc','')
    user = User.objects.get(pk=user_id)
    user.desc = desc
    user.save()
    response = {'status': 'success'}
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def block(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id', 0)
        is_block = request.POST.get('value')
        user = User.objects.get(pk=user_id)
        user.is_block = int(is_block)
        user.save()
        response= {'status': 'success'}
    else:
        response = {'status': 'error', 'msg': u"only support post method!"}

    return HttpResponse(json.dumps(response), content_type="application/json")



@login_required
def add_top(request):
    user_id = request.GET.get('pk')
    user = User.objects.get(id=user_id)
    t = User()
    t.user = user
    t.seq = 0
    t.save()
    return HttpResponseRedirect('/user/list')


@login_required
def delete_top(request):
    user_id = request.GET.get('pk')
    user = User.objects.get(id=user_id)
    top_user = User.objects.get(user=user)
    top_user.delete()
    return HttpResponseRedirect('/user/list')


@login_required
def save_top_position(request):
    position = request.POST.get('user_ids')
    user_ids = [int(i) for i in position.split(',')]
    seq_map = {}

    for i in range(1, len(user_ids) + 1):
        seq_map[user_ids[i - 1]] = i

    top_users = User.objects.all()
    #
    # for t in top_users:
    #     t.seq = seq_map.get(t.user_id)
    #     t.save()
    response = {'status': 'success'}
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def gift(request):
    return render(request, 'gift/gift.html', )


@login_required
def parttime_list(request):
    order_key = request.GET.get('order_kw', 0)
    # top_users = User.objects.all().order_by('created_at')
    # top_user_ids = [t.user_id for t in top_users]

    #query user      
    users = User.objects.filter(is_parttime=1)

    if order_key == '0':
        date = request.GET.get('search_date')

        if date:
            # timeStamp
            timeArray_min = time.strptime(date, "%Y-%m-%d")
            timeStamp_min = int(time.mktime(timeArray_min))
            timeStamp_max = timeStamp_min+86400

            user_room = LiveRoom.objects.filter(created_at__gte=timeStamp_min).order_by('owner', '-created_at')
            user_room = user_room.filter(created_at__lt=timeStamp_max).order_by('owner', '-created_at')

            user_room = user_room.filter(owner__is_parttime=1)

            #list_user = []
            #for room in user_room:
            #    user = users.filter(id=room.owner_id)
            #    list_user.append(user)
            

            pages = Pages(user_room, 20)
            page = request.GET.get('page', 1)

            try:
                show_rooms = pages.pages.page(page)
            except PageNotAnInteger:
            # If page is not an integer, deliver first page.
                show_rooms = pages.pages.page(1)
                page = 1
            except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
                show_rooms = pages.pages.page(pages.num_pages)

            return render(request, 'user/parttime_list.html',
                    {'show_rooms': show_rooms, 
                    'pages_to_show': pages.pages_to_show(int(page)), 
                    'order_kw': order_key, 'search_date': date, "extra": "&order_kw=0&search_date=%s" % date, })   
        else:
            return render(request, 'user/parttime_list.html',
                    {'order_kw': order_key,})
        
    elif order_key == '1':
        key = request.GET.get('search_kw', '')
        if key:
            try:
                skey = int(key)
                users = users.get(identity=skey)
            except Exception, e:
                try:
                    users = users.get(nickname__contains=key)
                except Exception, e:
                    return render(request, 'user/parttime_list.html',
                            {'order_kw': order_key, })

            user_room = LiveRoom.objects.filter(owner_id=users.id).order_by('-created_at')

            pages = Pages(user_room, 20)
            page = request.GET.get('page', 1)

            try:
                show_rooms = pages.pages.page(page)
            except PageNotAnInteger:
            # If page is not an integer, deliver first page.
                show_rooms = pages.pages.page(1)
                page = 1
            except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
                show_rooms = pages.pages.page(pages.num_pages)

            return render(request, 'user/parttime_list.html', 
                    {'user': users, 'show_rooms': show_rooms, 'pages_to_show': pages.pages_to_show(int(page)), 
                    'order_kw': order_key, 'search_kw': key, "extra": "&order_kw=1&search_kw=%s" % key, })
        else:
            return render(request, 'user/parttime_list.html',
                    {'order_kw': order_key, })

    else:
        return render(request, 'user/parttime_list.html',
                {'order_kw': order_key, })


@login_required
def parttime_edit(request):
    key = request.GET.get('search_kw', '')
    users = User.objects.filter(is_parttime=1)

    if key:
        try:
            skey = int(key)
            users = User.objects.filter(identity=skey)
        except Exception, e:
            users = User.objects.filter(nickname__contains=key)

    pages = Pages(users, 20)
    page = request.GET.get('page', 1)

    try:
        show_users = pages.pages.page(page)
    except PageNotAnInteger:
    # If page is not an integer, deliver first page.
        show_users = pages.pages.page(1)
        page = 1
    except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
        show_users = pages.pages.page(pages.num_pages)


    return render(request, 'user/parttime_edit.html',
            {'users': users, 'show_users': show_users, 'pages_to_show': pages.pages_to_show(int(page)), })


@login_required
def parttime_show(request):

    rooms = LiveRoom.objects.filter(status=LiveRoom.ROOM_IS_OPEN).all()
    rooms = rooms.filter(owner__is_parttime=1)

    return render(request, 'user/parttime_show.html', {'rooms': rooms, })


@login_required
def set_parttime(request):
    user_id = request.GET.get('user_id')
    is_parttime = request.GET.get('is_parttime', '0') == '1'
    user = User.objects.get(id=user_id)

    #try:
    #    user = User.objects.get(pk=user_id)
    #except User.DoesNotExist:
    #    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    #    return HttpResponse(json.dumps({"status": "fail"}))
    if is_parttime:
        user.cancel_parttime()
    else:
        user.be_parttime()
    # return HttpResponse(json.dumps({"status": "success"}))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# list superadmin
@login_required
def superadmin_list(request):
    users = User.objects.filter(user_type=724882775).order_by('id')

    return render(request, 'user/superadmin_list.html',
        {'users': users, })


# edit superadmin
@login_required
def superadmin_edit(request):
    user_identity = request.GET.get('search_kw', '0')

    try:
        user = User.objects.get(identity=int(user_identity))

        return render(request, 'user/superadmin_edit.html',
            {'user': user, })
    except:
        return render(request, 'user/superadmin_edit.html')

# set superadmin
@login_required
def set_superadmin(request):
    user_id = request.GET.get('user_id')
    super_admin = request.GET.get('super_admin', '0') == '1'
    user = User.objects.get(id=user_id)

    if super_admin:
        user.cancel_superadmin()
    else:
        user.be_superadmin()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# room_user_gift
@login_required
def room_user_gift(request):
    order_key = request.GET.get('order_key', 0)
    user_id = request.GET.get('user_id', '')
    
    room_user_gift = RoomUserGift.objects.all().order_by('-created_at')

    if user_id:
        if order_key == '0':
            room_user_gift = room_user_gift.filter(user__identity=user_id)
        else:
            room_user_gift = room_user_gift.filter(sender__identity=user_id)

    pages = Pages(room_user_gift, 20)
    page = request.GET.get('page', 1)

    try:
        show_users = pages.pages.page(page)
    except PageNotAnInteger:
    # If page is not an integer, deliver first page.
        show_users = pages.pages.page(1)
        page = 1
    except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
        show_users = pages.pages.page(pages.num_pages)

#    if order_key == '0':
#        room_user_gift = RoomUserGift.objects.filter(sender__identity=user_id).order_by('-created_at')
#
#    else:
#        room_user_gift = RoomUserGift.objects.filter(user__identity=user_id).order_by('-created_at')

    return render(request, 'user/room_user_gift.html',
            {'room_user_gift': show_users, 'pages_to_show': pages.pages_to_show(int(page)), 
            "extra1": "&order_key=%s" % order_key, "extra2": "&user_id=%s" % user_id, })

# channel
@login_required
def channel_list(request):
    channels = ChannelInfo.get_channel_list()

    return render(request, 'user/channel_list.html',
        {'channels': channels, })

@login_required
def channel_edit(request):
    if request.method == "POST":
        channel_id = request.POST.get('channel_id', None)
        channel_num = request.POST.get('channel_num', "")
        channel_name = request.POST.get('channel_name', "")
        
        if not channel_id:
            status = ChannelInfo.create_channel(channel_num, channel_name)
        else:
            channel = ChannelInfo.objects.get(id=channel_id)
            channel.channel_num = channel_num
            channel.channel_name = channel_name
            channel.save()

        return HttpResponseRedirect(reverse("channel_list"))

    else:
        channel_id = request.GET.get('channel_id', None)
        if not channel_id:
            channel = []
        else:
            channel = ChannelInfo.objects.get(id=channel_id)
        
        return render(request, 'user/channel_edit.html', 
            {'channel': channel, })

@login_required
def channel_delete(request):
    channel_id = request.GET.get('channel_id')
    status = ChannelInfo.delete_channel(channel_id=channel_id)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def videoManager(request):
    VideoManagers = VideoManagerVerify.objects.all().order_by('user_id')

    return render(request,'user/video_manager_list.html',{'VideoManagers':VideoManagers})


def Status_video_manager(request):
    manager_id = request.GET.get('id')
    manager = VideoManagerVerify.objects.get(pk=manager_id)

    if request.method == "GET":
        return render(request, 'user/manager_status_edit.html',{'manager': manager})


    else:
        qd = request.POST
        status = qd.get('edit_status')
        feedback = qd.get('edit_feedback')
        status = int(status)
        manager.status = status
        manager.feedback_reason = feedback
        manager.save()
        user = User.objects.get(id=manager.user_id)
        user.is_video_auth = status
        user.save()
        video_managers = VideoManagerVerify.objects.all().order_by('user_id')
        return render(request,'user/video_manager_list.html',{'VideoManagers': video_managers})




