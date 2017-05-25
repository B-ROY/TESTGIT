# coding=utf-8

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from app.customer.models.user import LuckIDInfo


@login_required()
def lucknum_list(request):
    qd = request.GET
    lucknums = LuckIDInfo.objects.all().order_by('user_id')
    return render(request, 'lucknum/list.html', {'lucknums': lucknums})

# 创建或修改
@login_required()
def lucknum_new(request):
    if request.method == 'POST':
        qd = request.POST
        user_id = qd.get('user_id', "")
        id_type = qd.get('id_type', '')
        id_level = qd.get('id_level', '')
        id_assign = qd.get('id_assign', '')

        return HttpResponseRedirect(reverse("lucknum_list"))
    else:
        qd = request.GET
        user_id = qd.get('user_id', "")
        id_type = 0
        id_level = 0
        id_assign = 0

        return render(request, 'lucknum/edit.html', {'user_id': user_id, 'id_type': id_type,'id_level':id_level,'id_assign':id_assign})