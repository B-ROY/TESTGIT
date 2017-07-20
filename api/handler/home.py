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
from app.customer.models.vip import *
from app.customer.models.index_column import *
from app.customer.models.rank import *

@handler_define
class RecommendList(BaseHandler):
    @api_define("get recommend list", r'/home/recommend/list', [], description=u"首页各栏目推荐列表")
    def get(self):
        #audiorooms = AudioRoomRecord.get_online_users_v1(query_time=datetime.datetime.now(), page=1, page_count=9, gender=2, is_video=0)
        #videorooms = AudioRoomRecord.get_online_users_v1(query_time=datetime.datetime.now(), page=1, page_count=27, gender=2, is_video=1)
        now_time = int(time.time())
        pre_time = now_time - 120
        heartbeats = UserHeartBeat.objects.filter(last_report_time__gte=pre_time)
        hots=[]
        anchors = Anchor.objects.all()
        hot_ids = []
        for anchor in anchors:
            user = User.objects.get(id=anchor.sid)
            user_heart = UserHeartBeat.objects.get(user=user)
            if user_heart.last_report_time > pre_time and user.disturb_mode != 1:
                hots.append(user)
                hot_ids.append(user.id)

        for heartbeat in heartbeats:
            if heartbeat.user.charm_value > 3500 and heartbeat.user.disturb_mode != 1 \
                    and heartbeat.user.id not in hot_ids and heartbeat.user.is_video_auth == 1:
                hots.append(heartbeat.user)

        if not hots:
            hots = User.objects.filter(is_video_auth=1).order_by("-charm_value")[0:4]

        audio_list = []
        video_list = []
        hot_list = []

        user_id_list=[]
        """
        for audioroom in audiorooms:
            user = AudioRoomRecord.get_audio_user(audioroom.user_id)
            personal_tags = UserTags.get_usertags(user_id=audioroom.user_id)
            if not personal_tags:
                personal_tags = []
            dic = {
                "audioroom": convert_audioroom(audioroom),
                "user": convert_user(user),
                "personal_tags": personal_tags,
                "time_stamp": datetime_to_timestamp(audioroom.open_time),
            }
            audio_list.append(dic)
            user_id_list.append(user.id)
        """
        for user in hots:
            room = AudioRoomRecord.objects.get(id=user.audio_room_id)
            personal_tags = UserTags.get_usertags(user_id=room.user_id)
            if not personal_tags:
                personal_tags = []

            user_vip = UserVip.objects.filter(user_id=user.id).first()

            # time = int(time.time())
            # pre_time = time - 120
            user_beat = UserHeartBeat.objects.filter(user=user, last_report_time__gte=pre_time).first()
            if user_beat:
                is_online = 1
            else:
                is_online = 0

            if not user_vip:
                dic = {
                    "audioroom": convert_audioroom(room),
                    "user": convert_user(user),
                    "personal_tags": personal_tags,
                    "time_stamp": int(time.time()),
                    "is_online": is_online
                }
            else:
                vip = Vip.objects.filter(id=user_vip.vip_id).first()
                dic = {
                    "audioroom": convert_audioroom(room),
                    "user": convert_user(user),
                    "personal_tags": personal_tags,
                    "time_stamp": int(time.time()),
                    "vip": convert_vip(vip),
                    "is_online": is_online
                }
            hot_list.append(dic)
            user_id_list.append(user.id)
        """    
        for videoroom in videorooms:
            user = AudioRoomRecord.get_audio_user(videoroom.user_id)
            if user.id not in user_id_list:
                personal_tags = UserTags.get_usertags(user_id=videoroom.user_id)
                if not personal_tags:
                    personal_tags = []
                dic = {
                    "audioroom": convert_audioroom(videoroom),
                    "user": convert_user(user),
                    "personal_tags": personal_tags,
                    "time_stamp": datetime_to_timestamp(videoroom.open_time),
                }
                video_list.append(dic)
        """
        result_advs = []
        advs = Adv.get_list()
        for adv in advs or []:
            result_advs.append(adv.normal_info())

        self.write({
            "status": "success",
            "banners": result_advs,
            "audio_list": audio_list,
            "video_list": video_list,
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
        data = []

        if column_type == 2:
            # 新人驾到
            anchor_list = NewAnchorRank.objects.all()[(page - 1) * page_count:page * page_count]

            for anchor in anchor_list:
                user = User.objects.filter(id=anchor.user_id).first()
                if user.id == 1 or user.id == 2:
                    continue

                audioroom = AudioRoomRecord.objects.get(id=user.audio_room_id)
                personal_tags = UserTags.get_usertags(user_id=user.id)
                user_vip = UserVip.objects.filter(user_id=user.id).first()
                if user_vip:
                    vip = Vip.objects.filter(id=user_vip.vip_id).first()
                    dic = {
                        "audioroom": convert_audioroom(audioroom),
                        "user": convert_user(user),
                        "personal_tags": personal_tags,
                        "vip": convert_vip(vip)
                    }
                else:
                    dic = {
                        "audioroom": convert_audioroom(audioroom),
                        "user": convert_user(user),
                        "personal_tags": personal_tags
                    }
                data.append(dic)
        return self.write({"status": "success", "data": data, })
