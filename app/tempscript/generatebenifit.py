#coding=utf-8

from app.customer.models.benifit import *
from app.customer.models.user import *
import datetime
from app.customer.models.account import *


def generate_with_draw_bonus_ratio():
    """
    添加规则

    """
    ratio_1 = WithdrawBonusRatio()
    ratio_1.user_type = 0
    ratio_1.ratio = 0.6
    ratio_1.save()
    ratio_2 = WithdrawBonusRatio()
    ratio_2.user_type = 100 #工会老大
    ratio_2.ratio = 1.0
    ratio_2.save()


def generate_benifit(start_time, end_time):
    users = User.objects(created_at__gte=start_time, created_at__lt=end_time)
    for user in users:
        ticket_account = TicketAccount()
        ticket_account.user = user
        ticket_account.total_ticket = 0
        ticket_account.gift_ticket = 0
        ticket_account.call_ticket = 0
        ticket_account.friend_charge_ticket = 0
        ticket_account.friend_benifit_ticket = 0
        ticket_account.money = 0
        ticket_account.ticket_requesting_withdraw = 0
        ticket_account.money_withdrawed = 0
        ticket_account.last_ticket = 0
        ticket_account.bonus_ticket = 0
        ticket_account.update_time = datetime.datetime.now()
        ticket_account.save()

def accounting_charge(start_time, end_time):
    users = User.objects.filter(created_at__gte=start_time, created_at__lt=end_time)
    accounts = Account.objects.filter(user__in=users, )
    for account in accounts:
        print account.user.id
        invite_record = UserInviteCode.objects.filter(user_id=account.user.id).first()
        if invite_record and invite_record.invite_id!=0:
            invite_user = User.objects.get(id=invite_record.invite_id)
            ticket_account = TicketAccount.objects.get(user=invite_user)
            ticket_account.total_ticket += account.charge * 0.1
            ticket_account.friend_charge_ticket += account.charge*0.1
            ticket_account.money += account.charge*0.1*0.6
            ticket_account.save()


def accounting_withdraw(start_time, end_time):
    withdraw_reqeusts = WithdrawRequest.objects(request_time__gte=start_time, request_time__lt=end_time)
    for withdraw_reqeust in withdraw_reqeusts:
        print withdraw_reqeust.id
        if withdraw_reqeust.status==0 or withdraw_reqeust.status==4:
            user = User.objects.get(id=withdraw_reqeust.user_id)
            user_ticket_account = TicketAccount.objects.get(user=user)
            user_ticket_account.money_requesting += withdraw_reqeust.request_money
            user_ticket_account.save()
        elif withdraw_reqeust.status==2:
            user = User.objects.get(id=withdraw_reqeust.user_id)
            user_ticket_account = TicketAccount.objects.get(user=user)
            user_ticket_account.money_withdrawed += withdraw_reqeust.request_money
            user_ticket_account.save()



def accounting_ticket_record(start_time,end_time):

    ticket_records = TradeTicketRecord.objects(created_time__gte=start_time, created_time__lt=end_time)
    # 拿到邀请人提成比例
    withdraw_ratios = WithdrawBonusRatio.objects.all()
    ratios = {}

    for ratio in withdraw_ratios:
        ratios[ratio.user_type] = ratio.ratio

    num = 0

    for ticket_record in ticket_records:
        num += 1
        print num
        print ticket_record.id
        user_id = ticket_record.user.id
        user = User.objects.get(id=user_id)
        ticket_account = TicketAccount.objects.get(user=user)
        ticket_account.last_ticket = ticket_account.total_ticket
        ticket_account.update_time = ticket_record.created_time
        ticket_account.total_ticket += ticket_record.ticket
        ticket_account.money += ticket_record.ticket*0.6
        if ticket_record.trade_type == TradeTicketRecord.TradeTypeGift:
            ticket_account.gift_ticket += ticket_record.ticket
            pass
        elif ticket_record.trade_type == TradeTicketRecord.TradeTypeAudio:
            ticket_account.call_ticket += ticket_record.ticket
            pass
        # computer the Inviter 的收益
        invite_record = UserInviteCode.objects.filter(user_id=user_id).first()
        if invite_record:
            invite_user = User.objects.get(id=invite_record.invite_id)
            invite_ticket_account = TicketAccount.objects.get(user=invite_user)
            invite_ticket_account.last_ticket = ticket_account.total_ticket
            invite_ticket_account.update_time = ticket_record.created_time
            invite_ticket_account.total_ticket += ticket_record.ticket * 0.1
            invite_ticket_account.friend_benifit_ticket += ticket_record.ticket*0.1
            invite_ticket_account.money += ticket_record.ticket * 0.1 * ratios[invite_user.user_type]
            invite_ticket_account.save()
        ticket_account.save()


def generate_new_ticket():
    start_time = datetime.datetime(2017, 4, 23, 0, 40, 0)
    end_time = datetime.datetime(2017, 4, 23, 1, 18, 0)

    generate_benifit(start_time, end_time)
    accounting_ticket_record(start_time, end_time)

    pass



if __name__ == "__main__":
    generate_new_ticket()



def test_ticket():
    users = User.objects.all()
    num = 0
    error_num = 0
    no_0_num = 0

    for user in users:
        ticket_account = TicketAccount.objects.get(user=user)
        if user.ticket != 0 or ticket_account.gift_ticket + ticket_account.call_ticket != 0:
            no_0_num += 1
        if user.ticket != int(ticket_account.gift_ticket + ticket_account.call_ticket):
            print user.id
            print "user ticket is " + str(user.ticket) + " new ticket is " + str(int(ticket_account.gift_ticket + ticket_account.call_ticket))
            error_num += 1

    print "error num is " + str(error_num)
    print "no_0_num si " + str(no_0_num)


def test_diamond_ticket():
    users = User.objects.all()

    start_date = datetime.datetime(2017, 1, 20)
    time_delta = datetime.timedelta(days=1)
    end_date = datetime.datetime(2017, 4, 22)

    d = start_date
    ne_day =[]
    while d <= end_date:
        print d
        next_d = d + time_delta
        gift_diamond_record = TradeDiamondRecord.objects.filter(trade_type=1, created_time__gt=d, created_time__lt=next_d)
        gift_ticket_record = TradeTicketRecord.objects.filter(trade_type=0,created_time__gt=d, created_time__lt=next_d)

        gift_diamond = 0
        gift_ticket = 0
        for record in gift_diamond_record:
            gift_diamond += record.diamon
        for record in gift_ticket_record:
            gift_ticket += record.ticket

        print "gift diamond record count is " + str(gift_diamond_record.count()) + " gift ticket record count is " + str(gift_ticket_record.count())
        print "gift diamond is " + str(gift_diamond) + " gift_ticket is " + str(gift_ticket)
        audio_diamond_record = TradeDiamondRecord.objects.filter(trade_type=2, created_time__gt=d, created_time__lt=next_d)
        audio_ticket_record = TradeTicketRecord.objects.filter(trade_type=2, created_time__gt=d, created_time__lt=next_d)

        audio_diamond = 0
        audio_ticket = 0
        for record in audio_diamond_record:
            audio_diamond += record.diamon
        for record in audio_ticket_record:
            audio_ticket += record.ticket
        print "audio diamond is " + str(audio_diamond) + "  " + str(audio_ticket)
        print "audio diamond record count is " + str(audio_diamond_record.count()) + " aduio ticket record count is " + str(audio_ticket_record.count())
        print " "
        if gift_diamond_record.count() != gift_ticket_record.count() or audio_diamond_record.count() != audio_ticket_record.count() or gift_diamond != gift_ticket or audio_diamond != audio_ticket:
            ne_day.append(d)
        d = next_d

    print ne_day



def test_user_ticket(user_id, start_time, end_time):
    start_time = datetime.datetime(2017, 1, 20)
    time_delta = datetime.timedelta(days=1)
    end_time = datetime.datetime(2017, 4, 23)
    user = User.objects.get(id=user_id)
    ticket_records = TradeTicketRecord.objects(created_time__gte=start_time, created_time__lt=end_time,user=user)
    total_ticket = 0
    for record in ticket_records:
        total_ticket += record.ticket

    print total_ticket













