#coding=utf-8
import datetime

from api.document.doc_tools import *
from api.view.base import *
from django.conf import settings
from api.convert.convert_user import *

from api.util.agoratools.voicekeyutil import generate_media_channel_key, generate_signalingkey
import time

from app.customer.models.user import *
from app.customer.models.gift import GiftManager
from app.picture.models.picture import PictureInfo, PicturePriceList
from app.picture.models.comment import CommentInfo


# 创建新的图片
@handler_define
class CreatePicture(BaseHandler):
    @api_define("Create picture", r'/picture/create', [
        Param('picture_url', True, str, "", "", u'图片url'),
        Param('desc', True, str, None, None, u'描述'),
        Param('picture_type', False, str, None, None, u'图片类型'),
        Param('price', True, str, "0", "0", u'价格'),
        Param('is_private', False, str, "1", "1", u'权限'),
        Param('lock_type', True, str, "0", "0", u'锁类型'),
        Param('lock_count', False, str, "0", "0", u'自动解锁需购买次数'),
        Param('location', False, str, None, None, u'地点'),
        Param('mention', False, str, None, None, u'圈人'),
    ], description=u'创建图片')
    @login_required
    def get(self):
        user_id = self.current_user_id
        # picture_url = self.arg('picture_url')
        picture_url = User.convert_http_to_https(self.arg('picture_url'))
        desc = self.arg('desc', "")
        picture_type = self.arg('picture_type', "")
        price = self.arg_int('price', 0)
        is_private = self.arg_int('is_private', 1)
        lock_type = self.arg_int('lock_type', 0)
        lock_count = self.arg_int('lock_count', 0)
        location = self.arg('location', "")
        mention = self.arg('mention', [])
        created_at = datetime.datetime.now()

        picture_id = PictureInfo.create_picture(user_id=user_id, created_at=created_at, picture_url=picture_url,
                                                desc=desc, picture_type=picture_type, price=price, is_private=is_private,
                                                lock_type=lock_type, lock_count=lock_count, location=location,
                                                mention=mention)
        if picture_id:
            self.write({"status": "success", "picture_id": picture_id, })
        else:
            self.write({"status": "failed", })


# 删除图片
@handler_define
class DeletePicture(BaseHandler):
    @api_define("Delete picture", r'/picture/delete', [
        Param('picture_id', True, str, "", "", u'图片id'),
    ], description=u'删除图片')
    @login_required
    def get(self):
        user_id = self.current_user_id
        picture_id = self.arg('picture_id')
        status = PictureInfo.delete_picture(picture_id, user_id)
        if status:
            self.write({"status": "success", })
        else:
            self.write({"status": "failed", })


# 获得图片广场页列表
@handler_define
class GetPictureList(BaseHandler):
    @api_define("Get Picture List", r'/picture/list', [
        Param('page', True, str, "1", "1", u'page'),
        Param('page_count', True, str, "10", "10", u'page_count'),
    ], description=u'获取图片列表')
    # @login_required
    def get(self):
        user_id = self.current_user_id
        page = self.arg_int('page')
        page_count = self.arg_int('page_count')

        pictures = PictureInfo.get_picture_list(page=page, page_count=page_count)
        data = []
        for picture in pictures:
            user = PictureInfo.get_picture_user(user_id=picture.user_id)
            if not user_id:
                is_purchase = False
                is_like = False
            else:
                is_purchase = PictureInfo.check_is_purchase(picture.id, user_id)
                is_like = PictureInfo.check_is_like(picture.id, user_id)
            picture_count = PictureInfo.objects.filter(user_id=user.id, status=0).count()
            if picture.lock_type == 0:
                is_purchase = True
            if is_purchase:
                dic = {
                    "user": convert_user(user),
                    "picture": convert_real_picture(picture),
                    "is_like": is_like,
                    "is_purchase": is_purchase,
                    "picture_count": picture_count,
                }
            else:
                dic = {
                    "user": convert_user(user),
                    "picture": convert_picture(picture),
                    "is_like": is_like,
                    "is_purchase": is_purchase,
                    "picture_count": picture_count,
                }
            data.append(dic)

        self.write({"status": "success", "data": data, })


# 图片列表_精简版
@handler_define
class GetPictureListV2(BaseHandler):
    @api_define("Get Picture List", r'/picture/list_v2', [
        Param('page', True, str, "1", "1", u'page'),
        Param('page_count', True, str, "10", "10", u'page_count'),
        Param('user_id', False, str, "", "", u' user_id'),
    ], description=u'简版_获取图片列表V2')
    @login_required
    def get(self):
        user_id = self.arg("user_id","")
        page = self.arg_int('page')
        page_count = self.arg_int('page_count')
        current_user_id = self.current_user_id

        if not user_id:
            uid = current_user_id
        else:
            uid = user_id
        pictures = PictureInfo.objects.filter(user_id=int(uid), status=0).order_by('-created_at')[(page-1)*page_count:page*page_count]
        data = []
        for picture in pictures:
            pic_url = picture.picture_url
            if pic_url:
                dic = {
                    "id": str(picture.id),
                    "picture_url": pic_url
                }
                data.append(dic)

        self.write({"status": "success", "data": data, })


# 解锁人列表
@handler_define
class UnlockUserList(BaseHandler):
    @api_define("Unlock User List", r'/picture/unlock_list', [
        Param('picture_id', True, str, "", "", u'图片id'),
        Param('page', True, str, "1", "1", u'page'),
        Param('page_count', True, str, "10", "10", u'page_count'),
    ], description=u'解锁人列表')
    @login_required
    def get(self):
        picture_id = self.arg('picture_id')
        page = self.arg_int('page')
        page_count = self.arg_int('page_count')
        user_list = PictureInfo.get_unlock_user_list(picture_id=picture_id, page=page, page_count=page_count)
        data = []
        for user_id in user_list:
            user = PictureInfo.get_picture_user(user_id)
            data.append(convert_user(user))

        self.write({"status": "success", "data": data, })


# 浏览照片
@handler_define
class ViewPicture(BaseHandler):
    @api_define("View picture", r'/picture/view', [
        Param('picture_id', True, str, "", "", u'图片id'),
    ], description=u'浏览照片')
    # @login_required
    def get(self):
        picture_id = self.arg('picture_id')
        PictureInfo.add_viewcount(picture_id)
        picture = PictureInfo.get_picture_info(picture_id=picture_id)
        comments = picture.comment
        comments.reverse()
        data = []
        for comment_id in comments:
            comment = CommentInfo.comment_view(comment_id=comment_id)
            user = CommentInfo.get_comment_user(user_id=comment.user_id)
            if comment.reply_id:
                reply_user = CommentInfo.get_comment_user(user_id=comment.reply_id)
                dic = {
                    "id": str(comment.id),
                    "user": convert_user(user),
                    "reply": convert_user(reply_user),
                    "comment": comment.comment,
                    "like_count": comment.like_count,
                    "created_at": datetime_to_timestamp(comment.created_at),
                    "status": comment.status,
                    "picture_id": comment.picture_id,
                }
            else:
                dic = {
                    "id": str(comment.id),
                    "user": convert_user(user),
                    "comment": comment.comment,
                    "like_count": comment.like_count,
                    "created_at": datetime_to_timestamp(comment.created_at),
                    "status": comment.status,
                    "picture_id": comment.picture_id,
                }
            data.append(dic)

        self.write({"status": "success", "picture": convert_real_picture(picture), "data": data, })


# 图片点赞
@handler_define
class PictureLike(BaseHandler):
    @api_define("Picture like", r'/picture/like', [
        Param('picture_id', True, str, "", "", u'图片id'),
    ], description=u'给图片点赞')
    @login_required
    def get(self):
        user_id = int(self.current_user_id)
        picture_id = self.arg('picture_id')
        status = PictureInfo.create_likeuser(picture_id, user_id)
        if status:
            self.write({"status": "success", "picture_id": picture_id, })
        else:
            self.write({"status": "failed", })


# 图片取消点赞
@handler_define
class PictureUnlike(BaseHandler):
    @api_define("Picture unlike", r'/picture/unlike', [
        Param('picture_id', True, str, "", "", u'图片id'),
    ], description=u'图片取消点赞')
    @login_required
    def get(self):
        user_id = int(self.current_user_id)
        picture_id = self.arg('picture_id')
        status = PictureInfo.cancel_likeuser(picture_id, user_id)
        if status:
            self.write({"status": "success", "picture_id": picture_id, })
        else:
            self.write({"status": "failed", })


# 图片回复评论
@handler_define
class CreatePictureComment(BaseHandler):
    @api_define("Create picture comment", r'/picture/createcomment', [
        Param('picture_id', True, str, "", "", u'图片id'),
        Param('reply_id', True, str, "", "", u'给谁回复评论'),
        Param('comment', True, str, "", "", u'评论内容'),
    ], description=u'图片添加评论')
    @login_required
    def get(self):
        user_id = self.current_user_id
        picture_id = self.arg('picture_id')
        reply_id = self.arg_int('reply_id', 0)
        comment = self.arg('comment')
        created_at = datetime.datetime.now()
        status = PictureInfo.create_comment(picture_id=picture_id, user_id=user_id, reply_id=reply_id,
                                            created_at=created_at, comment=comment)
        if status:
            self.write({"status": "success", })
        else:
            self.write({"status": "failed", })


# 图片评论删除
@handler_define
class DeletePictureComment(BaseHandler):
    @api_define("Delete picture comment", r'/picture/deletecomment',[
        Param('comment_id', True, str, "", "", u'评论id'),
    ], description=u'图片评论删除')
    @login_required
    def get(self):
        user_id = self.current_user_id
        comment_id = self.arg('comment_id')
        status = PictureInfo.delete_comment(comment_id, user_id)
        if status:
            self.write({"status": "success", })
        else:
            self.write({"status": "failed", })


# 价格列表
@handler_define
class GetPriceList(BaseHandler):
    @api_define("Get Picture Price List", r'/picture/price/list', [], description=u'获取价格列表')
    @login_required
    def get(self):
        price_list = PicturePriceList.get_price_list()
        data = []
        for price in price_list:
            dic = {
                "price": price.picture_price,
                "desc": price.price_desc,
            }
            data.append(dic)

        self.write({"status": "success", "data": data, })

################### 新接口  ##################

@handler_define
class UserPictureCreate(BaseHandler):
    @api_define("Create User picture", r'/user_picture/create', [
        Param('picture_urls', True, str, "", "", u'图片url, 多个逗号相隔')
    ], description=u'保存用户相册图片')
    @login_required
    def get(self):
        user_id = self.current_user_id
        picture_urls = self.arg('picture_urls')
        picture_url_list = picture_urls.split(',')
        picture_ids = []

        if picture_url_list:
            created_at = datetime.datetime.now()
            for temp_pic_url in picture_url_list:
                pic_url = User.convert_http_to_https(temp_pic_url)
                pic_info = PictureInfo()
                pic_info.user_id = user_id
                pic_info.lock_type = 0
                pic_info.picture_url = pic_url
                pic_info.created_at = created_at
                pic_info.type = 1
                pic_info.save()
                picture_ids.append(str(pic_info.id))

        if picture_ids:
            self.write({"status": "success", "picture_ids": picture_ids})
        else:
            self.write({"status": "failed", })
