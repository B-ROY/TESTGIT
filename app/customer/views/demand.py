# coding=utf-8

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from app.customer.models.user import *

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


@login_required()
def demand_list(request):
    qd = request.GET
    demand_id = qd.get('search_kw')

    demands = DemandList.objects.all().order_by('-id')

#   dict_demand_user = {}

    if demand_id:
        demands = demands.filter(uuid=demand_id)

    pages = Pages(demands, 20)
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

#    for demand in demands:
#        try:
#            user = User.objects.get(id=demand.uid)
#        except:
#            user = []
#        dict_demand_user[demand] = user

    return render(request, 'demand/list.html', {'demands': show_users, 'pages_to_show': pages.pages_to_show(int(page)), })


# 创建或修改
@login_required()
def demand_new(request):
    if request.method == 'POST':
        qd = request.POST
        demand_id = qd.get('demand_id', "")
        user_id = qd.get('edit_demand_id','')
        status = qd.get('edit_demand_status', '')


        if not user_id:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        #if not demand_id:
            #DemandList.create(user_id, status)
        #else:
        DemandList.gen(demand_id,user_id,status)

        return HttpResponseRedirect(reverse("demand_list"))
    else:
        qd = request.GET
        demand_id = qd.get('demand_id', "")
        current_demand = ''
        if demand_id:
            current_demand = DemandList.objects.get(id=demand_id)
        return render(request, 'demand/edit.html', {'current_demand':current_demand,'demand_id': demand_id})
    
@login_required()
def demand_delete(request):
    user_id = request.GET.get('user_id', "")
    demand = DemandList.do_invalid(user_id)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required()
def demandvideo_list(request):
    qd = request.GET
    demand_videos = DemandVideoInfo.objects.all().order_by('id')
    dict_videos = {}
    for videos in demand_videos:
        try:
            demand_user = User.objects.get(id=videos.uid)
        except:
            demand_user = []
        dict_videos[videos] = demand_user

    return render(request, 'demand/video_list.html', {'dict_videos': dict_videos })


@login_required()
def demandvideo_delete(request):
    dv_id = request.GET.get('id', "")
    demand = DemandVideoInfo.do_invalid(dv_id)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  