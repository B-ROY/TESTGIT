# coding=utf-8

from app.customer.models.hotAnchor import Anchor
from app_redis.user.models.hotanchor import HotAnchorRedis
from app.customer.models.user import User, UserHeartBeat
from app.customer.models.personal_tags import UserTags
from app.audio.models.record import AudioRoomRecord
from api.convert.convert_user import *
import time
import json


class HotAnchorRedisScript:

    @classmethod
    def push_hot_anchor(cls):
        """
            push user_id into redis
            key: "user_id"
        """
        anchor_redis = HotAnchorRedis()

        hot_list = []
        now_time = int(time.time())
        pre_time = now_time - 120
        heartbeats = UserHeartBeat.objects.filter(last_report_time__gte=pre_time)
        hots = []
        anchors = Anchor.objects.all()
        hot_ids = []
        for anchor in anchors:
            user = User.objects.get(id=anchor.sid)
            user_heart = UserHeartBeat.objects.get(user=user)
            if user_heart.last_report_time > pre_time and user.disturb_mode != 1:
                hots.append(user)
                hot_ids.append(user.id)

        for heartbeat in heartbeats:
            if heartbeat.user.charm_value > 2500 and heartbeat.user.disturb_mode != 1 \
                    and heartbeat.user.id not in hot_ids:
                hots.append(heartbeat.user)

        if not hots:
            hots = User.objects.all().order_by("-charm_value")[0:4]


        for user in hots:
            room = AudioRoomRecord.objects.get(id=user.audio_room_id)
            personal_tags = UserTags.get_usertags(user_id=room.user_id)
            if not personal_tags:
                personal_tags = []

            dic = {
                "audioroom": convert_audioroom(room),
                "user": convert_user(user),
                "personal_tags": personal_tags,
                "time_stamp": int(time.time())
            }
            hot_list.append(dic)
            user_id_list.append(user.id)
