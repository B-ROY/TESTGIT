# coding=utf-8
import datetime

from api.document.doc_tools import *
from api.view.base import *
from app.customer.models.getuiusers import GeTuiUsers


@handler_define
class AddGeTui(BaseHandler):
    @api_define("add getui record", "/getui/add_record",
                [
                    Param("user_id",True, str, "", "", u"用户短id"),
                    Param("dev_no", True, str, "", "", u"客户端设备号"),
                    Param("cid", True, str, "", "", u"个推clientid"),
                    Param("province", True, str, "", "", u"省"),
                    Param("city", True, str, "", "", u"市"),
                    Param("districts", True, str, "", "", u"区"),
                    Param("address", True, str, "", "", u"地址"),
                    Param("os_version", True, str, "", "", u"操作系统版本号"),
                    Param("platform", True, str, "", "", u"平台"),
                ], description=u"添加个推数据")
    def post(self):
        ua = self.request.headers.get('User-Agent')
        app_name = ua.split(";")[0]
        dev_no = self.arg("dev_no", "")
        cid = self.arg("cid", "")
        province = self.arg("province", "")
        city = self.arg("city", "")
        districts = self.arg("districts", "")
        address = self.arg("address", "")
        os_version = self.arg("os_version", "")
        platform = self.arg("platform", "")
        user_id = self.arg("user_id", "")
        record = GeTuiUsers.objects.filter(dev_no = dev_no).first()
        if record:
            if user_id != "":
                try:
                    record.user_id = int(user_id)
                    if app_name != "":
                        record.appname = app_name
                    if province != "":
                        record.province = province
                    if city != "":
                        record.city = city
                    if districts != "":
                        record.districts = districts
                    if address != "":
                        record.address = address
                    if os_version != "":
                        record.os_version = os_version
                    if platform != "":
                        record.platform = platform
                    record.save()
                    tuser = User.objects.filter(id=int(user_id)).first()
                    if tuser:
                        #tiantianyouliao;2.3.1;iPhone;10.3.2;iPhone 6 Plus;tiantianyouliao
                        tuser.devname = ua.split(";")[4]
                        tuser.osver = ua.split(";")[3]
                        tuser.save()
                    return self.write({"status": "success"})
                except Exception,e:
                    logging.error("create Getui error:{0}".format(e))
                    return self.write({"status": "fail","error": u"上报设备信息失败"})
            return self.write({"status": "success"})
        else :
                gtuser = GeTuiUsers()
                gtuser.dev_no = dev_no
                if user_id != "":
                    gtuser.user_id = int(user_id)
                gtuser.cid = cid
                gtuser.appname = app_name
                gtuser.province = province
                gtuser.city = city
                gtuser.districts = districts
                gtuser.address = address
                gtuser.os_version = os_version
                gtuser.platform = platform
                gtuser.create_time = datetime.datetime.now()
                try:
                    gtuser.save()
                    return self.write({"status": "success"})
                except Exception,e:
                    logging.error("create Getui error:{0}".format(e))
                    return self.write({"status": "fail","error": u"上报设备信息失败"})




