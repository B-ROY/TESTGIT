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

from app.audio.models.record import *
import time
import logging
import datetime

def do_close():
    page = 1
    rooms = AudioRoomRecord.need_closed_userrooms(page)
    while rooms:
        for room in rooms:
            logging.info("%s:%s" % ("close", room.id))
            room.finish_roomrecord(room_id=str(room.id), end_time=datetime.datetime.now())

        page += 1
        rooms = AudioRoomRecord.need_closed_userrooms(page)

    page = 1
    rooms = AudioRoomRecord.need_closed_joinrooms(page)
    while rooms:
        for room in rooms:
            logging.info("%s:%s" % ("close", room.id))
            room.finish_roomrecord(room_id=str(room.id), end_time=datetime.datetime.now())

        page += 1
        rooms = AudioRoomRecord.need_closed_joinrooms(page)

    AudioRoomRecord.closed_waitingrooms()

if __name__ == "__main__":
    do_close()


