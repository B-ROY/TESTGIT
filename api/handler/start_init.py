#coding=utf-8

from api.document.doc_tools import *
from api.view.base import BaseHandler
from app.customer.models.startup_image import StartupImage
from app.customer.models.switch import Switcher
from app.customer.models.version_info import VersionInfo
import time
from app.customer.models.user import UserHeartBeat

@handler_define
class Initial(BaseHandler):
    @api_define("Initial", r'/app/inital', [
        Param('platform', True, str, "", "", u'IOS,ANDROID,H5,WEB'),
    ], description="初始化接口")
    def get(self):
        obj = StartupImage.objects.filter(status=StartupImage.STATUS_VALID).first()
        if obj:
            data = {'id': obj.key, 'image': obj.image, 'url': obj.url}
        else:
            data = {}
        switches = {}
        platform = self.arg("platform")
        ua = self.request.headers.get('User-Agent')

        # 开关规则 0不处理 1开启
        switch_on = Switcher.get_on_switches(platform)
        for switch in switch_on:
            status = switch.status
            if status.isdigit():
                status = int(status)
            switches[switch.name] = status
        
        # upgrade_type 0不做处理 1强升 2非强生
        version_info = {
            'version': '',
            'upgrade_type': '',
            'download_url': '',
            'desc': '',
        }
        app_name = ua.split(";")[0]
        uas = ua.split(";")
        if uas[2] == "iPhone" or uas[2] == "iPad":
            channel = None
        else:
            channel = uas[5]

        version = VersionInfo.get_version_info(platform, app_name, channel)
        if version:
            version_info = version.format_version_info()

        ua_version = ua.split(";")[1]
        if version and ua_version > version.version:
            switches["review"] = 0
        else:
            switches["review"] = 1

        if platform.upper() == 'ANDROID' and ua_version < "2.2.1":
            if channel == "chatpa" or channel == "600009":
                channel = "600000"
            version_info["upgrade_type"] = 1
            version_info["version_code"] = 300
            downloads_url = "http://heydo-10048692.file.myqcloud.com/android_apk/chatpa2.2.1_" + channel + ".apk"
            version_info["download_url"] = downloads_url
            version_info["desc"] = "亲爱的女神、男神：您好！为了给大家提供更好的服务，我们将现有版本升级，新版特性：\n" \
                                   "\n" \
                                   "优化了视频显示效果；\n" \
                                   "VIP功能上线，享受更多特权。\n" \
                                   "增加支付宝支付"

        share_url = "http://www.qqzwq.cn/share/"
        invite_url = "http://www.qqhqf.cn/invite/liaopa_invite.html"

        self.write({
            'status': "success",
            'start_image': data,
            "system_timestamp": int(time.time()),
            "switch": switches,
            "version_info": version_info,
            "report_interval": UserHeartBeat.REPORT_INTERVAL,
            "share_url": share_url,
            "invite_url": invite_url
        })
