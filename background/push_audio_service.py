# -*- coding: utf-8 -*-
import os
import sys

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../push_util')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../..')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../../..')))

from base.settings import load_django_settings

load_django_settings('live_video.base', 'live_video.app')
from redis_model.queue import Worker
from push_util.list_push import *

from app.customer.models.user import *
import traceback


def do_push(data):
    # print "**Recieve data: ", data
    #logging.error(data)
    # ...... todo data.get("user_id")
    print datetime.datetime.now() + "     " + data
    user_id = int(data.get("user_id"))
    user = User.objects.get(id=user_id)
    host_id = int(data.get("host_id"))
    audio_room_id = data.get("audio_room_id")

    title = ""
    desc =  user.nickname + u" 正在请求与您进行情感连线，快来接听吧！"
    content_dic = {'title': "",
                   'content': user.nickname + u" 正在请求与您进行情感连线，快来接听吧！",
                   'type': 0,
                   'user_id': int(user_id),
                   'host_id': int(host_id),
                   'audio_room_id': audio_room_id}

    content = json.dumps(content_dic)

    print content_dic

    host = User.objects.get(id=host_id)
    if not host.cid:
        print "host cid is none    host id is " + str(host.id)
        return
    try:
        push_message_to_list(title, desc, content, host.cid, host.app_name, host.platform, host.osver)
    except Exception, e:
        logging.error("send audio message erro " + format(e))

    """过往代码 留作参考
    if android_arr:
        pushMessageToList(title, desc, content, android_arr, _type='android')
    if ios_arr:
        pushMessageToList(title, desc, content, ios_arr, _type='ios')
    if ios_82_arr:
        pushMessageToList(title, desc, content, ios_82_arr, _type='ios82')
    """


if __name__ == "__main__":
    worker = Worker("do_push.audio")
    try:
        worker.register(do_push)
        worker.start()
    except KeyboardInterrupt:
        worker.stop()
        print "exited cleanly"
        sys.exit(1)
    except Exception, e:
        print e

