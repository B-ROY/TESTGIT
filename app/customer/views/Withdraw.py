#coding=utf-8
from app.customer.models.account import *
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse


def WithdrawHandler(request):
    Withdraws = WithdrawRequest.objects.all().order_by('user_id')

    return render(request,'account/Withdraw.html',{'Withdraws':Withdraws})


def chooseHandler(request):
    kw_num = request.GET.get('real_kw')
    orderID = request.GET.get('order_id')
    kw_num = int(kw_num)
    if kw_num==3:
        return render(request,'account/withdraw_refuse.html',{'orderID':orderID})
    # return HttpResponse('ok')



def refuseHandler(request):
    orderID = request.GET.get('order_id')
    refuse_reason = request.POST.get('edit_refuse')
    try:
        WithdrawRequest.reject_withdraw_request(orderID,refuse_reason)
        return HttpResponseRedirect(reverse("WithdrawHandler"))

    except Exception as e:
        print e
        return False



