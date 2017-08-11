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
from app.customer.models.real_video_verify import RealVideoVerify


@handler_define
class RealVideoVerifyUpload(BaseHandler):
    @api_define("real video upload", "/video/upload_verify", [
                    Param("cover_url", True, str, "", "", u"封面地址"),
                    Param("video_url", True, str, "", "", u"视频地址"),
                ], description=u"视频认证上传")
    @login_required
    def get(self):
        cover_url = self.arg("cover_url")
        video_url = self.arg("video_url")
        user_id = self.current_user_id
        video_verify = RealVideoVerify()
        now = datetime.datetime.now()
        video_verify.user_id = int(user_id)
        video_verify.cover_url = cover_url
        video_verify.video_url = video_url
        video_verify.feedback_reason = ""
        video_verify.create_time = now
        video_verify.update_time = now
        video_verify.status = 0
        video_verify.is_valid = 1
        video_verify.save()

        self.write({"status": "success"})


@handler_define
class GetVODSign(BaseHandler):
    @api_define("get vod sign", "/video/get_vod_sign",
                [], description=u"获取云点播签名")
    def get(self):
        secret_id = "AKIDrgKznR0CqJbi5If9uUt6A5pNlyrfttGe"
        secret_key = "Vq03vb8WntnVL3e3HPMAvY2LTPBpIG9w"

        time1 = int(time.time())
        time2 = int(time.time()) + 3600
        original = "secretId=%s&currentTimeStamp=%d&expireTime=%s&random=%d" % \
                   (secret_id, time1, time2, random.randint(0, 1000000))

        sign_temp = hmac.new(secret_key, original, hashlib.sha1).digest()
        sign = base64.b64encode(sign_temp + original)
        self.write({"status": "success", "sign": sign})

