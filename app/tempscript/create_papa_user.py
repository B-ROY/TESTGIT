# coding=utf-8

from app.customer.models.user import User
from app.audio.models.record import AudioRoomRecord
import random
import datetime

def create_papa_user():
    for i in range(1,30):

        open_id = "papa_user_" + str(i)
        source = 4
        nickname = "papa_user" + str(i)
        platform = 0
        phone = "12345567" + str(i)
        gender = random.randint(1,2)
        guid = "fake_papa_user" + str(i)

        User.create_user(open_id, source, nickname, platform, phone, gender,guid=guid)


def create_papa_room():
    for i in range(1,30):
        open_id = "papa_user_" + str(i)
        user = User.objects.get(openid=open_id)
        AudioRoomRecord.create_roomrecord(user_id=user.id, open_time=datetime.datetime.now())
