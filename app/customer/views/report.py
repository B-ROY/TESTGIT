# coding=utf-8

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from wi_model_util.imodel import *


@login_required()
def report_list(request):
    qd = request.GET
    reports = Report.objects.all().order_by('status','-created_time')
    attach_foreignkey(reports, Report.liveRoom)
    return render(request, 'report/list.html', {'reports': reports})


# 忽略
@login_required()
def report_ignore(request):
    qd = request.GET
    report_id = qd.get('report_id', "")
    if report_id:
        current_report = Report.objects.get(id=report_id)
        if current_report.status == 0:
            result = Report.to_complete(report_id, "忽略")
    return HttpResponseRedirect(reverse("report_list"))

# 下线
@login_required()
def report_off(request):
    qd = request.GET
    report_id = qd.get('report_id', "")
    if report_id:
        current_report = Report.objects.get(id=report_id)
        if current_report.status == 0:
            result = Report.to_complete(report_id, "下线")
            current_report.liveRoom.close_room()
    return HttpResponseRedirect(reverse("report_list"))

# 处理
@login_required()
def report_edit(request):
    if request.method == 'POST':
        qd = request.POST
        report_id = qd.get('report_id', "")
        report_result = qd.get('edit_report_result', '')
        if not report_result:
            report_result = "忽略"
        if report_id:
            result = Report.to_complete(report_id, report_result)
        return HttpResponseRedirect(reverse("report_list"))
    else:
        qd = request.GET
        report_id = qd.get('report_id', "")
        if report_id:
            current_report = Report.objects.get(id=report_id)
            if current_report.status == 0:
                return render(request, 'report/edit.html', {'current_report': current_report})
        return HttpResponseRedirect(reverse("report_list"))