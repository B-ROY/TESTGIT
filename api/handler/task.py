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
        self.write({"status": "success", "novice_data": novice_data, "day_data": day_data, "anchor_data": anchor_data})
