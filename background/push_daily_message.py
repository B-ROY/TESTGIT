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

def do_push(data):
    desc = data.get("message_desc")
    message_type = data.get("message_type", 0)

    users = User.objects.filter(user_type=0, gender=message_type)
    for user in users:
        title = ""
        content_dic = {'title': "",
                       'content': desc,
                       'type': 0,
                       'host_id': int(user.id),}

        content = json.dumps(content_dic)

        host = User.objects.filter(id=user.id)
        (android_arr, ios_arr, ios_82_arr) = target_list(host)
        print android_arr, ios_arr, ios_82_arr
        if android_arr:
            pushMessageToList(title, desc, content, android_arr, _type='android')
        if ios_arr:
            pushMessageToList(title, desc, content, ios_arr, _type='ios')
        if ios_82_arr:
            pushMessageToList(title, desc, content, ios_82_arr, _type='ios82')


if __name__ == "__main__":
    worker = Worker("do_push.daily_message")
    try:
        worker.register(do_push)
        worker.start()
    except KeyboardInterrupt:
        worker.stop()
        print "exited cleanly"
        sys.exit(1)
    except Exception, e:
        print e

