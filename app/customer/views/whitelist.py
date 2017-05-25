# coding=utf-8

from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages

from app.customer.models.user import *
from wi_model_util.imodel import *


@login_required
def whitelist_list(request):
    whitelists = Whitelist.objects.filter(status=Whitelist.STATUS_USING).order_by('-position')
    attach_foreignkey(whitelists, Whitelist.lister)
    return render(
        request, 'whitelist/list.html',
        {'whitelists': whitelists, }
    )

@login_required
def edit_whitelist(request):
    if request.method == 'POST':
        whitelist_id = request.POST.get('whitelist_id')
        if whitelist_id:
            whitelist = Whitelist.objects.get(id=whitelist_id)
        else:
            whitelist = Whitelist(status=Whitelist.STATUS_USING)
        whitelist.lister_id = request.POST.get('lister_id')
        whitelist.position = request.POST.get('position')
        checked, error = whitelist.check_valid()
        if not checked:
            messages.error(request, Whitelist.ERROR_MAP.get(error))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        whitelist.save()
        return HttpResponseRedirect(reverse("whitelist_list"))
    else:
        whitelist_id = request.GET.get('whitelist_id')
        if whitelist_id:
            whitelist = Whitelist.objects.get(id=whitelist_id)
        else:
            whitelist = Whitelist()
        return render(request, 'whitelist/edit.html', {'current_whitelist': whitelist, })

@login_required
def delete_whitelist(request):
        whitelist_id = request.GET.get('whitelist_id')
        whitelist = Whitelist.objects.get(id=whitelist_id)
        whitelist.status = Whitelist.STATUS_DELETED
        whitelist.save()
        return HttpResponseRedirect(reverse("whitelist_list"))


