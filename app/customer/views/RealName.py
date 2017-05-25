#coding=utf-8
from app.customer.models.user import *
from django.shortcuts import render



def RealNameHandler(request):
    RealNames = RealNameVerify.objects.all().order_by('user_id')

    return render(request,'user/realName.html',{'RealNames':RealNames})


def Statue_edit(request):
    user_id = request.GET.get('user_id')
    user = RealNameVerify.objects.get(pk=user_id)
    
    if request.method == "GET":
        return render(request, 'user/realName_edit.html',
            {'user': user})
    else:
        qd = request.POST
        status = qd.get('edit_status')
        feedback = qd.get('edit_feedback')
        status = int(status)
        user.status = status
        user.feedback_reason = feedback
        user.save()

        RealNames = RealNameVerify.objects.all().order_by('user_id')
        return render(request,'user/realName.html',{'RealNames':RealNames})

