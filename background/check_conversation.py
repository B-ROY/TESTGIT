# -*- coding: utf-8 -*-
import os
import sys

import datetime
PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../push_util')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../..')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../../..')))

from base.settings import load_django_settings

load_django_settings('live_video.base', 'live_video.app')

from app.customer.models.chat import UserConversation
from app.customer.models.tools import UserTools, Tools
from app.util.messageque.msgsender import MessageSender


def check_conversation():
    now = datetime.datetime.now()
    print now.strftime("%Y-%m-%d %H:%M:%S")
    conversations = UserConversation.objects.filter(type__in=[1, 2, 3])
    if not conversations:
        return
    for conversation in conversations:
        if conversation.type == 1:
            #  建立会话(60分钟关闭)
            start_time = conversation.start_time
            if int((now - start_time).total_seconds()) > 3600:
                conversation.update(set__type=4)
                conversation.update(set__stop_time=now)
                conversation.update(set__stop_type=1)

        if conversation.type == 2:
            #  会话未建立(10分钟关闭)
            wait_time = conversation.wait_time
            if int((now-wait_time).total_seconds()) > 600:
                conversation.update(set__type=4)
                conversation.update(set__stop_time=now)
                conversation.update(set__stop_type=1)
                if conversation.is_send_tool == 1:
                    # 返还道具:
                    tool = Tools.objects.filter(tools_type=0).first()
                    db_user_tools = UserTools.objects.filter(user_id=conversation.send_id, tools_id=str(tool.id),
                                             time_type=conversation.tool_time_type).first()
                    time_type = conversation.tool_time_type
                    get_type = 0
                    if time_type == 1:
                        get_type = 2

                    if not db_user_tools:
                        user_tools = UserTools()
                        user_tools.user_id = conversation.send_id
                        user_tools.tools_id = str(tool.id)
                        user_tools.tools_count = 1
                        user_tools.time_type = time_type
                        user_tools.get_type = get_type
                        if time_type == 0:
                            user_tools.invalid_time = now + datetime.timedelta(days=1)
                        user_tools.save()
                    else:
                        db_user_tools.update(inc__tools_count=1)
                    MessageSender.send_return_tool(conversation.from_user_id, conversation.to_user_id, 1)
                    MessageSender.send_return_tool(conversation.to_user_id, conversation.from_user_id, 2)
                    print "close........"
        if conversation.type == 3:
            # 道具解锁状态
            wait_time = conversation.wait_time
            if int((now-wait_time).total_seconds()) > 600:
                conversation.update(set__type=4)
                conversation.update(set__stop_time=now)
                conversation.update(set__stop_type=1)


if __name__ == '__main__':
    check_conversation()











