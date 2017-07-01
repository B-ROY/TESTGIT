# coding=utf-8

from app.customer.models.user import User, UserInviteCode
from app.customer.models.account import TicketAccount

def find_repeated_ticket_account(user_id):

    user = User.objects.get(id=user_id)

    user_ids = UserInviteCode.objects.filter(invite_id=user.id).distinct("user_id")

    for u_id in user_ids:
        user = User.objects.get(id=u_id)
        count = TicketAccount.objects.filter(user=user).count()
        if count!=1:
            print u_id


