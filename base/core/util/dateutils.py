#encoding=utf-8
import  datetime, time
import re


def humanreadable_mseconds(mseconds):
    seconds = int(mseconds) / 1000
    s = seconds % 60
    h = seconds / 60 / 60

    if h:
        m = seconds / 60 % 60
        ret = u"%02d:%02d:%02d" % (h,m,s)

    else:
        m = seconds / 60
        ret = u"%02d:%02d" % (m,s)

    return ret


def zero_date():
    d = datetime.datetime.today()
    return datetime.datetime(d.year, d.month, d.day)


def datetime_to_timestamp(d):
    if d:
        return int(time.mktime(d.timetuple()))
    else:
        return 0 


def days_ago(day=30):
    return datetime.datetime.now() - datetime.timedelta(day)


def nature_days_ago(day=30):
    return zero_date() - datetime.timedelta(day)


def after_days(day=30):
    return datetime.datetime.now() + datetime.timedelta(day)


def nature_after_days(day=30):
    return zero_date() + datetime.timedelta(day)


def seconds_to_zero():
    d = nature_after_days(1)
    return int(datetime_to_timestamp(d) - int(time.time()))


def is_weekend(d=datetime.datetime.today()):
    return d.weekday() in (0, 6)


def minutes_ago(seconds=300):
    return datetime.datetime.now() - datetime.timedelta(seconds=seconds)


def after_minutes(seconds=300):
    return datetime.datetime.now() + datetime.timedelta(seconds=seconds)


def int_day(d=None):
    if d is None:
        d = datetime.datetime.today()
    return int("%s%d%d" % (d.year,d.month, d.day))

def int_days(d=None):
    if d is None:
        d = datetime.datetime.today()
    return int("%s%02d%02d" % (d.year,d.month, d.day))


def int_month(d=None):
    if d is None:
        d = datetime.datetime.today()
    return int("%s%d" % (d.year, d.month))


def int_week(d=None):
    if d is None:
        d = datetime.datetime.today()

    monday = d.weekday()
    d = d - datetime.timedelta(monday)

    return int("%s%d%d" % (d.year, d.month, d.day))


def int_weeks(d=None):
    if d is None:
        d = datetime.datetime.today()

    monday = d.weekday()
    d = d - datetime.timedelta(monday)

    return int("%s%02d%02d" % (d.year, d.month, d.day))


def is_legal_date(d):
    timere = "^(\d{2}|\d{4})-((0([1-9]{1}))|(1[0|1|2]))-(([0-2]([0-9]{1}))|(3[0|1]))$"
    return re.match(timere, d) != None
