# coding=utf-8

from background.messagehandler import MessageHandler
from background.settings import MessageType
from app.customer.models.porncheck import PornCheckItem
from app.customer.models.user import User
import logging
from app.util.shumeitools.shumeitools import *
from app.customer.models.shumeidetect import *
import datetime
# from background.tecent_im.qcloud.im import QCloudIM
import time
import math
# from app.customer.models.block_user_device import BlockUserDev


class AuditMessageHandler(MessageHandler):

    HEAD_URL_MALE = "https://hdlive-10048692.image.myqcloud.com/activity_1493191693"
    HEAD_URL_FEMALE = "https://hdlive-10048692.image.myqcloud.com/activity_1493192498"

    porn_messages_list=[
        "据自动鉴黄系统检测，您的行为存在违规行为，请遵守平台绿色运营协议；当自动鉴黄系统连续三次检测到您的违规行为时，系统将会自动给予封号处理，请您爱惜您的账号！",
        "据自动鉴黄系统检测，您的行为存在违规行为，请遵守平台绿色运营协议；当自动鉴黄系统连续三次检测到您的违规行为时，系统将会自动给予封号处理，请您爱惜您的账号！",
        "据自动鉴黄系统检测，您的行为存在违规行为，已超过系统提醒上限，系统自动给予封号处理！"]
    #todo 测试
    intervals = [0 * 60, 3 * 60, 6 * 60]

    EDIT_ERROR_MESSAGE = u"<html><p>尊敬的用户您好，由于您的（昵称/签名/头像/封面）内容涉及违规因素，已被系统自动替换，请依照净网规定重新编辑，敬请谅解</p><html>"

    @classmethod
    def handle_message(cls, message):
        type = message.get("type")
        try:
            if type == 2101:
                cls.handle_porn_check(message)
            elif type == 2111:
                cls.handle_picture_detect(message)
            elif type == 2112:
                cls.handle_text_detect(message)
        except Exception as e:
            logging.error("tecenthandler handle message error " + str(type) + format(e))


    @classmethod
    def handle_porn_check(cls, message):
        # 对图片鉴黄 然后选择删除或者是创建鉴黄记录
        file_id = message.get("file_id")
        pic_url = message.get("pic_url")
        room_id = message.get("room_id")
        user_id = message.get("user_id")
        join_id = message.get("join_id")
        room_user_id = message.get("room_user_id")


        result = PornCheckItem.porn_check(pic_url, file_id, room_id, user_id, join_id, room_user_id)

        print result
        if result:
            #time_list = PornCheckItem.objects.fitlter(room_id=room_id, user_id=user_id, need_delete__ne=1).order_by(
                #"upload_time").distinct("upload_time")
            time_list = PornCheckItem.objects.filter(room_id=room_id, user_id=user_id, need_delete=0).order_by(
                "upload_time").distinct("upload_time")
            times, is_send = cls.check_porn_check_times(time_list)
            if not is_send:
                return
            # 发送im消息
            if times==3:
                close_room = 1
                block_user = 0
                title = u"通知"
                user = User.objects.get(id=user_id)

                #BlockUserDev.add_block_user(user, 999999, block_start=datetime.datetime.now(), block_end=None, status=2,
                #                   reason=u"涉黄", devno=None, created_time=None, update_time=None, block_type=2)
                #user.update(set__is_block=1)
            else:
                close_room = 0
                block_user = 0
                title = u"警告"

            QCloudIM.send_room_porn_message(user_id=user_id, title=title,message= cls.porn_messages_list[times-1],times=times,
                                            close_room=close_room, block_user=block_user)


    @classmethod
    def check_porn_check_times(cls, time_list):
        times = 0
        time_list = map(lambda x: int(time.mktime(x.timetuple())), time_list)
        is_send = False
        temp_time = time_list[0]
        for timme in time_list:
            if math.fabs(timme - temp_time - cls.intervals[times])<5:
                times += 1
                temp_time = timme
                is_send = True
            else:
                is_send = False
            if times == 3:
                break
        return times, is_send


    @classmethod
    def handle_picture_detect(cls, message):

        pic_url = message["pic_url"]
        user_id = message["user_id"]
        pic_channel = message["pic_channel"]

        user = User.objects.get(id=user_id)

        if user.gender == 1:
            sex = user.gender
        else:
            sex = 0

        ret, duration = shumei_image_detect(pic_url=pic_url, timeout=12, user_id=user.id, channel=pic_channel, sex=sex,
                                  phone=user.phone)

        print "logo change ################" + str(ret)
        # todo 格式不正确
        is_pass = 0
        if ret["code"] == 1100:
            if ret["riskLevel"] == "PASS":
                is_pass = 1
            if ret["riskLevel"] == "REJECT":
                is_pass = 0
            if ret["riskLevel"] == "REVIEW":
                # todo +人工审核逻辑
                is_pass = 1

        if is_pass == 0:
            if pic_channel == 1:#封面图片
                user.update(set__cover=user.image)
                QCloudIM.send_system_message(user.id, cls.EDIT_ERROR_MESSAGE)
            elif pic_channel == 2:
                if user.gender==1:
                    url = cls.HEAD_URL_MALE

                else:
                    url = cls.HEAD_URL_FEMALE
                user.update(set__image=url)
                QCloudIM.send_system_message(user.id, cls.EDIT_ERROR_MESSAGE)
            pic_detect = PictureDetect()
            pic_detect.user = user
            pic_detect.pic_channel = pic_channel
            pic_detect.pic_url = pic_url
            pic_detect.created_time = datetime.datetime.now()
            pic_detect.save()



    @classmethod
    def handle_text_detect(cls, message):

        text = message["text"]
        user_id = message["user_id"]
        text_channel = message["text_channel"]
        ip = message["ip"]

        user = User.objects.get(id=user_id)


        ret, duration = shumei_text_spam(text=text, timeout=1, user_id=user.id, channel=text_channel, nickname=user.nickname,
                               phone=user.phone, ip=ip)

        print ret
        is_pass = 0
        if ret["code"] == 1100:
            if ret["riskLevel"] == "PASS":
                is_pass = 1
            if ret["riskLevel"] == "REJECT":
                is_pass = 0
            if ret["riskLevel"] == "REVIEW":
                # todo +人工审核逻辑
                is_pass = 1

        if not is_pass:
            if text_channel==1:
                user.update(set__nickname="爱聊用户" + str(user.identity))
                QCloudIM.send_system_message(user.id, cls.EDIT_ERROR_MESSAGE)
            elif text_channel == 3:
                user.update(set__desc="等待一通电话，连接你我的心。")
                QCloudIM.send_system_message(user.id, cls.EDIT_ERROR_MESSAGE)
            text_detect = TextDetect()
            text_detect.user = user
            text_detect.text_channel = text_channel
            text_detect.text = text
            text_detect.created_time = datetime.datetime.now()
            text_detect.save()
