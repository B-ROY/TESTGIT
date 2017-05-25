#coding=utf-8
from mongoengine import *
import logging
import datetime
from app.picture.models.comment import *
from app.customer.models.user import *
from django.db import models
from PIL import Image, ImageFilter
import multiprocessing
from base.settings import CHATPAMONGO


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)


class PictureInfo(Document):

    PRIVATE = [
        (0, u'未公开'),
        (1, u'全部公开'),
        (2, u'仅好友可见'),
    ]

    STATUS = [
        (0, u'可见'),
        (1, u'删除'),
    ]

    LOCK = [
        (0, u'无锁'),
        (1, u'铜锁'),  # 1引力币
        (2, u'银锁'),  # 5引力币
        (3, u'金锁'),  # 10引力币
    ]

    user_id = IntField(verbose_name=u'用户id', required=True)
    created_at = DateTimeField(verbose_name=u'创建时间', default=None)
    picture_url = StringField(verbose_name=u'图片url', max_length=256, default=None)
    picture_real_url = StringField(verbose_name=u'真实图片url', max_length=256, default=None)
    comment = ListField(StringField(verbose_name=u'评论', default=None))
    desc = StringField(verbose_name=u'图片描述', max_length=65535, default=None)
    picture_type = StringField(verbose_name=u'分类', max_length=1024, default=None)
    price = IntField(verbose_name=u'价格', default=0)
    is_private = IntField(verbose_name=u'权限', default=0, choices=PRIVATE)
    lock_type = IntField(verbose_name=u'锁类型', default=0, choices=LOCK)
    lock_count = IntField(verbose_name=u'自动解锁需购买次数', default=0)
    purchase_list = ListField(IntField(verbose_name=u'购买人详情', default=None))
    location = StringField(verbose_name=u'地点', max_length=256, default=None)
    mention = ListField(IntField(verbose_name=u'圈人', default=None))
    like_user = ListField(IntField(verbose_name=u'点赞人', default=None))
    like_count = IntField(verbose_name=u'点赞数', default=0)
    view_count = IntField(verbose_name=u'浏览次数', default=0)
    status = IntField(verbose_name=u'状态', default=0)

    class Meta:
        app_label = "picture"
        verbose_name = u"图片"
        verbose_name_plural = verbose_name

    def normal_info(self):
        data = {}
        data['id'] = str(self.id)
        data['user_id'] = self.user_id
        data['created_at'] = datetime_to_timestamp(self.created_at)
        data['picture_url'] = self.picture_url
        data['comment_count'] = len(self.comment)
        data['desc'] = self.desc
        data['picture_type'] = self.picture_type
        data['price'] = self.price
        data['is_private'] = self.is_private
        data['lock_type'] = self.lock_type
        data['lock_count'] = self.lock_count
        data['purchase_list'] = self.purchase_list
        data['purchase_user_count'] = len(self.purchase_list)
        data['location'] = self.location
        data['mention'] = self.mention
        data['like_user'] = self.like_user
        data['like_count'] = self.like_count
        data['view_count'] = self.view_count
        data['status'] = self.status
        return data

    def real_info(self):
        data = {}
        data['id'] = str(self.id)
        data['user_id'] = self.user_id
        data['created_at'] = datetime_to_timestamp(self.created_at)
        data['picture_url'] = self.picture_real_url
        data['comment_count'] = len(self.comment)
        data['desc'] = self.desc
        data['picture_type'] = self.picture_type
        data['price'] = self.price
        data['is_private'] = self.is_private
        data['lock_type'] = self.lock_type
        data['lock_count'] = self.lock_count
        data['purchase_list'] = self.purchase_list
        data['purchase_user_count'] = len(self.purchase_list)
        data['location'] = self.location
        data['mention'] = self.mention
        data['like_user'] = self.like_user
        data['like_count'] = self.like_count
        data['view_count'] = self.view_count
        data['status'] = self.status
        return data

    @classmethod
    def create_picture(cls, user_id, created_at, picture_url, desc=None, picture_type=None, price=0, is_private=1,
                       lock_type=0, lock_count=0, location=None, mention=None):
        try:
            picture = PictureInfo(
                user_id=user_id,
                created_at=created_at,
                picture_url=picture_url,
                picture_real_url=picture_url,
                comment=None,
                desc=desc,
                picture_type=picture_type,
                price=price,
                is_private=is_private,
                lock_type=lock_type,
                lock_count=lock_count,
                purchase_list=None,
                location=location,
                mention=mention,
                like_user=None,
                like_count=0,
                view_count=0,
                status=0,
            )
            if price != 0:
                picture.picture_url = 'https://hdlive-10048692.image.myqcloud.com/5c8ff8bdc5a3645edcd8d4f9313f29e7'
                picture.save()
                lock = multiprocessing.Lock()
                p = multiprocessing.Process(target=PictureInfo.generate_blurred_picture, args=(lock, picture_url, lock_type, picture.id))
                p.start()

            picture.save()

            user = User.objects.get(id=user_id)
            user.add_experience(2)

        except Exception,e:
            logging.error("create picture error:{0}".format(e))
            return False
        return str(picture.id)

    @classmethod
    def create_comment(cls, picture_id, user_id, reply_id=0, created_at=None, comment=None):
        try:
            picture = PictureInfo.objects.get(id=picture_id)
            comment_id = str(CommentInfo.create_comment(user_id, picture_id, reply_id, created_at, comment))
            if comment_id:
                picture.comment.append(comment_id)
                picture.save()
            else:
                return False
        except Exception,e:
            logging.error("create comment error:{0}".format(e))
            return False
        return True

    @classmethod
    def create_likeuser(cls, picture_id, user_id):
        try:
            picture = PictureInfo.objects.get(id=picture_id)
            is_like = PictureInfo.check_is_like(picture_id, user_id)
            if not is_like:
                picture.like_user.append(user_id)
                picture.like_count += 1
                picture.save()
            else:
                return False
        except Exception,e:
            logging.error("like user error:{0}".format(e))
            return False
        return True

    @classmethod
    def cancel_likeuser(cls, picture_id, user_id):
        try:
            picture = PictureInfo.objects.get(id=picture_id)
            is_like = PictureInfo.check_is_like(picture_id, user_id)
            if is_like:
                picture.like_user.remove(user_id)
                picture.like_count -= 1
                picture.save()
            else:
                return False
        except Exception,e:
            logging.error("cancel like user error:{0}".format(e))
            return False
        return True

    @classmethod
    def check_is_like(cls, picture_id, user_id):
        picture = PictureInfo.objects.get(id=picture_id)
        if int(user_id) in picture.like_user:
            return True
        else:
            return False

    @classmethod
    def purchase_picture(cls, picture_id, user_id):
        try:
            picture = PictureInfo.objects.get(id=picture_id)
            new_url = picture.picture_real_url
            is_purchase = PictureInfo.check_is_purchase(picture_id, user_id)
            if not is_purchase:
                picture.purchase_list.append(int(user_id))
                picture.save()
                UserPurchase.user_purchase_picture(user_id, picture_id)
            else:
                return False, None
        except Exception,e:
            logging.error("purchase picture error:{0}".format(e))
            return False, None
        return True, new_url

    @classmethod
    def check_is_purchase(cls, picture_id, user_id):
        picture = PictureInfo.objects.get(id=picture_id)
        if int(user_id) in picture.purchase_list:
            return True
        else:
            return False

    @classmethod
    def get_picture_list(cls, page=1, page_count=10):
        pictures = PictureInfo.objects.filter(is_private=1, status=0).order_by('-created_at')[(page-1)*page_count:page*page_count]
        return pictures

    @classmethod
    def get_unlock_user_list(cls, picture_id, page=1, page_count=10):
        user_list = PictureInfo.objects.get(id=picture_id).purchase_list[(page-1)*page_count:page*page_count]
        return user_list

    @classmethod
    def get_picture_user(cls, user_id):
        user = User.objects.get(id=user_id)
        return user

    @classmethod
    def add_viewcount(cls, picture_id):
        try:
            picture = PictureInfo.objects.get(id=picture_id)
            picture.view_count = picture.view_count + 1
            picture.save()
        except Exception,e:
            logging.error("view count error:{0}".format(e))
            return False
        return picture.view_count

    @classmethod
    def get_picture_info(cls, picture_id):
        try:
            picture = PictureInfo.objects.get(id=picture_id)
        except Exception,e:
            logging.error("get picture info error:{0}".format(e))
            return False
        return picture

    @classmethod
    def delete_comment(cls, comment_id, user_id):
        try:
            comment = CommentInfo.objects.get(id=comment_id)
            picture = PictureInfo.objects.get(id=comment.picture_id)
            if comment.user_id == int(user_id):
                picture.comment.remove(comment_id)
                picture.save()
                comment.status = 1
                comment.save()
            else:
                return False
        except Exception,e:
            logging.error("delete comment error:{0}".format(e))
            return False
        return True

    @classmethod
    def delete_picture(cls, picture_id, user_id):
        try:
            picture = PictureInfo.objects.get(id=picture_id)
            if picture.user_id == int(user_id):
                picture.status = 1
                picture.save()
            else:
                return False
        except Exception,e:
            logging.error("delete picture error:{0}".format(e))
            return False
        return True

    @classmethod
    def get_user_picture(cls, user_id, page=1, page_count=10):
        pictures = PictureInfo.objects.filter(user_id=user_id, status=0).order_by('-created_at')
        return pictures

    @classmethod
    def generate_blurred_picture(cls, lock, picture_url, lock_type, picture_id):

        from PIL.ExifTags import TAGS
        import urllib2

        img = urllib2.urlopen(picture_url).read()
        name = '/mydata/python/live_video/app/download_pic/1.jpg'
        new_name = '/mydata/python/live_video/app/download_pic/2.jpg'
        pic = open(name, 'wb')
        pic.write(img)
        pic.close()

        radius_list = [30, 40, 50]
        radius = radius_list[lock_type - 1]

        image = Image.open(name)
        exifinfo = image._getexif()

        if exifinfo:
            ret = {}
            for tag, value in exifinfo.items():
                decoded = TAGS.get(tag, tag)
                ret[decoded] = value

            if 'Orientation' not in ret:
                orientation = 1
            else:
                orientation = ret['Orientation']

            if orientation == 1:
                # Nothing
                mirror = image.copy()
            elif orientation == 2:
                # Vertical Mirror
                mirror = image.transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 3:
                # Rotation 180°
                mirror = image.transpose(Image.ROTATE_180)
            elif orientation == 4:
                # Horizontal Mirror
                mirror = image.transpose(Image.FLIP_TOP_BOTTOM)
            elif orientation == 5:
                # Horizontal Mirror + Rotation 90° CCW
                mirror = image.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.ROTATE_90)
            elif orientation == 6:
                # Rotation 270°
                mirror = image.transpose(Image.ROTATE_270)
            elif orientation == 7:
                # Horizontal Mirror + Rotation 270°
                mirror = image.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.ROTATE_270)
            elif orientation == 8:
                # Rotation 90°
                mirror = image.transpose(Image.ROTATE_90)

            mirror.save(name, "JPEG", quality=85)

        image = Image.open(name)
        image = image.filter(MyGaussianBlur(radius=radius))
        image.save(new_name)

        new_pic = open(new_name, 'rb')
        data = UploadImage.push_binary_to_qclude(new_pic, radius)
        new_pic.close()

        new_url = data.get("data", {}).get('download_url', '')
        picture = PictureInfo.objects.get(id=picture_id)
        # picture.picture_url = new_url
        picture.picture_url = User.convert_http_to_https(new_url)
        picture.save()




class MyGaussianBlur(ImageFilter.Filter):
    name = "GaussianBlur"

    def __init__(self, radius=2, bounds=None):
        self.radius = radius
        self.bounds = bounds

    def filter(self, image):
        if self.bounds:
            clips = image.crop(self.bounds).gaussian_blur(self.radius)
            image.paste(clips, self.bounds)
            return image
        else:
            return image.gaussian_blur(self.radius)


class UserPurchase(Document):

    user_id = IntField(verbose_name=u'用户id', required=True)
    purchase_picture = ListField(StringField(verbose_name=u'用户购买的图片列表', default=None))

    class Meta:
        app_label = "picture"
        verbose_name = u"图片"
        verbose_name_plural = verbose_name

    # 创建用户
    @classmethod
    def create_user_purchase(cls, user_id, picture_id):
        try:
            user = UserPurchase(
                user_id=user_id,
                purchase_picture=[picture_id],
            )
            user.save()
        except Exception,e:
            logging.error("create user purchase error:{0}".format(e))
            return False
        return True

    # 添加图片
    @classmethod
    def user_purchase_picture(cls, user_id, picture_id):
        try:
            user = UserPurchase.objects.get(user_id=user_id)
            user.purchase_picture.insert(0, picture_id)
            user.save()
            return True
        except UserPurchase.DoesNotExist:
            status = UserPurchase.create_user_purchase(user_id, picture_id)
            return status


class PicturePriceList(Document):

    picture_price = IntField(verbose_name=u'图片价格列表', required=True)
    price_desc = StringField(verbose_name=u'价格描述', max_length=64, default='')

    class Meta:
        app_label = "picture"
        verbose_name = u"图片价格"
        verbose_name_plural = verbose_name

    # 图片价格列表
    @classmethod
    def create_price(cls, picture_price, price_desc=None):
        try:
            price = PicturePriceList(picture_price=picture_price, price_desc=price_desc)
            price.save()

        except Exception,e:
            logging.error("create price error:{0}".format(e))
            return False
        return True

    @classmethod
    def get_price_list(cls):
        price_list = cls.objects.all()
        return price_list

    @classmethod
    def get_price_desc(cls, picture_price):
        desc = cls.objects.get(picture_price=picture_price).price_desc
        return desc
