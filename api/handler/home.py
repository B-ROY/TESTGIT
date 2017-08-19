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
from app.customer.models.real_video_verify import RealVideoVerify

@handler_define
class RecommendList(BaseHandler):
    @api_define("get recommend list", r'/home/recommend/list', [], description=u"首页各栏目推荐列表")
    def get(self):
        #audiorooms = AudioRoomRecord.get_online_users_v1(query_time=datetime.datetime.now(), page=1, page_count=9, gender=2, is_video=0)
        #videorooms = AudioRoomRecord.get_online_users_v1(query_time=datetime.datetime.now(), page=1, page_count=27, gender=2, is_video=1)
        audio_list = []
        video_list = []
        hot_list = []
        recommed_list = UserRedis.get_recommed_list()
        recommed_data = eval(UserRedis.get_recommed())
        if recommed_list:
            try:
                for recommed in recommed_list:
                    hot_list.append(recommed_data[recommed])
            except Exception,e:
                print e
                hot_list = oldcommonlist()
        else:
            hot_list = oldcommonlist()

        result_advs = []
        advs = Adv.get_list()
        for adv in advs or []:
            result_advs.append(adv.normal_info())

        self.write({
            "status": "success",
            "banners": result_advs,
            "audio_list": audio_list,
            "video_list": video_list,
            "hot_list": map(lambda x:json.loads(x), hot_list),
        })

def oldcommonlist():
    now_time = int(time.time())
    pre_time = now_time - 120
    heartbeats = UserHeartBeat.objects.filter(last_report_time__gte=pre_time)
    hots=[]
    anchors = Anchor.objects.all()
    hot_ids = []
    hot_list = []
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

        show_video = RealVideoVerify.objects(user_id=user.id, status=1).order_by("-update_time").first()
        if show_video:
            dic["check_real_video"] = show_video.status
        else:
            real_video = RealVideoVerify.objects(user_id=user.id, status__ne=2).order_by("-update_time").first()
            if real_video:
                dic["check_real_video"] = real_video.status
            else:
                dic["check_real_video"] = 3
        hot_list.append(json.dumps(dic))
    return hot_list

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
                if not user.audio_room_id:
                    continue
                # 是否在线 查看心跳
                import time
                time = int(time.time())
                pre_time = time - 3600
                user_beat = UserHeartBeat.objects.filter(user=user, last_report_time__gte=pre_time).first()
                if user_beat:
                    is_online = 1
                else:
                    is_online = 0

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
                # 视频认证状态
                real_video = RealVideoVerify.objects(user_id=user.id, status__ne=2).order_by("-update_time").first()
                show_video = RealVideoVerify.objects(user_id=user.id, status=1).order_by("-update_time").first()
                if show_video:
                    dic["check_real_video"] = show_video.status
                else:
                    if real_video:
                        dic["check_real_video"] = real_video.status
                    else:
                        dic["check_real_video"] = 3
                data.append(dic)
        return self.write({"status": "success", "data": data, })
