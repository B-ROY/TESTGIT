# coding=utf-8

from user import User
from mongoengine import *
from base.settings import CHATPAMONGO


connect(CHATPAMONGO.db, host=CHATPAMONGO.host, port=CHATPAMONGO.port, username=CHATPAMONGO.username,
        password=CHATPAMONGO.password)

#将所有推荐数据全部放在一张表中
class Recommend(Document):

    RecommendType = {
        (1, u"声优推荐"),
        (2, u"视频推荐"),
        (3, u"美女来了推荐")
    }

    user_id = StringField(verbose_name=u"用户id")
    recommend_type = IntField(verbose_name=u"推荐类型", choices=RecommendType)
    seq = IntField(verbose_name=u"推荐序号")

    @classmethod
    def create_recommend_item(cls, user_id=user_id, recommend_type=recommend_type, seq=seq):
        try:
            recommend_item = Recommend.objects.get(user_id=user_id)
            recommend_item.recommend_type = recommend_type
            recommend_item.seq = seq
        except Recommend.DoesNotExist:
            recommend_item = Recommend(user_id=user_id,
                                   recommend_type=recommend_type, seq=seq)
            recommend_item.save()

    @classmethod
    def get_recommend_list(cls):
        reccomand_list = Recommend.objects.get()
        audio_list = []
        video_list = []
        beauty_list = []
        for recommend_item in reccomand_list:
            if recommend_item.seq == 1:
                audio_list.append(recommend_item)
            elif recommend_item.seq == 2:
                video_list.append(recommend_item)
            else:
                beauty_list.append(recommend_item)

        return audio_list, video_list, beauty_list

    @classmethod
    def get_recommend_audio_list:





