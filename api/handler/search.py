#coding=utf-8
from api.document.doc_tools import *
from api.view.base import *
from app.live.models import *
from django.conf import settings
import time
import tempfile
from app.customer.models.follow import *
from app.customer.models.user import *
from app.picture.models.picture import *


module_title = "房间 API"

@handler_define
class DoSearch(BaseHandler):
    @api_define("Search", r'/live/user/search', [
        Param('keyword', True, str, "", "", u'用户id或者keyword'),
    ], description=u"搜索接口")

    # @login_required
    def get(self):
        #关注者

        keyword = self.arg("keyword")
        results = []

        if keyword:
            users = User.search(keyword)
            #user_ids = []
            #for user in users:
            #    user_ids.append(user.id)

            #followed_list = UserFollow.is_followered_list(self.current_user_id, user_ids)
            #followed_dict = {}
            #for ff in followed_list or []:
            #    followed_dict[ff.followee_id] = 1

            for user in users:
                #self.current_user_id
                d = user.get_normal_dic_info()
                d["follower_count"] = FollowFansList.follow_count(user_id=user.id)
                d["followee_count"] = FollowFansList.fans_count(user_id=user.id)
                d["picture_count"] = PictureInfo.objects.filter(user_id=user.id, status=0).count()
                if not self.current_user_id:
                    d["is_followed"] = 0
                else:
                    d["is_followed"] = FollowFansList.check_follow(self.current_user_id, user.id)
                #if followed_dict.get(user.id):
                #    d["is_followed"] = 1
                #else:
                #    d["is_followed"] = 0

                results.append(d)


        self.write({'status': 'success',"results":results})

