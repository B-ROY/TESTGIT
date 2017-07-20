# coding=utf-8

from django.conf import settings
from api.handler.thridpard.http_request import RequestApi
from api.util.tencenttools.signature import gen_signature
import time
import datetime
import json


def multiaccount_import():
    app_id = settings.QCLOUD_LIVE_SDK_APP_ID
    sig = gen_signature(app_id, "admin")
    random_int = int(time.mktime(datetime.datetime.now().timetuple()))
    #https: // console.tim.qq.com / v4 / im_open_login_svc / account_import?usersig = xxx & identifier = admin & sdkappid = 88888888 & random = 99999999 & contenttype = json

    uri = "/v4/im_open_login_svc/multiaccount_import?usersig=%s&identifier=admin&sdkappid=%s&random=%s&contenttype=json" % (sig, app_id,random_int)

    accounts = []
    for i in range(3100050, 3100081):
        accounts.append(str(i))

    body = {
        "Accounts": accounts
    }

    body = json.dumps(body)
    data = RequestApi.post_body_request(uri, body, headers={}, host='console.tim.qq.com')
    result = json.loads(data)
    print result
    if result.get("ActionStatus") == "OK":
        return True, result
    else:
        return False, "%s:%s" % (result.get("ErrorInfo", ""), result.get("ErrorCode", ""))