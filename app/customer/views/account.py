# coding=utf-8

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from app.customer.models.account import *
from app.customer.models.user import *
from app.customer.common_util.page import Pages
from django.contrib import messages
from app.customer.models.platform import *
from app.customer.models.fillin import *

from datetime import datetime

@login_required()
def account(request):
    # levels = .objects.filter(status=1).order_by('grade')
    qd = request.GET
    user_id = qd.get("user_id")
    #user_id = request.GET.get('user_id')
    print " **** " ,user_id
    user = User.objects.get(id=int(user_id))
    
    account = Account.objects.get(user=user)
    #account = Account.objects.filter(user_id=int(user_id))

    orders = TradeBalanceOrder.objects.filter(
        user=user).order_by('-buy_time')[0:10]
    #query
    records = TradeDiamondRecord.objects.filter(
        user=user).order_by('-created_time')[0:10]

    # withdraws = WithdrawBalanceOrder.objects.filter(
    #     user=user).order_by("-withdraw_time")[0:10]

    return render(request, 'account/account.html', {
        'user': user,
        'account': account,
        'orders': orders,
        'records': records,
        # 'withdraws': withdraws,
        'PLATFORM_DICT': TradeBalanceOrder.PLATFORM_DICT,
        'FILL_IN_TYPE_DICT': TradeBalanceOrder.FILL_IN_TYPE_DICT,
        'STATUS_PAY_MAP': TradeBalanceOrder.STATUS_PAY_MAP,
        # 'STATUS_DICT': WithdrawBalanceOrder.STATUS_MAP,
    })



@login_required
def more_trade_orders(request):

    #get param
    page = request.GET.get('page')
    user_id = request.GET.get('user_id')
    user = User.objects.get(id=int(user_id))

    #query
    orders = TradeBalanceOrder.objects.filter(
        user=user).order_by('-buy_time')
    #print orders
    #pagination
    pages = Pages(orders, 10)
    try:
        show_orders = pages.pages.page(page)
    except PageNotAnInteger:
        show_orders = pages.pages.page(1)
        page = 1
    except EmptyPage:
        show_orders = pages.pages.page(pages.num_pages)


    return render(
        request, 'account/more_trade_orders.html',
        {'orders': show_orders,
         'pages_to_show': pages.pages_to_show(int(page)),
         'PLATFORM_DICT': TradeBalanceOrder.PLATFORM_DICT,
         'FILL_IN_TYPE_DICT': TradeBalanceOrder.FILL_IN_TYPE_DICT,
         'STATUS_PAY_MAP': TradeBalanceOrder.STATUS_PAY_MAP,
         'extra': '&user_id=%s'%user_id}
         
    )

@login_required
def trade_order_detail(request):
    order_id = request.GET.get('id')
    order = TradeBalanceOrder.objects.get(id=order_id)
    fill_type = ''
    if FillType.to_s(order.fill_in_type) == 'we_chat':
        notice = WeChatFillNotice.objects.filter(out_trade_no=str(order_id)).first()
        fill_type = 'we_chat'
    elif FillType.to_s(order.fill_in_type) == 'apple_pay':
        notice = AppleVerifyResult.objects.filter(out_trade_no=str(order_id)).first()
        fill_type = 'apple_pay'
    else:
        notice = None
    return render(
        request, 'account/trade_order_detail.html',
        {'order': order,
         'notice': notice,
         'fill_type': fill_type,
        'PLATFORM_DICT': TradeBalanceOrder.PLATFORM_DICT,
        'FILL_IN_TYPE_DICT': TradeBalanceOrder.FILL_IN_TYPE_DICT,
        'STATUS_PAY_MAP': TradeBalanceOrder.STATUS_PAY_MAP,}
    )


@login_required
def trade_account_records(request):

    #get param
    page = request.GET.get('page')
    user_id = request.GET.get('user_id')
    user = User.objects.get(id=int(user_id))
    #
    # a = Account.objects.get(user_id=user_id)
    # a.trade_in(10, u'购买引力币', trade_type=1)

    #query
    records = TradeDiamondRecord.objects.filter(
        user=user).order_by('-created_time')
    #pagination
    pages = Pages(records, 10)
    try:
        show_records = pages.pages.page(page)
    except PageNotAnInteger:
        show_records = pages.pages.page(1)
        page = 1
    except EmptyPage:
        show_records = pages.pages.page(pages.num_pages)


    return render(
        request, 'account/trade_account_record.html',
        {'records': show_records,
         'pages_to_show': pages.pages_to_show(int(page)),
         'extra': '&user_id=%s' % user_id,
         'PLATFORM_DICT': TradeBalanceOrder.PLATFORM_DICT,
         'FILL_IN_TYPE_DICT': TradeBalanceOrder.FILL_IN_TYPE_DICT,
        }
    )

@login_required
def with_draw_orders(request):

    #get param
    page = request.GET.get('page')
    key_word = request.GET.get('key_word', '')

    filter_condition = {}
    if key_word:
        if key_word.isdigit():
            filter_condition.update({'user__identity__contains': key_word})
        else:
            filter_condition.update({'user__nickname__contains': key_word})
        records = WithdrawBalanceOrder.objects.filter(**filter_condition).order_by(
            '-withdraw_time')
    else:
        records = WithdrawBalanceOrder.objects.all().order_by(
            '-withdraw_time')

    #pagination
    pages = Pages(records, 10)
    try:
        show_orders = pages.pages.page(page)
    except PageNotAnInteger:
        show_orders = pages.pages.page(1)
        page = 1
    except EmptyPage:
        show_orders = pages.pages.page(pages.num_pages)

    context = {
        'orders': show_orders,
        'pages_to_show': pages.pages_to_show(int(page)),
        'PLATFORM_DICT': TradeBalanceOrder.PLATFORM_DICT,
         'FILL_IN_TYPE_DICT': TradeBalanceOrder.FILL_IN_TYPE_DICT,
         'STATUS_DICT': WithdrawBalanceOrder.STATUS_MAP,
    }

    if key_word:
        context['extra'] = '&key_word=%s' % key_word

    return render(
        request, 'account/with_draw_balance_order.html', context
    )


@login_required
def withdraw_order_detail(request):
    order_id = request.GET.get('id')
    order = WithdrawBalanceOrder.objects.get(id=order_id)
    user = order.user

    return render(
        request, 'account/with_draw_balance_detail.html', {'order': order, 'user': user,
         'PLATFORM_DICT': TradeBalanceOrder.PLATFORM_DICT,
         'FILL_IN_TYPE_DICT': TradeBalanceOrder.FILL_IN_TYPE_DICT,
         'STATUS_DICT': WithdrawBalanceOrder.STATUS_MAP,
        }
    )


@login_required
def allow_withdraw_order(request):
    order_id = request.POST.get('id')
    alipay_order_id = request.POST.get('alipay_order_id')
    alipay_order_image = request.POST.get('image')
    order = WithdrawBalanceOrder.objects.get(id=order_id)
    try:
        order.user.account.withdraw_out_order_pass(order, alipay_order_id, alipay_order_image)
    except Exception, e:
        messages.error(request, e.message)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def dissmiss_withdraw_order(request):
    order_id = request.POST.get('id')
    dismiss_reason = request.POST.get('dismiss_reason', '')
    if dismiss_reason:
        order = WithdrawBalanceOrder.objects.get(id=order_id)
        # order.user.account.withdraw_out_order_dismiss(order_id)
        account = order.user.account
        account.withdraw_out_order_dismiss(order, dismiss_reason)
        return HttpResponseRedirect('/customer/withdraw/orders')
    else:
        messages.error(request, "必须填写驳回申请原因")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#交易规则管理
@login_required
def trade_rule(request):
    qd = request.GET
    rules = TradeBalanceRule.objects.all().order_by('money')
    return render(request, 'account/trade_rule_list.html', {'traderules': rules})

@login_required()
def trade_rule_edit(request):
    if request.method == 'POST':
        qd = request.POST
        trade_rule_id = qd.get('trade_rule_id', "")
        trade_rule_money = qd.get('edit_trade_rule_money', '')
        trade_rule_diamon = qd.get('edit_trade_rule_diamon', '')
        trade_rule_free_diamon = qd.get('edit_trade_rule_free_diamon', '')
        trade_rule_desc = qd.get('edit_trade_rule_desc', '')
        trade_rule_apple_product_id = qd.get('edit_trade_rule_apple_product_id', '')
        trade_rule_platform = int(qd.get('edit_trade_rule_platform', 0))
        trade_rule_trade_type = int(qd.get('edit_trade_rule_trade_type', 0))
        trade_rule_activity_desc = qd.get('edit_trade_rule_activity_desc','')
        if not trade_rule_money or not trade_rule_diamon or not trade_rule_free_diamon:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if not trade_rule_desc:
            trade_rule_desc = '没有说明'
        if not trade_rule_id:
            result = TradeBalanceRule.create(trade_rule_money,
                                             trade_rule_diamon, trade_rule_free_diamon, trade_rule_desc,trade_rule_apple_product_id,trade_rule_trade_type,trade_rule_activity_desc,trade_rule_platform)
        else:
            result = TradeBalanceRule.update(trade_rule_id, trade_rule_money,
                                             trade_rule_diamon, trade_rule_free_diamon, trade_rule_desc,trade_rule_apple_product_id,trade_rule_trade_type,trade_rule_activity_desc,trade_rule_platform)
        return HttpResponseRedirect(reverse("trade_rule"))
    else:
        qd = request.GET
        trade_rule_id = qd.get('trade_rule_id', "")
        current_rule = ''
        if trade_rule_id:
            current_rule = TradeBalanceRule.objects.get(id=trade_rule_id)
        return render(request, 'account/trade_rule_edit.html', {'current_rule': current_rule})
        
@login_required()
def trade_rule_delete(request):
    tr_id = request.GET.get('trade_rule_id', "")
    demand = TradeBalanceRule.do_invalid(tr_id)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/')) 

def withdraw_pass_confirm_form(request):
    order_id = request.GET.get('order_id', '')
    order = WithdrawBalanceOrder()
    if order_id:
        order = WithdrawBalanceOrder.objects.filter(id=order_id).first()
    return render(request, 'account/withdraw_pass_confirm_form.html', {'order': order})

def withdraw_dismiss_form(request):
    order_id = request.GET.get('order_id', '')
    order = WithdrawBalanceOrder()
    if order_id:
        order = WithdrawBalanceOrder.objects.filter(id=order_id).first()
    return render(request, 'account/withdraw_dismiss_form.html', {'order': order})

#后台添加余额
@login_required
def add_balance(request):
    qd = request.GET
    user_id = qd.get("user_id")
    rules = TradeBalanceRule.objects.all().order_by('money')
    return render(request,
                  'account/add_balance.html',
                  {
                      'traderules': rules,
                      'user_id': user_id
                  })

#后台代充值
@login_required
def replace_pay(request):
    qd = request.GET
    user_id = int(qd.get("user_id"))
    amount = int(qd.get('amount'))
    user = User.objects.get(id=user_id)
    trade_type = TradeBalanceOrder.FILL_IN_TYPE_REPLACE

    #创建本地订单
    account = Account.objects.get(user=user)
    order = account.fill_in_create_order(
        money=amount,
        platform=4,
        fill_in_type=trade_type,
        user_agent=u"后台",
        apple_product_id=""
    )
    order.status = TradeBalanceOrder.STATUS_FILL_IN_PAYED
    order.filled_time = datetime.now()
    order.save()

    #充值成功加引力币
    account.diamond += order.diamon
    account.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

#增加经验方式列表
@login_required
def account_experience(request):
    qd = request.GET
    user_id = qd.get("user_id")
    userExperienceTypes = UserExperienceType.objects.filter(status=1)
    return render(request,
                  'account/account_experience.html',
                  {
                      'experiences': userExperienceTypes,
                      'user_id': user_id
                  })

#后台增加经验
@login_required
def operate_experience(request):
    qd = request.GET
    user_id = int(qd.get("user_id"))
    identifier = qd.get('identifier')
    user = User.objects.get(id=user_id)
    ex_type = UserExperienceType.objects.get(identifier=identifier)
    success = ExperienceManage.operate_experience(user, ex_type)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

#苹果验证显示
@login_required
def apple_verify(request):
    search_key = request.GET.get('search_key')
    receipts = AppleVerify.objects.all().order_by('-buy_time')

    for receipt in receipts:
        order = TradeBalanceOrder.objects.get(id=(receipt.out_trade_no))
        receipt.user_id = order.user.identity
        receipt.user_nickname = order.user.nickname
        receipt.buy_time = order.buy_time
        receipt.money = order.money
        receipt.diamon = order.diamon


    return render(request, 'account/apple_verify.html',
            {'receipts': receipts, })
