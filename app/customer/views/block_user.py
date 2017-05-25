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
from app.customer.models.block_user import *
from datetime import *

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
def block_user_list(request):
    page = request.GET.get('page', 1)
    search_key = request.GET.get('search_key')
    
    if search_key:
        block_users = BlockUser.objects.filter(block_user__identity=search_key)
        return render(request, 'block_user/list.html',
                {'block_users': block_users, })
    block_users = BlockUser.objects.all().order_by('-id')

    pages = Pages(block_users, 20)
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

    for user in show_users:
        user.user = User.objects.get(id=user.block_user)
        user.admin = User.objects.get(id=user.block_admin)

    return render(request, 'block_user/list.html',
            {'block_users': show_users, 'pages_to_show': pages.pages_to_show(int(page)),})


@login_required
def block_user_update(request):
    update_id = request.GET.get('id')
    block_user = BlockUser.objects.get(id=update_id)
    if update_id:
        block_user.cancel_block()

	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def block_user_new(request):
    if request.method == 'POST':
        qd = request.POST
        user = qd.get('edit_block_user')
        block_user = User.objects.get(identity=user)
        admin = int(qd.get('edit_block_admin', 0))
        block_long = qd.get('edit_block_long', '')
        reason = qd.get('edit_block_reason', '')

        room = LiveRoom.objects.filter(owner=user).order_by('-created_at').first()

        if admin == 0:
            block_admin = User.objects.get(id=1)
        else:
            block_admin = User.objects.get(identity=admin)

        if room:
            if room.status == 1:
                room.block_room()
            else:
                room = None
        else:
            room = None
        
        if block_user.is_block == 0:
            block_user.be_block()

        block_start = datetime.now()
        if block_long != '0':
            block_end = datetime.now() + timedelta(hours=int(block_long))
        else:
            block_end = None

        try:
            BlockUser.add_block_user(block_user.id, block_admin.id, room, block_start, block_end, 1, reason)
        except Exception, e:
            logging.error("add block user error:{0}".format(e))
        return HttpResponseRedirect(reverse("block_user_list"))
    
    else:
        return render(request, 'block_user/edit.html')


