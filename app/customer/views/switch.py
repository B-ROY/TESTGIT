#!/usr/bin/env python  
# -*- coding: utf-8 -*-  
__author__ = 'zen@heydo.tv'
__date__ = '2016-06-21'

import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from app.customer.models.switch import Switcher

@login_required()
def switch_list(request):
    switchers = Switcher.get_all()
    return render(request, 'switch/list.html', {'switchers': switchers})

@login_required()
def switch_edit(request):
    if request.method == 'POST':
        qd = request.POST
        switch_id = qd.get('switch_id')
        name = qd.get('name', '')
        description = qd.get('description', '')
        platform = qd.get('platform', '')
        status = qd.get('status')
        if not switch_id:
            #create
            Switcher.create(
                name, description, platform, status
            )
        else:
            #update
            Switcher.update(
                switch_id, name, description, platform, status
            )
        return HttpResponseRedirect(reverse("switch_list"))

    else:
        qd = request.GET
        switch_id = qd.get('switch_id', "")
        switch = ''
        if switch_id:
            try:
                switch = Switcher.objects.get(id=switch_id)
            except Switcher.DoesNotExist:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return render(request, 'switch/edit.html', {'switch': switch})

@login_required()
def platform_json(request):
    return HttpResponse(json.dumps([u'IOS', u'H5', u'ANDROID', u'WEB']))

@login_required()
def switch_delete(request):
    switch_id = request.GET.get('switch_id', "")
    switcher = Switcher.objects.get(id=switch_id)
    switcher.delete_status = 1
    switcher.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
