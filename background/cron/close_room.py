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

from app.audio.models.roomrecord import RoomRecord
from app.customer.models.user import User
import logging
import datetime


def close_room():
    # 查询未关闭的房间
    rooms = RoomRecord.objects.filter(room_status=1)
    now_ = datetime.datetime.now()
    time_delta = datetime.timedelta(seconds=180)
    end_type = 0
    for room in rooms:
        need_close = False
        if room.report_time_user is not None and room.report_time_join is not None:
            if now_ - room.report_time_user > time_delta or now_ - room.report_time_join > time_delta:
                if room.report_time_join > room.report_time_user:
                    end_type = 6
                else:
                    end_type = 3
                need_close = True
        else:
            if room.start_time is not None:
                if now_ - room.start_time > time_delta:
                    need_close = True
            else:
                if now_ - room.create_time > time_delta:
                    need_close = True
            if room.report_time_user is None and room.report_time_join is not None:
                end_type = 6
            elif room.report_time_user is not None and room.report_time_join is None:
                end_type = 3

        if need_close:
            room.update(set__room_status=2, end_type=end_type)
            join_user = User.objects.get(id=room.join_id)
            room_user = User.objects.get(id=room.user_id)
            if join_user.last_room_id == str(room.id):
                join_user.update(set__audio_status=2)
            if room_user.last_room_id == str(room.id):
                room_user.update(set__audio_status=2)
            logging.info("%s:%s" % ("close", room.id))
            print join_user.id, room_user.id





if __name__ == "__main__":
    close_room()










