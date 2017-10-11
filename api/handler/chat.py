# coding=utf-8


from api.document.doc_tools import *
from api.view.base import *
from api.convert.convert_user import *
import hashlib
import hmac
import base64
import random
import time
import datetime
from app.customer.models.chat import ChatMessage, UserConversation
from app.util.shumeitools.shumeitools import *
import international


@handler_define
class ChatMessageCreate(BaseHandler):
    @api_define("chat message create", "/chat/create", [
                    Param("to_user_id", True, str, "", "", u"接收消息用户id"),
                    Param("type", True, str, "", "", u"1:文本  2:图片  3:音频"),
                    Param("content", False, str, "", "", u"消息内容"),
                    Param("resource_url", False, str, "", "", u"资源地址"),
                    Param("conversation_id", True, str, "", "", u"会话id"),
                ], description=u"聊天信息创建")
    @login_required
    def get(self):
        data = {}
        user = self.current_user
        from_user_id = self.current_user_id
        to_user_id = self.arg("to_user_id")
        type = self.arg_int("type")
        content = self.arg("content", "")
        resource_url = self.arg("resource_url", "")

        user_ip = self.user_ip

        # 本会话第一次发聊天信息, 开始 "十分钟" 倒计时
        conversation_id = self.arg("conversation_id", "")
        status, create_time, con_id, message = ChatMessage.create_chat_message(from_user_id, to_user_id, type, content, conversation_id, resource_url, user_ip)

        if status == 2:
            # 文本鉴黄
            return self.write({'status': "fail",
                               'error': _(message)})
        if status == 1:
            temp_time = create_time.strftime("%Y-%m-%d %H:%M:%S")
            timeArray = time.strptime(temp_time, "%Y-%m-%d %H:%M:%S")
            # 转换成时间戳
            timestamp = time.mktime(timeArray)
            data["create_time"] = int(timestamp)

        # data["conversation_id"] = con_id

        self.write({"status": "success", "data": data})


@handler_define
class ChatCancel(BaseHandler):
    @api_define("chat cancel", "/chat/cancel", [
        Param("to_user_id", True, str, "", "", u"接收消息用户id"),
        Param("conversation_id", True, str, "", "", u"会话id"),
    ], description=u"聊天结束,取消")
    @login_required
    def get(self):
        from_user_id = self.current_user_id
        to_user_id = self.arg("to_user_id")
        conversation_id = self.arg("conversation_id")
        # android 可能出现 conversation_id 为 null的情况
        if conversation_id == "null":
            return self.write({"status": "fail"})
        if not to_user_id or not conversation_id:
            return self.write({"status": "success"})
        UserConversation.cancel(conversation_id, from_user_id, to_user_id)
        return self.write({"status": "success"})
