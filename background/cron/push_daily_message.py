# -*- coding: utf-8 -*-
import os
import sys

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../..')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../../..')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../../../..')))

from base.settings import load_django_settings

load_django_settings('live_video.base', 'live_video.app')
from redis_model.queue import Worker

from app.customer.models.push import *
import time
import logging
import datetime

def do_close():
    PushMessage.push_daily_message()

if __name__ == "__main__":
    do_close()


