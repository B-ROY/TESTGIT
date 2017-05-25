# -*- coding: utf-8 -*-
import os
import sys
import datetime

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../push_util')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../..')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../../..')))

from base.settings import load_django_settings
from app.cutlog_daily import CutLog

load_django_settings('live_video.base', 'live_video.app')


if __name__ == '__main__':

    time_now = datetime.datetime.now()
    oneday = datetime.timedelta(days=1)
    time_yesterday = time_now - oneday
    time = time_yesterday.strftime('%Y-%m-%d')
    print time
    CutLog.write_orignal_log(time)
