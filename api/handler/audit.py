# coding=utf-8

from api.document.doc_tools import *
from api.view.base import *
from app.customer.models.report import *
from app.util.messageque.msgsender import MessageSender
from app.util.shumeitools.shumeitools import *
from app.customer.models.block_user_device import BlockUserRecord
import international

@handler_define
class PornCheck(BaseHandler):
    @api_define("porn check", "/audit/porn_check",
                [
                    Param("file_id", True, str, "", "", description=u"图片id"),
                    Param("pic_url", True, str, "", "", description=u"图片url"),
                    Param("room_id", False, str, "", "", description=u"当前房间id"),
                    Param("user_id", True, str, "", "", description=u"主播id)"),
                    Param("join_id", False, str, "", "", description=u"房间加入者")

                ],
                description=u"鉴黄接口"
                )
    @login_required
    def get(self):
        file_id = self.arg("file_id")
        pic_url = self.arg("pic_url")
        room_id = self.arg("room_id")
        room_user_id = self.arg("user_id")
        join_id = self.arg("join_id")

        user_id = self.current_user_id


        #PornCheckItem.create_item(file_id=file_id, pic_url=pic_url,room_id=room_id,user_id=user_id,join_id=join_id)
        MessageSender.send_porn_check(file_id=file_id, pic_url=pic_url,room_id=room_id, user_id=user_id, join_id=join_id, room_user_id=room_user_id)
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

        desc = u"<html><p>" + _(u"%s您好，您的举报我们会及时处理，请静候佳音" % self.current_user.nickname) + u"</p></html>"

        MessageSender.send_system_message(user_id, desc)

        return self.write({"status": "success"})



@handler_define
class PictureCheck(BaseHandler):
    @api_define("yidun picture detect", "/audit/pic_check",[
            Param("file_id", True, str, "", "", description=u"图片id"),
            Param("pic_url", True, str, "", "", description=u"图片id"),
            Param("type", True, int, 1, 1, description=u"待鉴定图片类型,1:封面,2:头像,3:聊天")
        ], description=u"数美图片检测"
    )
    def get(self):
        file_id = self.arg("file_id")
        pic_url = self.arg("pic_url")
        pic_channel = self.arg("type")

        user = self.current_user
        if user.gender == 1:
            sex = user.gender
        else:
            sex = 0

        ret = shumei_image_detect(pic_url=pic_url, timeout=12, user_id=user.id, channel=pic_channel, sex=sex, phone=user.phone)

        # todo 格式不正确
        is_pass = 0
        if ret["code"] == 1100:
            if ret["riskLevel"] == "PASS":
                is_pass = 1
            if ret["riskLevel"] == "REJECT":
                is_pass = 0
            if ret["riskLevel"] == "REVIEW":
                # todo +人工审核逻辑
                is_pass = 1

        self.write({
            "status": "success",
            "is_pass": is_pass
        })


@handler_define
class TextCheck(BaseHandler):
    @api_define("MessageText checck", "/audit/text/check",[
        Param("text", True, str, "", "低俗小说", description=u"待鉴定文本"),
        Param("type", True, int, 0, 0, description=u"待鉴定来源(1:昵称,2:消息,3:资料")
    ], description=u"数美文本检测")
    @login_required
    def get(self):
        text = self.arg("text")
        guid = self.arg("guid")
        check_type = self.arg("type")

        ip = self.user_ip

        user = self.current_user

        ret = shumei_text_spam(text=text, timeout=1, user_id=user.id, channel=check_type, nickname=user.nickname, phone=user.phone, ip=ip)

        is_pass = 0
        if ret["code"] == 1100:
            if ret["riskLevel"]=="PASS":
                is_pass = 1
            if ret["riskLevel"] == "REJECT":
                is_pass = 0
            if ret["riskLevel"] == "REVIEW":
                # todo +人工审核逻辑
                is_pass = 1

        self.write({
            "status": "success",
            "is_pass": is_pass
        })


"""
@handler_define
class PictureCheck(BaseHandler):
    @api_define("yidun picture detect", "/audit/pic_check",[
            Param("file_id", True, str, "", "", description=u"图片id"),
            Param("pic_url", True, str, "", "", description=u"图片id"),
            Param("platform", True, int, 0, 0, description=u"用户设备类型")
        ], description=u"易盾图片检测"
    )
    def get(self):
        file_id = self.arg("file_id")
        pic_url = self.arg("pic_url")

        guid = self.arg("guid")
        ua = self.request.headers.get('User-Agent')
        uas = ua.split(";")
        device_type = 1
        if uas[2] == "iPhone":
            device_type = 4
        elif uas[2] == "iPad":
            device_type = 5
        elif uas[2] == "Android":
            device_type = 3
        else:
            device_type = 1

        user_id = self.current_user_id
        publish_time = str(int(time.time() * 1000))

        data_id = user_id + str(publish_time)

        images = []
        imageurl = {
            "name": data_id+"pic",
            "type": 1,
            "data": "http://p1.music.126.net/lEQvXzoC17AFKa6yrf-ldA==/1412872446212751.jpg"
        }
        images.append(imageurl)

        # print json.dumps(images)
        params = {
            "images": json.dumps(images),
            "account": "python@163.com",
            "ip": "123.115.77.137"
        }

        ret = YIDUNApi.text_check(params)
        if ret["code"] == 200:
            results = ret["result"]
            for result in results:
                print "taskId=%s，name=%s，labels：" % (result["taskId"], result["name"])
                maxLevel = -1
                for labelObj in result["labels"]:
                    label = labelObj["label"]
                    level = labelObj["level"]
                    rate = labelObj["rate"]
                    print "label:%s, level=%s, rate=%s" % (label, level, rate)
                    maxLevel = level if level > maxLevel else maxLevel
                if maxLevel == 0:
                    print "#图片机器检测结果：最高等级为\"正常\"\n"
                elif maxLevel == 1:
                    print "#图片机器检测结果：最高等级为\"嫌疑\"\n"
                elif maxLevel == 2:
                    print "#图片机器检测结果：最高等级为\"确定\"\n"
        else:
            print "ERROR: ret.code=%s, ret.msg=%s" % (ret["code"], ret["msg"])

        pass

@handler_define
class MessageTextCheck(BaseHandler):
    @api_define("MessageText checck", "/audit/text/check",[
        Param("text", True, str, "", "低俗小说", description=u"待鉴定文本")
    ], description=u"易盾文本检测")
    @login_required
    def get(self):
        text = self.arg("text")
        guid = self.arg("guid")
        ua = self.request.headers.get('User-Agent')
        uas = ua.split(";")

        if uas[2] == "iPhone" :
            device_type = 4
        elif uas[2] == "iPad":
            device_type = 5
        elif uas[2]=="Android":
            device_type = 3
        else:
            device_type = 1

        user_id = self.current_user_id
        publish_time = str(int(time.time() * 1000))

        data_id = user_id + str(publish_time)

        params = {
            "dataId": data_id,
            "content": text,
            "dataType": "1",
            "ip": "123.207.175.223",
            "account": str(user_id),
            "deviceType": str(device_type),
            "deviceId": guid,
            "callback": data_id,
            "publishTime": str(int(time.time() * 1000))
        }

        ret = YIDUNApi.text_check(params)

        if ret["code"] == 200:
            if len(ret["result"]) == 0:
                print "暂时没有人工复审结果需要获取，请稍后重试！"
            else:
                for result in ret["result"]:
                    taskId = result["taskId"]
                    callback = result["callback"]
                    labelArray = json.dumps(result["labels"], ensure_ascii=False)
                    if result["action"] == 0:
                        print "taskId=%s，callback=%s，文本人工复审结果：通过" % (taskId, callback)
                    else:
                        print "taskId=%s，callback=%s，文本人工复审结果：不通过，分类信息如下：%s" % (taskId, callback, labelArray)
        else:
            print "ERROR: code=%s, msg=%s" % (ret["code"], ret["msg"])

        pass
"""

@handler_define
class BlockList(BaseHandler):
    @api_define("block list", "/audit/block_list", [
                    Param("last_day", False, str, "2017-06-10", "2017-06-20", "最后一条记录时间，默认当天,格式年-月-日")
                ],
                description=u"封号列表"
                )
    def get(self):

        last_day = self.arg("last_day", "")
        if last_day:
            last_day = datetime.datetime.strptime(last_day, '%Y-%m-%d')
        else:
            last_day = datetime.datetime.today()

        block_list = BlockUserRecord.get_block_list(last_day)
        data = []

        for record in block_list:
            if not record.block_user_id:
                str_users = record.block_user_dev
            elif not record.block_user_dev:
                str_users = record.block_user_id
            else:
                str_users = record.block_user_id + "," + record.block_user_dev

            record_date_1 = record.block_date.strftime(u"%m月%d日")
            title = record_date_1 + u"违规公告"

            record_date_2 = (record.block_date-datetime.timedelta(days=1)).strftime(u"%m月%d日")
            content = record_date_2 + u"违规（包括且不限于色情、欺诈、拉人）封停账号如下：" + str_users


            dic = {
                "date": record.block_date.strftime("%Y-%m-%d"),
                "title": title,
                "content": content
            }
            data.append(dic)

        self.write({
            "status": "success",
            "data": data
        })



