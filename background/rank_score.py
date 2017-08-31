# coding=utf-8

import os
import sys

import datetime
from math import log
import random
PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../push_util')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../..')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../../..')))

from base.settings import load_django_settings

load_django_settings('live_video.base', 'live_video.app')

from app.customer.models.community import UserMoment, UserMomentLook


epoch = datetime.datetime(1970, 1, 1)

def epoch_seconds(date):
    """Returns the number of seconds from the epoch to date."""
    td = date - epoch
    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)

def score(ups, downs):
    return ups - downs

def hot(ups, downs, date):
    """The hot formula. Should match the equivalent function in postgres."""
    s = score(ups, downs)
    order = log(max(abs(s), 1), 10)
    sign = 1 if s > 0 else -1 if s < 0 else 0
    seconds = epoch_seconds(date) - 1134028003
    return round(order + sign * seconds / 45000, 7)


def update_rank_score():
    now = datetime.datetime.now()
    start_date = datetime.datetime(now.year, now.month, now.day) - datetime.timedelta(days=7)
    moments = UserMoment.objects.filter(create_time__gte=start_date, create_time__lte=now)
    if not moments:
        return

    for moment in moments:
        like_count = moment.like_count
        moment_look = UserMomentLook.objects.filter(user_moment_id=str(moment.id)).first()
        look_count = 0
        if moment_look:
            look_user_ids = moment_look.user_id_list
            look_count = len(look_user_ids)

        if int(moment.type) == 2 or int(moment.type) == 3:
            ups = like_count*2 + look_count + int(30*(random.random()) + 1)
        else:
            ups = like_count*2 + look_count
        rank_score = hot(ups, 0, moment.create_time)
        moment.update(set__rank_score=rank_score)


if __name__ == '__main__':
    update_rank_score()


# now = datetime.datetime.now()
# result = hot(100, 0, now)
# result2 = hot(100, 0, now)
# result3 = hot(100, 0, now)
# print result
# print result2
# print result3
