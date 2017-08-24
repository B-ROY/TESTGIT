#coding=utf-8

from api.document.doc_tools import *
from api.view.base import BaseHandler
from app.customer.models.startup_image import StartupImage
from app.customer.models.switch import Switcher
from app.customer.models.version_info import VersionInfo
import time
from app.customer.models.user import UserHeartBeat
from app.channel.models.audit_info import *
from django.conf import settings

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
            'version_code': 1000000
        }
        app_name = ua.split(";")[0]
        uas = ua.split(";")
        if app_name == "liaoai_teyue" or app_name == "liaoai_lizhen":
            channel = None
        else:
            channel = uas[5]

        version = VersionInfo.get_version_info(platform, app_name, channel)
        ua_version = ua.split(";")[1]

        if version:
            version_info = version.format_version_info()
            # 强升
            if ua_version < version.min_version:
                version_info["upgrade_type"] = 1
            elif version.min_version <= ua_version < version.version:
                version_info["upgrade_type"] = version.upgrade_type
            else:
                version_info["upgrade_type"] = 0

            downloads_url = version.download_url
            version_info["download_url"] = downloads_url
            version_info["desc"] = version.upgrade_info
        else:
            version_info["upgrade_type"] = 0
            version_info["download_url"] = ""
            version_info["desc"] = ""

        audit_info = ChannelAuditInfo.get_audit_info(channel)

        if audit_info and ua_version >= audit_info.version:
            switches["review"] = 0
        else:
            switches["review"] = 1


        share_url = settings.SHARE_URL
        invite_url = settings.INVITE_URL
        ins_img_url = settings.INS_IMAGE_URL

        self.write({
            'status': "success",
            'start_image': data,
            "system_timestamp": int(time.time()),
            "switch": switches,
            "version_info": version_info,
            "report_interval": UserHeartBeat.REPORT_INTERVAL,
            "share_url": share_url,
            "invite_url": invite_url,
            "ins_img_url": ins_img_url
        })
