# coding=utf-8

from api.document.doc_tools import *
from api.view.base import *
from app.customer.models.report import *
from app.util.messageque.msgsender import MessageSender
from app.customer.models.porncheck import PornCheckItem

@handler_define
class PornCheck(BaseHandler):
    @api_define("porn check", "/audit/porn_check",
                [
                    Param("file_id", True, str, "", "", description=u"图片id"),
                    Param("pic_url", True, str, "", "", description=u"图片id"),
                    Param("room_id", False, str, "", "", description=u"当前房间id"),
                    Param("user_id", True, str, "", "", description=u"用户id(图片拥有者)"),
                    Param("join_id", False, str, "", "", description=u"房间加入者")

                ],
                description=u"鉴黄接口"
                )
    @login_required
    def get(self):
        file_id = self.arg("file_id")
        pic_url = self.arg("pic_url")
        room_id = self.arg("room_id")
        user_id = self.arg("user_id")
        join_id = self.arg("join_id")

        #PornCheckItem.create_item(file_id=file_id, pic_url=pic_url,room_id=room_id,user_id=user_id,join_id=join_id)
        MessageSender.send_porn_check(file_id=file_id, pic_url=pic_url,room_id=room_id, user_id=user_id, join_id=join_id)
        return self.write({
            "status": "success",
        })


@handler_define
class ReportMessageShow(BaseHandler):
    @api_define("report message show", "/audit/report/message",
                [
                    Param("report_type", True, int, 0, 0, description=u"举报类型，0:个人主页举报，1：消息页面举报，2：聊天页面主播举报，3：聊天页面用户举报")
                ],description=u"获取举报文案")
    @login_required
    def get(self):
        report_type = self.arg_int("report_type")
        report_messages = ReportText.get_report_texts(report_type)

        report_texts = []
        for report_text in report_messages:
            data = {}
            data["label"] = report_text.label
            data["message"] = report_text.text
            report_texts.append(data)

        return self.write({
            "status": "success",
            "data": report_texts,
        })


@handler_define
class ReportMessageUpload(BaseHandler):
    @api_define("report message upload", "/audit/report/upload",
                [
                    Param("label", True, int, 101, 101, description=u"标签"),
                    Param("message", True, str, "", "色情举报", description=u"举报内容"),
                    Param("report_id", True, int, 0, 0, description=u"举报id"),
                    Param("pic_url", True, str, "", "", description=u"截图url"),
                    Param("file_id", True, str, "", "", description=u"截图文件id"),
                    Param("report_type", True, int, 0, 0, description=u"举报类型")

                ],description=u"举报消息上报")
    @login_required
    def get(self):
        user_id = self.current_user_id
        label = self.arg("label")
        message = self.arg("message")
        report_id = self.arg("report_id")
        pic_url = self.arg("pic_url")
        file_id = self.arg("file_id")
        report_type = self.arg_int("report_type")

        ReportRecord.create_report_record(user_id=user_id, label=label, report_id=report_id,
                                          text=message, pic_url=pic_url,
                                          file_id=file_id, report_type=report_type)

        return self.write({"status": "success"}) 