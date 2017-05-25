#!/usr/bin/env python  
# -*- coding: utf-8 -*-  
__author__ = 'zen@heydo.tv'
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from app.customer.models.version_info import VersionInfo

@login_required()
def version_list(request):
    versions = VersionInfo.get_all()
    return render(request, 'version_info/list.html', {'versions': versions})

@login_required()
def version_edit(request):
    if request.method == 'POST':
        qd = request.POST
        version_id = qd.get('version_id')
        app_name = qd.get('app_name', '')
        version = qd.get('version', '')
        download_url = qd.get('download_url', '')
        platform = qd.get('platform', '')
        upgrade_type = qd.get('upgrade_type')
        version_code = qd.get('version_code')
        upgrade_info = qd.get('upgrade_info', '')
        if not version_id:

            #create
            VersionInfo.create(
                app_name, version, platform, upgrade_type, download_url, version_code, upgrade_info
            )

        else:
            #update
            VersionInfo.update(
                version_id, app_name, version, platform, upgrade_type, download_url, version_code, upgrade_info
            )
#            print 'upgrade info2 is'+upgrade_info
        return HttpResponseRedirect(reverse("version_list"))

    else:
        qd = request.GET
        version_id = qd.get('version_id', "")
        version = ''
        if version_id:
            try:
                version = VersionInfo.objects.get(id=version_id)
            except VersionInfo.DoesNotExist:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return render(request, 'version_info/edit.html', {'version': version})

@login_required()
def version_delete(request):
    version_id = request.GET.get('version_id', "")
    version = VersionInfo.objects.get(id=version_id)
    version.delete_status = 1
    version.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
