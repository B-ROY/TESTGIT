# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from app.audio.models.pushRecord import *
from app.audio.im.qcloud.imHandler import *
from random import randint
from app.customer.models.user import *
import datetime


def PushRecord(request):
    records = pushMsg.objects.all()

    return render(request,'pushRecord.html',{'records':records})



def Push(request):
    if request.method == 'GET':


        return render(request,'push.html')

    else:
        qb = request.POST
        pushID = qb.get('pushUser')
        pushID = str(pushID)
        recvID = qb.get('recvUser')
        content = qb.get('content')
        randnum = randint(10000000,99999999)
        user = User.objects.get(identity=recvID)
        sid = user.id
        sid = str(sid)
        response = QCloudIM.message_in_push(pushID,sid,randnum,content)
        print response
        if response:
            print '===enter 1===='
            print response
            push = pushMsg(Pushor=pushID,Receiver=sid,Message_type=1,content=content,pushStatus='发送成功')
            push.save()

            records = pushMsg.objects.all()

            return render(request,'pushRecord.html',{'records':records})


        else:
            print '===enter 2===='
            return HttpResponse('push messge wrong')



