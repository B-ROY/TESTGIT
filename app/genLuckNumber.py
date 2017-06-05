#coding=utf-8

from app.customer.models.user import LuckIDInfo
from redis_model.genlucknum import checkLuckNumber


def gen_luck_number():
    count = LuckIDInfo.objects.all().count()
    for n in range(3040001, 31000000):
        strNum = str(n)
        result = checkLuckNumber(strNum)
        if result:
            luck_num = LuckIDInfo(id=count + 1, user_id=strNum, id_type=1, id_level=1,
                                  id_assign=1)
        else:
            luck_num = LuckIDInfo(id=count + 1, user_id=strNum, id_type=0, id_level=0,
                                  id_assign=0)
        luck_num.save()
        count += 1
