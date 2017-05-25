# coding=utf-8
import json
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from app.customer.models.startup_image import StartupImage
from app.customer.common_util.image import UploadImage

@login_required()
def startup_image_list(request):
    startup_images = StartupImage.objects.filter(delete_status=0).order_by('-id')
    return render(request, 'startup_image/list.html', {'startup_images': startup_images})


# 创建或修改
@login_required()
def startup_image_edit(request):
    if request.method == 'POST':
        #get params
        qd = request.POST
        status = int(qd.get('status', 0))
        image = qd.get('image', '')
        url = qd.get('url', '')
        startup_image_id = qd.get('startup_image_id')
        if not startup_image_id:
            #create
            StartupImage.create(url, image, status)
        else:
            #update
            StartupImage.update(startup_image_id, url, image, status)
        return HttpResponseRedirect(reverse("startup_image_list"))

    else:
        qd = request.GET
        startup_image_id = qd.get('startup_image_id', "")
        startup_image = StartupImage()
        if startup_image_id:
            try:
                startup_image = StartupImage.objects.get(id=startup_image_id)
            except StartupImage.DoesNotExist:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return render(request, 'startup_image/edit.html', {'startup_image': startup_image, })


# @login_required
# def adv_position(request):
#     position = request.POST.get('startup_image_ids')
#     adv_ids = [int(i) for i in position.split(',')]
#     seq_map = {}
#
#     for i in range(1, len(adv_ids)+1):
#         seq_map[adv_ids[i-1]] = i
#
#     advs = StartupImage.objects.all()
#
#     for adv in advs:
#         adv.seq = seq_map.get(adv.id)
#         adv.save()
#     response = {'status': 'success'}
#     return HttpResponse(json.dumps(response), content_type="application/json")

MIMEANY = '*/*'
MIMEJSON = 'application/json'
MIMETEXT = 'text/plain'


def response_mimetype(request):
    """response_mimetype -- Return a proper response mimetype, accordingly to
    what the client accepts, as available in the `HTTP_ACCEPT` header.

    request -- a HttpRequest instance.

    """
    can_json = MIMEJSON in request.META['HTTP_ACCEPT']
    can_json |= MIMEANY in request.META['HTTP_ACCEPT']
    return MIMEJSON if can_json else MIMETEXT


class JSONResponse(HttpResponse):
    """JSONResponse -- Extends HTTPResponse to handle JSON format response.

    This response can be used in any view that should return a json stream of
    data.

    Usage:

        def a_iew(request):
            content = {'key': 'value'}
            return JSONResponse(content, mimetype=response_mimetype(request))

    """
    def __init__(self, obj='', json_opts=None, mimetype=MIMEJSON, *args, **kwargs):
        json_opts = json_opts if isinstance(json_opts, dict) else {}
        content = json.dumps(obj, **json_opts)
        super(JSONResponse, self).__init__(content, mimetype, *args, **kwargs)



@login_required
def upload_img(request):

    if request.method == 'POST':

        file_obj = request.FILES[u'files[]']

        up = UploadImage(file_obj)
        data = up.push_to_qclude()

        code = data.get('code')
        if code != 0:
            response_data = {
                "e":{
                    "code": -1
                }
            }
        else:
            response_data = {
                "files": [
                    {
                        "name": file_obj.name,
                        "type": file_obj.content_type,
                        "size": file_obj.size,
                        "url": data.get("data",{}).get('download_url','')
                    }
                ]
            }

        response = JSONResponse(response_data, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
    else:
        return HttpResponse('OK')

@login_required()
def startup_image_delete(request):
    startup_image_id = request.GET.get('startup_image_id', "")
    startup_image = StartupImage.objects.get(id=startup_image_id)
    startup_image.delete_status = 1
    startup_image.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
