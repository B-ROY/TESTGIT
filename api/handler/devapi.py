# coding=utf-8


from api.document.doc_tools import *
from api.view.base import *

from app.customer.models.dev_info import DevInfoMatch
import datetime

@handler_define
class DevVisitHandler(BaseHandler):
    @api_define(r'dev visit', r'/dev/visit',
                [Param("model", False, str, "", "", u'手机型号'),
                 Param("osver", True, str, "", "", u'手机系统版本'),
                 Param("platform", True, str, "", "", u'手机系统版本'),
                 Param("user_id", True, str, "", "", u"页面用户id"),
                 Param("user_token", False, str, "", "", u"user_token")
                 ],
                description=u"呼叫接口")
    def get(self):

        model = self.arg("model")
        osver = self.arg("osver")
        platform = self.arg("platform")
        user_id = self.arg_int("user_id")
        ip=self.user_ip
        user_token=self.arg("user_token", "")

        dev_info_match = DevInfoMatch(model=model, osver=osver, platform=platform,
                                      visit_time=datetime.datetime.now(), user_id=user_id,ip=ip)
        dev_info_match.save()

        pass

@handler_define
class DevMatchHandler(BaseHandler):
    @api_define(r"dev match", r'/dev/match',
                [], description=u"用户访问应用建立关联"
    )
    @login_required
    def get(self):
        pass
        # ip = self.user_ip
        # ua = self.request.headers.get('User-Agent')
        # uas = ua.split(";")
        #
        # platform = 0 if uas[2]=="Android" else 1
        # osver = uas[3]
        # if platform ==0:
        #     model = uas[4]
        # else:
        #     model = uas[2]
        #
        # print ip, platform, osver, model
        # is_match, user_id = DevInfoMatch.match(model, ip, platform, osver)
        # if is_match:
        #     pass
        # else:
        #     pass
        #
        # dev_info_match = DevInfoMatch.objects.filter(model=model, ip=ip, platform=platform, osver=osver).first()
        # if dev_info_match:
        #     print "got it"


