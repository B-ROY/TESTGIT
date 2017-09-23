#coding=utf-8

from app.customer.models.account import Account
from app_redis.user.models.user import *
from redis_model.redis_client import *
from app.customer.models.user import User


def add_target_user():
    accounts = Account.objects.filter(charge__gt=20000).distinct("User")
    print accounts
    user_ids = map(lambda x: str(x.id), accounts)
    print user_ids
    a = RQueueClient.getInstance().redis.sadd("key_target_user", *user_ids)

def add_pure_user():
    qingcun = "597ef85718ce420b7d46ce11"
    pure_user_ids = User.objects.filter(label__contains=qingcun).distinct("_id")
    a = RQueueClient.getInstance().redis.sadd("key_pure_anchor", *pure_user_ids)