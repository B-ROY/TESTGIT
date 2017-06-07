# -*- coding: utf-8 -*-
import os
import sys
import datetime

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "base", "site-packages")))
sys.path.insert(1, os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "base", "site-packages","django_admin_bootstrapped")))

sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../..')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../../..')))

from base.settings import load_django_settings
load_django_settings('live_video.base', 'live_video.app', 'live_video.api')
from api.temp_script.tools_script import *
# 0 0 */1 * * python /mydata/python/live_video/background/statistics.py > /dev/null 2>&1 &

if __name__ == '__main__':
    ClearAndSendTools.clear_send_tools()