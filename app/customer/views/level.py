# coding=utf-8

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from app.customer.models.level import Level


@login_required()
def level_list(request):
    qd = request.GET
    levels = Level.objects.filter(status=1).order_by('grade')
    return render(request, 'level/list.html', {'levels': levels})

# 创建或修改
@login_required()
def level_new(request):
    if request.method == 'POST':
        qd = request.POST
        level_id = qd.get('level_id', "")
        level_grade = qd.get('edit_level_grade', '')
        level_name = qd.get('edit_level_name', '')
        level_experience = qd.get('edit_level_experience', '')
        if not level_grade or not level_experience:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if not level_name:
            level_name = "第" + str(level_grade) + "级"
        if not level_id:
            result = Level.create(level_grade, level_name, level_experience)
        else:
            result = Level.update(level_id, level_grade, level_name, level_experience)
        return HttpResponseRedirect(reverse("level_list"))
    else:
        qd = request.GET
        level_id = qd.get('level_id', "")
        current_level = ''
        plan_level = Level.last_level() + 1
        if level_id:
            current_level = Level.objects.get(id=level_id)
        return render(request, 'level/edit.html', {'current_level': current_level, 'plan_level': plan_level})