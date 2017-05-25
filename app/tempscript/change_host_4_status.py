# coding=utf-8
from app.customer.models.user import *
from app.audio.models.record import AudioRoomRecord
"""
修改主播 离线状态
将所有主播的房间状态4 改成1
"""


def chang_host_status():
    users = User.objects.filter(is_video_auth=1)
    count = 0
    h_count = 0

    for user in users:

        room_id = user.audio_room_id
        if not room_id:
            continue
        room = AudioRoomRecord.objects.get(id=room_id)
        if room.status == 4:
            count += 1
            room.status = 1
            room.save()
            hearbeat = UserHeartBeat.objects.get(user=user)
            if hearbeat.last_report_time > int(time.time())-22*60*60:
                h_count += 1

    print count
    print h_count
