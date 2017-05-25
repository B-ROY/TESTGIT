# coding=utf-8

from mongoengine import *
import datetime
from app.customer.common_util import image
import logging
from app.audio.models.record import AudioRoomRecord

class PornCheckItem(Document):

    DELETE_STATUS = [
        (0, "默认状态"),
        (1, "删除失败")
    ]
    pic_url = StringField(verbose_name=u"疑似图片url")
    file_id = StringField(verbose_name=u"图片在万象优图的file_id")
    room_id = StringField(verbose_name=u"房间id")
    user_id = IntField(verbose_name=u"房主id")
    join_id = IntField(verbose_name=u"用户id")
    upload_time = DateTimeField(verbose_name=u"上报时间")
    pic_delete_status = IntField(verbose_name=u"是否删除成功", choices=DELETE_STATUS)



    @classmethod
    def create_item(cls, pic_url, file_id, room_id, user_id, join_id, delete_status=0):
        obj_ = cls(pic_url=pic_url, room_id=room_id, file_id=file_id,
                   user_id=user_id, join_id=join_id, upload_time=datetime.datetime.now(), delete_status=delete_status)
        obj_.save()

    def delete_item(self):
        data = image.delete_pic(self.file_id)
        if data["code"] == 0:
            self.delete()
        else:
            self.update(set__pic_delete_status=1)
            logging.error()

    @classmethod
    def porn_check(cls, pic_url, file_id, room_id, user_id, join_id):
        data = image.porncheck(pic_url)
        result_data = data.get("result_list")[0].get("data")

        if result_data.get("result") == 0 and result_data.get("confidence") < 50:
            data = image.delete_pic(file_id)
            if data["code"] != 0:
                cls.create_item(pic_url, file_id, room_id, user_id, join_id, 1)
        else:
            # 黄图或疑似图片
            cls.create_item(pic_url, file_id, room_id, user_id, join_id)
            # todo 加入短信报警
            pass

    @classmethod
    def close_room_for_porn(cls, item_id):
        item = cls.objects.get(id=item_id)
        AudioRoomRecord.close_room_for_porn(item.room_id)

    @classmethod
    def ignore_porn_check_item(cls, item_id):
        item = cls.objects.get(id=item_id)
        item.delete_item()


