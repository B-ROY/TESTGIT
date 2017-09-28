#coding=utf-8
from api.document.doc_tools import *
from api.view.base import BaseHandler
import time
from api.view.base import *
from api.convert.convert_user import *
from app.customer.models.task import Task


@handler_define
class TaskList(BaseHandler):
    @api_define("task list", r'/task/task_list', [], description="任务中心")
    @login_required
    def get(self):
        user_id = int(self.current_user_id)
        user = self.current_user
        novice_data, day_data, anchor_data = Task.get_list(user_id)
        data = {}
        if novice_data:
            data["novice_data"] = novice_data

        if day_data:
            data["day_data"] = day_data

        if anchor_data:
            data["anchor_data"] = anchor_data

        self.write({"status": "success", "data": data})


@handler_define
class FinishTask(BaseHandler):
    @api_define("task finish", r'/task/finish', [
        Param('record_id', True, str, "1", "1", u'record_id (任务中心, 领取状态传入的 record_id)'),
    ], description="任务完成, 领取")
    @login_required
    def get(self):
        user_id = int(self.current_user_id)
        user = self.current_user
        record_id = self.arg("record_id")
        status, error = Task.finish_task(user, record_id)
        if status != 1:
            return self.write({"status": "failed", "error": _(error)})
        self.write({"status": "success"})
