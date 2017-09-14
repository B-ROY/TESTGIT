#coding=utf-8
from api.document.doc_tools import *
from api.view.base import BaseHandler
import time
from api.view.base import *
from app.customer.models.task import Task


@handler_define
class TaskList(BaseHandler):
    @api_define("task list", r'/task/list', [], description="任务中心")
    @login_required
    def get(self):
        user_id = int(self.current_user_id)
        user = self.current_user
        data = Task.get_list(1, 1)
        self.write({"status": "success", "task_list": data})


