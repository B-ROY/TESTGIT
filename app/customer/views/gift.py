# coding=utf-8
import json
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from app.customer.models.gift import Gift
from app.customer.common_util.image import UploadImage

@login_required()
def gift_list(request):
    gifts = Gift.objects.filter(status=Gift.STATUS_USING).order_by('seq')
    return render(request, 'gift/list.html', {'gifts': gifts})


# 创建或修改
@login_required()
def gift_edit(request):
    if request.method == 'POST':
        print '2222222'
        #get params
        qd = request.POST
        price = qd.get('price', '')
        ticket = qd.get('ticket', '')
        status = qd.get('status', 0)
        gift_id = qd.get('gift_id', "")
        gift_name = qd.get('gift_name', '')
        experience = qd.get('experience', '')
        continuity = qd.get('continuity', '')
        animation_type = qd.get('animation_type', '')
        is_flower = qd.get('is_flower', 0)
        logo = qd.get('logo')
        gift_type = qd.get('gift_type')
        wealth_value = qd.get('wealth_value')
        charm_value = qd.get('charm_value')
        # logo_file_obj = request.FILES[u"files[]"]
        # print request.FILES
        # u = UploadImage(logo_file_obj)
        # data = u.push_to_qclude()
        # print data
        # logo = data.get('data')['download_url']
        if not gift_id:
            #create
            Gift.create(
                gift_name, price, experience,
                ticket, continuity, animation_type,
                logo, is_flower,gift_type,wealth_value,charm_value
            )
        else:
            #update
            Gift.update(
                gift_id, gift_name, price, experience,
                ticket, continuity, animation_type,
                logo, is_flower,gift_type,wealth_value,charm_value
            )
        return HttpResponseRedirect(reverse("gift_list"))

    else:
        print '111111'
        qd = request.GET
        gift_id = qd.get('gift_id', "")
        gift = ''
        if gift_id:
            gift = Gift.objects.get(id=gift_id)
        return render(request, 'gift/edit.html', {'gift': gift,})


@login_required
def gift_position(request):
    position = request.POST.get('gift_ids')
    gift_ids = [int(i) for i in position.split(',')]
    seq_map = {}

    for i in range(1, len(gift_ids)+1):
        seq_map[gift_ids[i-1]] = i

    gifts = Gift.objects.filter(status=Gift.STATUS_USING)

    for g in gifts:
        g.seq = seq_map.get(g.id)
        g.save()
    response = {'status': 'success'}
    return HttpResponse(json.dumps(response), content_type="application/json")

@login_required()
def gift_delete(request):
    gift_id = request.GET.get('gift_id', "")
    gift = Gift.objects.get(id=gift_id)
    gift.status = Gift.STATUS_DELETED
    gift.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


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

        print file_obj.__dict__

        up = UploadImage(file_obj)
        data = up.push_to_qclude()
        print data
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