#coding=utf-8
from api.document.doc_tools import *
from api.view.base import BaseHandler
import time
from api.view.base import *
from api.convert.convert_user import *
from app.customer.models.friend import *
from django.db.models import Q


@handler_define
class Apply_Friend(BaseHandler):
    @api_define("apply friend", r'/friend/apply_friend', [
        Param("friend_id", True, str, "", "", u"friend_id"),
    ], description="申请好友")

    @login_required
    def get(self):
        user_id = int(self.current_user_id)
        friend_id = self.arg("friend_id", "")

        if user_id == friend_id:
            return self.write({"status": "failed", "error_message": "您无需添加自己为好友", })

        # 判断是否已经成为好友
        friend = Friend.objects.filter(user_id=user_id, friend_id=friend_id, friend_status=2).first()
        if friend:
            return self.write({"status": "failed", "error_message": "对方已经成为您的好友", })

        # 是否可以申请(好友记录里面没有没清除的此好友申请记录)
        is_apply = FriendStatusRecord.objects.filter(oper_user_id=user_id, to_user_id=friend_id, friend_status=1)
        if not is_apply:
            Friend.apply_friend(user_id, friend_id)

        self.write({"status": "success"})


@handler_define
class Add_Friend(BaseHandler):
    @api_define("add friend", r'/friend/add_friend', [
        Param("friend_id", True, str, "", "", u"friend_id"),
    ], description="同意添加好友")

    @login_required
    def get(self):
        user_id = int(self.current_user_id)
        friend_id = self.arg("friend_id", "")

        # 判断是否已经成为好友
        friend = Friend.objects.filter(user_id=user_id, friend_id=friend_id, friend_status=2).first()
        # reverse_friend = Friend.objects.filter(user_id=friend_id, friend_id=user_id, friend_status=2).first()
        if friend:
            return self.write({"status": "failed", "error_message": "对方已经成为您的好友", })

        Friend.add_friend(user_id, friend_id)

        self.write({"status": "success"})


@handler_define
class FriendList(BaseHandler):
    @api_define("friend list ", r'/friend/friend_list', [], description="好友列表")

    @login_required
    def get(self):
        user_id = int(self.current_user_id)
        data = []
        friends = Friend.objects.filter(user_id=user_id, friend_status=2)
        if friends:
            for friend in friends:
                user = User.objects.filter(id=friend.friend_id).first()
                dic = {
                    "user": convert_user(user)
                }
                data.append(dic)

        self.write({"status": "success", "data": data})


@handler_define
class ApplyList(BaseHandler):
    @api_define("add friend", r'/friend/apply_list', [], description="好友申请列表")

    @login_required
    def get(self):
        user_id = int(self.current_user_id)
        data = []
        records = []

        apply_records = FriendStatusRecord.objects.filter(to_user_id=user_id, friend_status=1)
        success_records = FriendStatusRecord.objects.filter(oper_user_id=user_id, friend_status=2)

        if apply_records:
            for r in apply_records:
                record = FriendStatusRecord.objects.filter(oper_user_id=user_id, to_user_id=r.oper_user_id, friend_status=2)
                if not record:
                    user = User.objects.filter(id=r.oper_user_id).first()
                    date_time = r.create_time.strftime('%Y-%m-%d %H:%M:%S')
                    dic = {
                        "record_id": str(r.id),
                        "user": convert_user(user),
                        "status": r.friend_status,
                        "date_time": date_time
                    }
                    data.append(dic)


        if success_records:
            for r in success_records:
                user = User.objects.filter(id=r.to_user_id).first()
                date_time = r.create_time.strftime('%Y-%m-%d %H:%M:%S')
                dic = {
                    "record_id": str(r.id),
                    "user": convert_user(user),
                    "status": r.friend_status,
                    "date_time": date_time
                }
                data.append(dic)

        self.write({"status": "success", "data": data})


@handler_define
class ClearFriend(BaseHandler):
    @api_define("clear friend", r'/friend/clear_friend', [
        Param("record_id", True, str, "", "", u"record_id"),
    ], description="清除好友申请(非删除,拉黑好友)")

    @login_required
    def get(self):
        record_id = self.arg("record_id", "")
        FriendStatusRecord.clear_record(record_id)
        self.write({"status": "success"})

@handler_define
class ClearFriendList(BaseHandler):
    @api_define("clear friend_list", r'/friend/clear_friend_list', [], description="清空好友申请列表")

    @login_required
    def get(self):
        user_id = int(self.current_user_id)
        FriendStatusRecord.clear_record_list(user_id)
        self.write({"status": "success"})


@handler_define
class ISFriend(BaseHandler):
    @api_define("is friend", r'/friend/is_friend', [
        Param("friend_id", True, str, "", "", u"friend_id"),
    ], description="判断是否是好友")

    @login_required
    def get(self):
        user_id = int(self.current_user_id)
        friend_id = self.arg("friend_id", "")
        is_friend = 0
        # 判断是否已经成为好友
        friend = Friend.objects.filter(user_id=user_id, friend_id=friend_id, friend_status=2).first()

        if friend:
            is_friend = 1

        self.write({"status": "success", "is_friend": is_friend, })


@handler_define
class BlackFriend(BaseHandler):
    @api_define("black friend", r'/friend/black_friend', [
        Param("friend_id", True, str, "", "", u"friend_id"),
    ], description="拉黑好友")

    @login_required
    def get(self):
        user_id = int(self.current_user_id)
        friend_id = self.arg("friend_id", "")

        Friend.black_friend(user_id, friend_id)
        FriendStatusRecord.black_user_clear(user_id, friend_id)

        self.write({"status": "success" })



