# coding=utf-8
import json
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from app.customer.models.adv import Adv
from app.customer.models.user import *
from app.customer.common_util.image import UploadImage

@login_required()
def adv_list(request):
    advs = Adv.objects.filter(delete_status=0).order_by('seq')
    return render(request, 'adv/list.html', {'advs': advs})


# 创建或修改
@login_required()
def adv_edit(request):
    if request.method == 'POST':
        adv_id = request.POST.get('adv_id')
        if not adv_id:
            image = request.FILES.get('image')
            if not image:
                return HttpResponse(u'请添加图片')
            
            idata = image.read()
            data = UploadImage.push_binary_to_qclude(idata)
            url = data.get("data",{}).get('download_url','')

            qd = request.POST
            adv_title = qd.get('adv_title', '')
            adv_type = int(qd.get('adv_type', 0))
            adv_info = qd.get('adv_info', '')
            status = int(qd.get('status', 0))

            Adv.create(
                adv_title, adv_info, url, adv_type, status
            )
            #print image, adv_title, adv_type, adv_info, status

            return HttpResponse(u'上传成功')
        else:
            qd = request.POST
            adv_title = qd.get('adv_title', '')
            adv_type = int(qd.get('adv_type', 0))
            adv_info = qd.get('adv_info', '')
            status = int(qd.get('status', 0))

            adv = Adv.objects.get(id=adv_id)
            adv.status = status
            adv.adv_info = adv_info
            adv.adv_type = adv_type
            adv.title = adv_title
            adv.save()

            return HttpResponseRedirect(reverse("adv_list"))
        #get params
        #qd = request.POST
        #status = qd.get('status', 0)
        #image = qd.get('image', '')
        #adv_info = qd.get('adv_info', '')
        #adv_title = qd.get('adv_title', '')
        #adv_type = qd.get('adv_type', 0)
        #adv_id = qd.get('adv_id')
        # logo_file_obj = request.FILES[u"files[]"]
        # print request.FILES
        # u = UploadImage(logo_file_obj)
        # data = u.push_to_qclude()
        # print data
        # logo = data.get('data')['download_adv_info']
        #if not adv_id:
        #    #create
        #    Adv.create(
        #        adv_title, adv_info, image, adv_type, status
        #    )
        #else:
        #    #update
        #    Adv.update(
        #        adv_id, adv_title, adv_info, image, adv_type, status
        #    )
        #return HttpResponseRedirect(reverse("adv_list"))

    else:
        qd = request.GET
        adv_id = qd.get('adv_id', "")
        adv = ''
        if adv_id:
            try:
                adv = Adv.objects.get(id=adv_id)
            except Adv.DoesNotExist:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return render(request, 'adv/edit.html', {'adv': adv,})


@login_required
def adv_upload(request):
    if request.method == "POST":
        image = request.FILES.get('edit_image')
        if not image:
            return HttpResponse(u'请添加图片')
        adv_id = request.GET.get('adv_id')
        adv = Adv.objects.get(id=adv_id)
        idata = image.read()
        data = UploadImage.push_binary_to_qclude(idata)
        url = data.get("data",{}).get('download_url','')
        adv.image = User.convert_http_to_https(url)
        adv.save()
        
        return HttpResponse(u'上传成功')
    else:
        return HttpResponse(u'上传失败')


@login_required
def adv_position(request):
    advs = Adv.objects.all()
    for adv in advs:
        position = request.POST.get(str(adv.id), 0)
        if position:
            adv.seq = position
            adv.save()
    #adv_ids = [int(i) for i in position.split(',')]
    #seq_map = {}

    #for i in range(1, len(adv_ids)+1):
    #    seq_map[adv_ids[i-1]] = i

    #advs = Adv.objects.all()

    #for adv in advs:
    #    adv.seq = seq_map.get(adv.id)
    #    adv.save()
    response = {'status': 'success'}
    return HttpResponse(json.dumps(response), content_type="application/json")

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
def adv_delete(request):
    adv_id = request.GET.get('adv_id', "")
    adv = Adv.objects.get(id=adv_id)
    adv.delete_status = 1
    adv.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
