# coding=utf-8
from api.document.doc_tools import *
from api.view.base import *
from app.audio.models.record import AudioRoomRecord
import json
import datetime
from api.convert.convert_user import *
from app.customer.models.personal_tags import *
from app.customer.models.hotAnchor import *
from app.customer.models.adv import Adv
from app.customer.models.rank import *
from app.customer.models.vip import *
from app.customer.models.index_column import *
import random

@handler_define
class RecommendList(BaseHandler):
    @api_define("get recommend list", r'/home/recommend/list', [], description=u"首页各栏目推荐列表")
    def get(self):
        hot_ids = [3078716,
                3078715,
                3078714,
                3078713]
        ua = self.request.headers.get('User-Agent')
        uas = ua.split(";")
        app_name = uas[0]

        if app_name == "reliaozaixian":
            hot_ids = [
                    3080093,
                    3080094,
                    3080092,
                    3080091,
                    3080087,
            ]


        if app_name == "tianmireyue":
            hot_ids = []

        if app_name == "liaoai_yelaixiang":
            hot_ids = [
                3301434,
                3301433,
                3301432,
                3301431,
            ]
        random.shuffle(hot_ids)

        hot_list = []
        for hot_id in hot_ids:
            user = User.objects.get(identity=hot_id)

            if not user.audio_room_id:
                user.audio_room_id = AudioRoomRecord.create_roomrecord(user.id, datetime.datetime.now())

            room = AudioRoomRecord.objects.get(id=user.audio_room_id)

            dic = {
                "audioroom": convert_audioroom(room),
                "user": convert_user(user),
                "time_stamp": datetime_to_timestamp(room.open_time),
            }
            hot_list.append(dic)

        result_advs = []
        #advs = Adv.objects.filter(id__in=["58cf48d218ce425cad6e61e8","594cd0ca89deba88c66bb821"])
        #for adv in advs or []:
        #    result_advs.append(adv.normal_info())


        self.write({
            "status": "success",
            "banners": result_advs,
            "hot_list": hot_list,
        })

@handler_define
class ColumnList(BaseHandler):
    @api_define("home column list ", r'/home/column_list', [], description=u"首页栏目列表")
    def get(self):

        columns = IndexColumn.objects.filter(delete_status=1).order_by("-colume_type")
        data = []
        if columns:
            for column in columns:
                dic = convert_columns(column)
                data.append(dic)

        self.write({"status": "success", "columns": data})

@handler_define
class Get_Index_Column(BaseHandler):
    @api_define("get_index_column ", r'/audio/room/get_index_column', [
        Param('page', True, str, "1", "1", u'page'),
        Param('page_count', True, str, "10", "10", u'page_count'),
        Param('column_type', True, str, "2", "2", u'column_type　2:新人驾到  ')
    ], description=u"获取首页某栏目信息")
    def get(self):
        column_type = self.arg_int('column_type')
        page = self.arg_int('page')
        page_count = self.arg_int('page_count')

        if page !=1:
            return self.write({"status": "success", "data": [], })
        
        data = []

        if column_type == 2:
            # 新人驾到
            ids = [
                3014372,
                3014195,
                3078722,
                3078721,
            ]
            ua = self.request.headers.get('User-Agent')
            uas = ua.split(";")
            app_name = uas[0]
            app_version = uas[1]
            if app_name == "reliaozaixian":
                ids = [
                    3080101,
                    3080102,
                    3080100,
                    3080097,
                ]
            if app_name == "tongchengyueai":
                ids = [
                    3301400,
                    3301399,
                    3301398,
                    3301397,
                    3301396,
                    3301395,
                    3301394,
                    3301393,
                    3301392,
                    3301391
                ]
            random.shuffle(ids)
            if app_name == "tianmireyue" and app_version > "2.3.5":
                ids = [
                    3301398,
                    3301397,
                    3080102,
                    3014195,
                    3301392,
                    3301396,
                ]

            if app_name == "liaoai_yelaixiang":
                ids=[
                    3080101,
                    3080102,
                    3301397,
                    3301396,
                    3301395,
                ]
                random.shuffle(ids)

            for id in ids:
                user = User.objects.filter(identity=id).first()
                if user.id == 1 or user.id == 2:
                    continue
                if not user.audio_room_id:
                    user.audio_room_id = AudioRoomRecord.create_roomrecord(user.id, datetime.datetime.now())
                # 是否在线 查看心跳
                import time
                time = int(time.time())
                pre_time = time - 3600
                user_beat = UserHeartBeat.objects.filter(user=user, last_report_time__gte=pre_time).first()
                if user_beat:
                    is_online = 1
                else:
                    is_online = 0

                print user.id
                audioroom = AudioRoomRecord.objects.get(id=user.audio_room_id)
                personal_tags = UserTags.get_usertags(user_id=user.id)
                user_vip = UserVip.objects.filter(user_id=user.id).first()
                if user_vip:
                    vip = Vip.objects.filter(id=user_vip.vip_id).first()
                    dic = {
                        "audioroom": convert_audioroom(audioroom),
                        "user": convert_user(user),
                        "personal_tags": personal_tags,
                        "vip": convert_vip(vip),
                        "is_online": is_online
                    }
                else:
                    dic = {
                        "audioroom": convert_audioroom(audioroom),
                        "user": convert_user(user),
                        "is_online": is_online,
                        "personal_tags": personal_tags
                    }
                data.append(dic)
        return self.write({"status": "success", "data": data, })