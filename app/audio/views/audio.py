# -*- coding: utf-8 -*-
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
from app.customer.models.account import *
from app.customer.models.online_user import *

from app.audio.models.audio import *
from app.audio.models.price import *
from app.audio.models.record import *
from app.audio.models.child_audio import *

import datetime
import time


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
def audio_price_list(request):
    audio_price_list = PriceList.objects.all()
    return render(request, 'audio_price_list.html',
        {'audio_price_list': audio_price_list, })

@login_required
def audio_price_edit(request):
    price_id = request.GET.get('price_id')
    price = PriceList.objects.get(id=price_id)
    
    if request.method == "GET":
        return render(request, 'audio_price_edit.html',
            {'price': price, })
    else:
        qd = request.POST
        audio_price = qd.get('edit_audio_price')
        audio_desc = qd.get('edit_audio_desc')
        price.price = audio_price
        price.desc = audio_desc
        price.save()
        
        audio_price_list = PriceList.objects.all()
        return render(request, 'audio_price_list.html',
            {'audio_price_list': audio_price_list, })

@login_required
def child_audio_list(request):
    child_audio_list = ChildAudioRecord.objects.all().order_by("-open_time")

    pages = Pages(child_audio_list, 20)
    page = request.GET.get('page')

    try:
        show_audios = pages.pages.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        show_audios = pages.pages.page(1)
        page = 1
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        show_audios = pages.pages.page(pages.num_pages)

    for audio in show_audios:
        audio.user = User.objects.get(id=audio.user_id)
        audio.audio_info = ChildUserInfo.objects.get(user_id=audio.user_id)

    return render(request, 'child_audio_list.html',
        {'child_audios': show_audios, 'pages_to_show': pages.pages_to_show(int(page)), })


@login_required
def child_audio_create(request):
    if request.method == "GET":
        prices = PriceList.objects.all()
        return render(request, 'child_audio_create.html', 
            {'prices': prices, })
    else:
        qd = request.POST
        user_identity = int(qd.get('edit_user_identity'))
        audio_price = int(qd.get('edit_audio_price'))
        listen_url = str(qd.get('edit_listen_url'))
        audio_status = int(qd.get('edit_audio_status'))

        if audio_status != 4:
            user_id = User.objects.get(identity=user_identity).id
            OnlineUser.update_online_user(user_id, "Login")

        ChildAudioRecord.create_child_audio(user_identity, audio_price, listen_url, audio_status)
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def child_audio_edit(request):
    if request.method == "GET":
        record_id = request.GET.get('record_id')
        record = ChildAudioRecord.objects.get(id=record_id)
        user = User.objects.get(id=record.user_id)
        prices = PriceList.objects.all()

        return render(request, 'child_audio_edit.html', 
            {'record': record, 'user': user, 'prices': prices, })
    else:
        qd = request.POST
        user_identity = int(qd.get('edit_user_identity'))
        audio_price = int(qd.get('edit_audio_price'))
        listen_url = str(qd.get('edit_listen_url'))
        audio_status = int(qd.get('edit_audio_status'))

        user_id = User.objects.get(identity=user_identity).id
        if audio_status == 1 or audio_status == 2 or audio_status == 0:
            OnlineUser.update_online_user(user_id, "Login")
        else:
            OnlineUser.update_online_user(user_id, "Logout")

        ChildAudioRecord.update_child_audio(user_identity, audio_price, listen_url, audio_status)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def close_child_audio(request):
    record_id = request.GET.get('record_id')
    ChildAudioRecord.close_child_audio(record_id)
    user_id = ChildAudioRecord.objects.get(id=record_id).user_id

    OnlineUser.update_online_user(user_id, "Logout")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def audio_price_add(request):

    return render(request,'audio_price_add.html')


def priceHanler(request):
    try:
        price = request.POST.get('add_audio_price')
        desc = request.POST.get('add_audio_desc')
        times = request.POST.get('limit_times')

        price = PriceList(price=price,desc=desc,limit_time=times)
        price.save()

        audio_price_list = PriceList.objects.all()

        return render(request, 'audio_price_list.html',{'audio_price_list': audio_price_list, })

    except Exception as e:
        print e
        return HttpResponse('False')



def video_price_handler(request):
    VideoPrices = VideoPriceList.objects.all()

    return render(request,'video_price_list.html',{'VideoPrices':VideoPrices})


def edit_price_handler(request):

    video_id = request.GET.get('video_id')
    print video_id
    video = VideoPriceList.objects.get(id=video_id)

    if request.method == "GET":
        return render(request, 'video_price_edit.html',{'video': video})



    else:
        qd = request.POST
        video_price = qd.get('edit_video_price')
        video_desc = qd.get('edit_video_desc')
        video.price = video_price
        video.desc = video_desc
        video.save()
        
        VideoPrices = VideoPriceList.objects.all().order_by('-price')
        return render(request, 'video_price_list.html',{'VideoPrices': VideoPrices})



def add_price_handler(request):

    return render(request,'video_price_add.html')

def add_handler(request):
    try:
        price = request.POST.get('edit_video_price')
        desc = request.POST.get('edit_video_desc')
        times = request.POST.get('edit_limit_time')

        video = VideoPriceList(price=price,desc=desc,limit_time=times)
        video.save()

        VideoPrices = VideoPriceList.objects.all().order_by("-price")


        return render(request, 'video_price_list.html',{'VideoPrices': VideoPrices})

    except Exception as e:
        print e
        return HttpResponse('False')















