# coding=utf-8
import datetime

from api.document.doc_tools import *
from api.view.base import *
from app.customer.models.getuiusers import GeTuiUsers


@handler_define
class AddGeTui(BaseHandler):
    @api_define("add getui record", "/getui/add_record",
                [
                    Param("dev_no", True, str, "", "", u"客户端设备号"),
                    Param("cid", True, str, "", "", u"个推clientid"),
                    Param("province", True, str, "", "", u"省"),
                    Param("city", True, str, "", "", u"市"),
                    Param("districts", True, str, "", "", u"区"),
                    Param("address", True, str, "", "", u"地址"),
                    Param("os_version", True, str, "", "", u"操作系统版本号"),
                    Param("platfrom", True, str, "", "", u"平台"),
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
        platfrom = self.arg("platfrom", "")
        gtuser = GeTuiUsers()
        gtuser.dev_no = dev_no
        gtuser.cid = cid
        gtuser.appname = app_name
        gtuser.province = province
        gtuser.city = city
        gtuser.districts = districts
        gtuser.address = address
        gtuser.os_version = os_version
        gtuser.platfrom = platfrom
        gtuser.create_time = datetime.datetime.now()
        try:
            gtuser.save()
            return self.write({"status": "success"})
        except Exception,e:
            logging.error("create Getui error:{0}".format(e))
            return self.write({"status": "fail","error": u"上报设备信息失败"})

@handler_define
class UpdateGeTui(BaseHandler):
    @api_define("update getui record", "/getui/update_record",
                [
                    Param("dev_no", True, str, "", "", u"设备号"),
                    Param("user_id", True, str, "", "", u"用户短id"),
                ], description=u"绑定用户设备")
    def get(self):
        resultmap ={}
        dev_no = self.arg("dev_no", "")
        user_id = self.arg("user_id", "")
        if dev_no != "" and user_id != "":
            record = GeTuiUsers.objects.filter(dev_no = dev_no).first()
            if record:
                record.user_id = int(user_id)
                record.save()
                resultmap["status"] = "success"
            else:
                resultmap["status"] = "fail"
                resultmap["error"] = u"无该设备号的记录"
        else:
            resultmap["status"] = "fail"
            resultmap["error"] = u"设备号和用户id不能为空"
        return self.write(resultmap)

@handler_define
class UnBindGeTui(BaseHandler):
    @api_define("unbind getui record", "/getui/unbind_user",
                [
                    Param("dev_no", True, str, "", "", u"设备号"),
                    Param("user_id", True, str, "", "", u"用户短id"),
                ], description=u"解绑用户设备")
    def get(self):
        resultmap ={}
        dev_no = self.arg("dev_no", "")
        user_id = self.arg("user_id", "")
        if dev_no != "" and user_id != "":
            record = GeTuiUsers.objects.filter(dev_no = dev_no,user_id=int(user_id)).first()
            if record:
                record.user_id = None
                record.save()
                resultmap["status"] = "success"
            else:
                resultmap["status"] = "fail"
                resultmap["error"] = u"无该设备号及userid的记录"
        else:
            resultmap["status"] = "fail"
            resultmap["error"] = u"设备号和用户id不能为空"
        return self.write(resultmap)



