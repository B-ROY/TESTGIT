#coding=utf-8
from api.document.doc_tools import *
from api.view.base import *
from app.customer.models.gift import *
from app.customer.models.account import *
import json
from app.customer.models.black_user import *

@handler_define
class GetGiflList(BaseHandler):
    @api_define("Get Gift List", r'/gift/list',
        [], description=u'获取礼物列表')
    def get(self):
        gift_list = Gift.list_mall()
        data = []
        for gift in gift_list:
            data.append(Gift.normal_info(gift))

        self.write({
            "status": "success",
            "gift_list": data
        })
@handler_define
class GetInstantGiftList(BaseHandler):
    @api_define("Get instatnt List", r'/gift/instant/list',
                [], description=u"获取快捷赠送礼物列表")
    def get(self):
        gift_list = Gift.list(gift_type=2)
        data = []
        for gift in gift_list:
            data.append(Gift.normal_info(gift))

        self.write({
            "status":"success",
            "gift_list":data
        })

@handler_define
class SendGift(BaseHandler):
    @api_define("Send Gift", r'/gift/send',
            [
                Param('user_id', True, str, "", "", u'收礼人id'),
                Param("gift_id", True, str, "", "", u'礼物id'),
                Param("count", True, int, 0, 0, u'礼物数量'),
                Param("room_id", False, str, "", "", u'送礼的房间号')
            ], description=u'送礼物')
    @login_required
    def get(self):
        from_user = self.current_user
        to_user_id = self.arg("user_id")
        to_user = User.objects.get(id=to_user_id)
        gift_id = self.arg("gift_id")
        gift = Gift.objects.get(id=gift_id)
        gift_count = self.arg_int("count")
        gift_price = gift.price
        room_id = self.arg("room_id", "")

        if gift_count < 0 or gift_count == 0:
            return self.write({
                "status": "failed",
                "error": "dick boom sky",
            })

        # 校验黑名单
        black_user = BlackUser.objects.filter(from_id=from_user.id, to_id=to_user.id).first()
        if black_user:
            return self.write({
                "status": "failed",
                "error": "to_user is on the blacklist"
            })

        rever_black_user = BlackUser.objects.filter(from_id=to_user.id, to_id=from_user.id).first()
        if rever_black_user:
            return self.write({
                "status": "failed",
                "error": "you are on to_user's blacklist"
            })

        ua = self.request.headers.get('User-Agent')
        ua_version = ua.split(";")[1]
        value, error_code, error_message = Gift.gift_giving(from_user=from_user, to_user=to_user, gift_id=gift_id,
                                                            gift_count=gift_count, gift_price=gift.price,
                                                            room_id=room_id, ua_version=ua_version)
        if not error_code:
            error_code = 4000
        if not error_message:
            error_message = "赠送礼物失败"
        if value:
            self.write({
                "status": "success",
                "gift_id": gift_id,
                "gift_price": gift_price,
                "gift_count": gift_count,
            })
        else:
            self.write({
                "status": "failed",
                "error_code": error_code,
                "error_message": error_message,
            })

@handler_define
class GetReceivedList(BaseHandler):
    @api_define("Get Gift Received List", r'/gift/received/list',
                [
                    Param("user_id", True, str, "", "", u'用户id')
                ],
                description=u"获取收到的礼物列表")
    def get(self):
        user_id = self.arg("user_id")
        gift_list = GiftRecord.get_received_list(user_id)
        data = []
        count = 0
        for gift_record in gift_list:
            data.append(gift_record.get_normal_dic_info())
            count += gift_record.gift_count
        self.write({
            "status": "success",
            "total_count": count,
            "data": data
        })

