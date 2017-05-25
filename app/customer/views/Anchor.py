#coding=utf-8
from app.customer.models.hotAnchor import *
from django.shortcuts import render
from app.customer.models.user import *
from django.http import HttpResponse, HttpResponseRedirect
import datetime


def AnchorHandler(request):
    Anchors = Anchor.objects.all()

    return render(request,'user/hotAnchorList.html',{'Anchors':Anchors})


def AnchorShow(request):
    try:
        uid = request.GET.get('user_id')
        user = User.objects.get(id=uid)
        image = user.image
        nichName = user.nickname
        is_block = user.is_block
        identity = user.identity
        phone = user.phone
        is_video_auth = user.is_video_auth
        gender = user.gender
        source = user.source
        desc = user.desc
        InfoList = {'image':image,'nichName':nichName,'is_block':is_block,'identity':identity,'phone':phone,'is_video_auth':is_video_auth,'gender':gender,'source':source,'desc':desc}

        return render(request,'user/AnchorInfo.html',InfoList) 

    except Exception as e:
        return HttpResponse('NO Anchor Exit')


def change(request):
    aid = request.GET.get("anchor_id")
    try:
        anchor = Anchor.objects.get(pk=aid)
        if request.method == 'GET':
            sid = anchor.sid
            identity = anchor.identity
            nickname = anchor.nickname
            InfoList = {'sid':sid,'identity':identity,'nickname':nickname,'aid':aid}

            return render(request,'user/anchorChange.html',InfoList)

        else:
            qb = request.POST
            sid = qb.get('edit_sid')
            identity = qb.get('edit_identity')
            nickName = qb.get('edit_nickName')
            anchor.sid = int(sid)
            anchor.identity = int(identity)
            anchor.nickname = nickName
            anchor.save()

            Anchors = Anchor.objects.all()

            return render(request,'user/hotAnchorList.html',{'Anchors':Anchors})



    except Exception as e:
        print e
        return HttpResponse('NO Anchor Exit')


def add_anchor(request):
    anchor_id = request.GET.get('anchor_id')
    anchor_id = int(anchor_id)
    user = User.objects.get(pk=anchor_id)
    identity = user.identity
    ident = int(identity)
    nickname = user.nickname
    anchor = Anchor(sid = anchor_id,identity = ident,nickname = nickname)
    anchor.save()

    Anchors = Anchor.objects.all()

    return render(request,'user/hotAnchorList.html',{'Anchors':Anchors})


def delete_anchor(request):
    aid = request.GET.get('anchor_id')
    anchor = Anchor.objects.get(pk=aid)
    anchor.delete()

    Anchors = Anchor.objects.all()

    return render(request,'user/hotAnchorList.html',{'Anchors':Anchors})





