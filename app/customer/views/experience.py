# coding=utf-8

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from app.customer.models.experience import UserExperienceType


@login_required()
def experience_list(request):
    qd = request.GET
    userExperienceTypes = UserExperienceType.objects.filter(status=1)
    return render(request, 'experience/list.html', {'experiences': userExperienceTypes})


# 创建或修改
@login_required()
def experience_type_new(request):
    if request.method == 'POST':
        qd = request.POST
        experience_id = qd.get('experience_id', "")
        experience_identifier = qd.get('edit_experience_identifier', "")
        experience_name = qd.get('edit_experience_name', '')
        experience_experience = qd.get('edit_experience_experience', '')
        experience_limit = int(qd.get('edit_experience_limit', 0))
        if not experience_identifier or not experience_experience:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if not experience_name:
            experience_name = experience_identifier
        if not experience_id:
            result = UserExperienceType.create(experience_identifier, experience_name, experience_experience,
                                               experience_limit)
        else:
            result = UserExperienceType.update(experience_id, experience_identifier, experience_name,
                                               experience_experience, experience_limit)
        return HttpResponseRedirect(reverse("experience_list"))
    else:
        qd = request.GET
        experience_id = qd.get('experience_id', "")
        current_experience = ""
        if experience_id:
            current_experience = UserExperienceType.objects.get(id=experience_id)
        return render(request, 'experience/edit.html', {'current_experience': current_experience})