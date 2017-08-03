# coding=utf-8
from app.customer.models.vip import *


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)

# 用户动态 (朋友圈)
class UserMoment(Document):
    user_id = IntField(verbose_name=u'用户id', required=True)
    like_count = IntField(verbose_name=u'用户点赞数', required=True)
    like_user_list = ListField(IntField(verbose_name=u"用户id"), verbose_name=u"点赞用户_id")
    comment_count = IntField(verbose_name=u"用户评论数")
    img_list = ListField(verbose_name=u"图片列表")
    content = StringField(verbose_name=u"用户动态的文字内容")
    create_time = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())
    show_status = IntField(verbose_name=u"是否展示", default=1)  # 1:展示  2:数美屏蔽  3:举报  4:数美部分屏蔽  5:数美鉴定中
    delete_status = IntField(verbose_name=u"删除状态", default=1)  # 1:未删除  2:删除
    ispass = IntField(verbose_name=u"是否忽略")  # 1:忽略  2:未忽略
    type = IntField(verbose_name=u"动态的类型")  # 1:普通动态  2:精华照片动态  3:私房视频

    @classmethod
    def create(cls, user_id, picture_urls, content):
        user_moment = UserMoment()
        user_moment.user_id = user_id
        user_moment.like_count = 0
        user_moment.like_user_list = []
        user_moment.comment_count = 0
        picture_url_list = picture_urls.split(',')
        if picture_url_list:
            for picture_url in picture_url_list:
                if picture_url:
                    pic_url = User.convert_http_to_https(picture_url)
                    dict = {
                        "url": pic_url,
                        "status": 1
                    }
                    user_moment.img_list.append(dict)
        user_moment.content = content
        user_moment.show_status = 5
        user_moment.delete_status = 1
        user_moment.ispass = 2
        user_moment.type = 1
        user_moment.create_time = datetime.datetime.now()
        user_moment.save()

        MessageSender.send_picture_detect(pic_url="", user_id=0, pic_channel=0, source=2, obj_id=str(user_moment.id))

    @classmethod
    def update_like(cls, status, user_id, moment_id):
        user_moment = UserMoment.objects.filter(id=moment_id).first()
        like_user_list = user_moment.like_user_list
        if status == 1:
            # 点赞

            if user_id not in like_user_list:
                user_moment.update(inc__like_count=1)
                user_moment.update(push__like_user_list=user_id)
        elif status == 2:
            # 取消点赞
            user_moment.update(dec__like_count=1)
            if user_id in like_user_list:
                user_moment.update(pull__like_user_list=user_id)

    def normal_info(self):
        user_id = self.user_id
        user = User.objects.filter(id=user_id).first()

        head_image = user.image
        age = User.get_age(user.birth_date)
        create_time = UserMoment.get_time(self.create_time)
        date_time = self.create_time.strftime('%Y-%m-%d')
        imgs = self.img_list
        img_list = []

        if self.type == 2:
            count = len(imgs)
            if count:
                for i in range(count):
                    img_list.append("")
        else:
            if imgs:
                for img in imgs:
                    for k,v in img.items():
                            if v == 1:
                                img_list.append(img["url"])
        moment_look = UserMomentLook.objects.filter(user_moment_id=str(self.id)).first()
        look_count = 0
        if moment_look:
            look_user_ids = moment_look.user_id_list
            look_count = len(look_user_ids)
        if user:
            data = {
                "moment_id": str(self.id),
                "user_id": user.id,
                "gender": user.gender_desc,
                "head_image": head_image,
                "nickname": user.nickname,
                "age": age,
                "create_time": create_time,
                "img_list": img_list,
                "comment_count": self.comment_count,
                "like_count": self.like_count,
                "type": self.type,
                "look_count": look_count,
                "content": self.content,
                "date_time": date_time
            }
            user_vip = UserVip.objects.filter(user_id=user_id).first()
            if user_vip:
                vip = Vip.objects.filter(id=user_vip.vip_id).first()
                data["vip_icon"] = vip.icon_url

            return data

    #  动态发布规则
    @classmethod
    def check_moment_count(cls, user):
        """
        VIP：
        1）动态：每日发布5条
        播主VIP：
        1）动态：每日发布15条
        播主：
        1）动态：每日发布10条
        普通用户：
        1）动态：每日发布3条
        """
        vip_count = 5
        anchor_vip_count = 15
        anchor_count = 10
        user_count = 3
        is_video = user.is_video_auth
        user_vip = UserVip.objects.filter(user_id=user.id).first()

        now = datetime.datetime.now()
        starttime = now.strftime("%Y-%m-%d 00:00:00")
        endtime = now.strftime('%Y-%m-%d 23:59:59')
        today_moment_count = UserMoment.objects.filter(user_id=user.id, show_status__ne=2, delete_status=1,
                                                       create_time__gte=starttime, create_time__lte=endtime).count()
        code = 1
        message = ""
        if user_vip:
            if int(is_video) == 1:
                # 播住vip
                if today_moment_count >= anchor_vip_count:
                    code = 2
                    message = u"播主VIP,每日动态发布最多15条"
            else:
                # 用户vip
                if today_moment_count >= vip_count:
                    code = 2
                    message = u"用户VIP,每日动态发布最多5条"
        else:
            if int(is_video) == 1:
                # 播主:
                if today_moment_count >= anchor_count:
                    code = 2
                    message = u"播主每日动态发布最多10条"
            else:
                # 普通用户
                if today_moment_count >= user_count:
                    code = 2
                    message = u"普通用户每日动态发布最多3条"

        return code, message

    @classmethod
    def get_time(cls, date_time):
        now = datetime.datetime.now()
        second = time.mktime(now.timetuple()) - time.mktime(date_time.timetuple())

        if second <= 0:
            second = 0

        #  时间格式
        if second == 0:
            interval = "刚刚"
        elif second < 30:
            interval = str(int(second)) + "秒以前"
        elif second >= 30 and second < 60:
            interval = "半分钟前"
        elif second >= 60 and second < 60 * 60:
            #  大于1分钟 小于1小时
            minute = int(second / 60)
            interval = str(minute) + "分钟前"
        elif second >= 60 * 60 and second < 60 * 60 * 24:
            #  大于1小时 小于24小时
            hour = int((second / 60) / 60)
            interval = str(hour) + "小时前"
        elif second >= 60 * 60 * 24 and second <= 60 * 60 * 24 * 2:
            #  大于1D 小于2D
            interval = "昨天" + date_time.strftime('%H:%M')
        elif second >= 60 * 60 * 24 * 2 and second <= 60 * 60 * 24 * 7:
            #  大于2D小时 小于 7天
            day = int(((second / 60) / 60) / 24)
            interval = str(day) + "天前"
        elif second <= 60 * 60 * 24 * 365 and second >= 60 * 60 * 24 * 7:
            #  大于7天小于365天
            interval = date_time.strftime('%Y-%m-%d %H:%M')
        elif second >= 60 * 60 * 24 * 365:
            #  大于365天
            interval = date_time.strftime('%Y-%m-%d %H:%M')
        else:
            interval = "0"
        return interval


class UserComment(Document):
    user_moment_id = StringField(verbose_name=u"用户发布动态的 id", max_length=64)
    user_id = IntField(verbose_name=u'用户id', required=True)
    create_time = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())
    content = StringField(verbose_name=u"评论内容", max_length=512)
    comment_type = IntField(verbose_name=u"评论类型")  # 1:评论动态  2:回复评论
    reply_user_id = IntField(verbose_name=u"回复用户id")
    delete_status = IntField(verbose_name=u"删除状态", default=1)  # 1:未删除  2:删除


    @classmethod
    def create_comment(cls, moment_id, user_id, content, comment_type, reply_user_id):
        user_coment = UserComment()
        user_coment.user_moment_id = moment_id
        user_coment.user_id = user_id
        user_coment.content = content
        user_coment.comment_type = comment_type
        if comment_type == 2:
            user_coment.reply_user_id = reply_user_id
        user_coment.delete_status = 1
        user_coment.create_time = datetime.datetime.now()
        user_coment.save()

        # 更新评论数
        user_moment = UserMoment.objects.filter(id=str(moment_id)).first()
        user_moment.update(inc__comment_count=1)
        return user_coment

    @classmethod
    def delete_comment(cls, comment_id, user_id):
        try:
            user_comment = UserComment.objects.filter(id=str(comment_id)).first()
            if user_comment:
                if user_comment.user_id == int(user_id):
                    user_comment.delete_status = 2
                    user_comment.save()
                    # 更新评论数
                    comment_count = len(UserComment.objects.filter(user_moment_id=user_comment.user_moment_id, delete_status=1))
                    user_moment = UserMoment.objects.filter(id=user_comment.user_moment_id).first()
                    user_moment.update(set__comment_count=comment_count)
                    return True
                else:
                    return False
        except Exception,e:
            logging.error("delete comment error:{0}".format(e))
            return False
        return True


    def normal_info(self):
        user = User.objects.filter(id=self.user_id).first()
        if user:
            nickname = user.nickname
            head_image = user.image
            create_time = UserMoment.get_time(self.create_time)
            data = {
                "moment_id": self.user_moment_id,
                "comment_id": str(self.id),
                "user_id": user.id,
                "nickname": nickname,
                "head_image": head_image,
                "create_time": create_time,
                "comment_content": self.content,
                "comment_type": self.comment_type,
            }
            user_vip = UserVip.objects.filter(user_id=user.id).first()
            if user_vip:
                vip = Vip.objects.filter(id=user_vip.vip_id).first()
                data["vip_icon"] = vip.icon_url

            if self.comment_type == 2:
                reply_user = User.objects.filter(id=self.reply_user_id).first()
                if reply_user:
                    reply_nickname = reply_user.nickname
                else:
                    reply_nickname = ""
                data["reply_user_id"] = self.reply_user_id
                data["reply_nickname"] = reply_nickname
            return data


class UserMomentLook(Document):
    user_moment_id = StringField(verbose_name=u"用户发布动态的 id", max_length=64)
    user_id_list = ListField(IntField(verbose_name=u"用户id"), verbose_name=u"看过用户_id")

    @classmethod
    def inc_look(cls, user_id, user_moment_id):
        moment_look = UserMomentLook.objects.filter(user_moment_id=user_moment_id).first()
        user_id = int(user_id)
        if not moment_look:
            new_look = UserMomentLook()
            new_look.user_moment_id = user_moment_id
            new_look.user_id_list = []
            new_look.user_id_list.append(user_id)
            new_look.save()
        else:
            user_ids = moment_look.user_id_list
            if user_id not in user_ids:
                moment_look.update(push__user_id_list=user_id)


class UserMomentReport(Document):
    user_moment_id = StringField(verbose_name=u"用户发布动态的 id", max_length=64)
    user_id = IntField(verbose_name=u'举报人id', required=True)
    create_time = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())
    report_text = StringField(verbose_name=u"举报内容", max_length=512)
    report_id = IntField(verbose_name=u"被举报人ID")
    status = IntField(verbose_name=u"处理状态", default=0)  # 0：未处理 1：已处理 2:忽略
    update_time = DateTimeField(verbose_name=u"处理时间")
    operator = StringField(verbose_name=u"操作人")
    operaterecord = StringField(verbose_name=u"操作记录")

    @classmethod
    def create_report_record(cls, user_moment_id, user_id, report_text, report_id):
        obj_ = cls()
        obj_.user_moment_id = user_moment_id
        obj_.user_id = user_id
        obj_.report_text = report_text
        obj_.report_time = datetime.datetime.now()
        obj_.report_id = report_id
        obj_.status = 0
        obj_.save()


class UserCommentReport(Document):
    comment_id = StringField(verbose_name=u"社区评论 id", max_length=64)
    user_id = IntField(verbose_name=u'举报人id', required=True)
    create_time = DateTimeField(verbose_name=u"创建时间", default=datetime.datetime.now())
    report_text = StringField(verbose_name=u"举报内容", max_length=512)
    report_id = IntField(verbose_name=u"被举报人ID")
    status = IntField(verbose_name=u"处理状态", default=0)  # 0：未处理 1：已处理 2:忽略
    update_time = DateTimeField(verbose_name=u"处理时间")
    operator = StringField(verbose_name=u"操作人")
    operaterecord = StringField(verbose_name=u"操作记录")

    @classmethod
    def create_report_record(cls, comment_id, user_id, report_text, report_id):
        obj_ = cls()
        obj_.comment_id = comment_id
        obj_.user_id = user_id
        obj_.report_text = report_text
        obj_.report_time = datetime.datetime.now()
        obj_.report_id = report_id
        obj_.status = 0
        obj_.save()


