#coding=utf-8

from app.customer.models.user import LuckIDInfo
from redis_model.genlucknum import checkLuckNumber
from app_redis.user.models.user import UserRedis


def gen_luck_number():
    count = LuckIDInfo.objects.all().count()
    identity_list = []
    for n in range(3065000, 3500000):
        strNum = str(n)
        result = checkLuckNumber(strNum)
        print result
        if not result:
            #luck_num = LuckIDInfo(id=count + 1, user_id=strNum, id_type=1, id_level=1, id_assign=1)
            identity_list.append(strNum)

    return identity_list