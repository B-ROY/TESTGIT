# coding=utf-8
from app.customer.models.user import User
from app.customer.models.account import *

def test_index():
    users = User.objects.all()
    start_time = time.time()
    for user in users:
        account = Account.objects.get(user=user)
        a =account.diamond=2
    end_time = time.time()

    print end_time - start_time

