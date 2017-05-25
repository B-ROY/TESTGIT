#coding=utf-8
from api.document.doc_tools import *
from api.view.base import BaseHandler
from app.customer.models.version_info import VersionInfo
import time


@handler_define
class VersionCheck(BaseHandler):
    @api_define("Version_check", r'/app/version/check',[
        Param('platform', True, str, "","",u'IOS,ANDROID,H5,WEB'),
    ], description="检查更新接口")
    def get(self):
        platform = self.arg("platform")
        version_info = {
            'version': '',
            'upgrade_type': '',
            'download_url': '',
            'upgrade_info': '',
        }
        ua = self.request.headers.get('User-Agent')
        app_name = ua.split(";")[0]
        version = VersionInfo.get_version_info(platform, app_name)
        if version:
            version_info = version.format_version_info()
        #version_info['desc'] = u'检测到新版本'
        self.write({
            'status': "success",
            'system_timestamp': int(time.time()),
            'version_info': version_info
        })

