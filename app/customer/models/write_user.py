# -*- coding: utf-8 -*-
from app.customer.models.user import *
from app.customer.models.account import Account
from app.customer.models.personal_tags import *
import datetime
import time

name_list = ["小玲子", "小嗨妞", "粉肉小笼包", "寂寞小姑娘", "坏老婆", "小老婆", "薛瑾芯", "小坏蛋", "胸大@熊大", "诗颖", "娜贝尔", "塔玛蒂", "茉莉娘", "清软", "金克丝", "翘臀mm", "小甜心", "大C小污婆", "糖糖", "Cup图图", "玉米棒棒", "陪你入眠", "大奶妹", "美人儿", "青春不设防", "初见", "米诺诺", "Sun"]

desc_list = [
    "请你不要吃掉我~", 
    "挑逗你的神经 让你欲罢不能", 
    "小笼包喜欢大香蕉", 
    "开心就好~", 
    "销魂的声音，来电任调教。", 
    "来一发，各种角色各种爱。", 
    "给你不一样的陪伴~", 
    "我要我要我还要~", 
    "胸大的熊大，这让人怎么活。", 
    "上了我的床，你就是我的人了。", 
    "喜欢后入，等你来哦~", 
    "外表清纯，内心狂热。", 
    "我喜欢你是来自心脏而不是来自口腔", 
    "声音暖你，哄你睡觉。", 
    "陪你度过漫长的夜。", 
    "吸精~小妖女~", 
    "用声音为你解压，让你没烦恼", 
    "哥哥~我们来彻夜长聊嘛~期待来电", 
    "大哥哥~快来嘛~我等你哦", 
    "我会变很多魔术~像香蕉变大术~嗯", 
    "别急~慢慢来~", 
    "哥哥，我好寂寞，给人家打电话嘛", 
    "给你想要的一切，来电惊喜满足你", 
    "一个人在家好寂寞，来找我吧！", 
    "聊一切你想聊的话题，让你随心所欲", 
    "你的身心我来呵护，快到怀里来", 
    "满足你一切幻想，来电有福利", 
    "陪你畅聊，让你开心，嗯~啊"
]

audio_list = ["https://heydo-10048692.file.myqcloud.com/record/introduce/2524/2524_1484645348.mp3", "https://heydo-10048692.file.myqcloud.com/record/introduce/2529/2529_1484645352.mp3", "https://heydo-10048692.file.myqcloud.com/record/introduce/2525/2525_1484645349.mp3", "https://heydo-10048692.file.myqcloud.com/record/introduce/2532/2532_1484645353.mp3", "https://heydo-10048692.file.myqcloud.com/record/introduce/2530/2530_1484645352.mp3", "https://heydo-10048692.file.myqcloud.com/record/introduce/2528/2528_1484645351.mp3", "https://heydo-10048692.file.myqcloud.com/record/introduce/2537/2537_1484645356.mp3", "https://heydo-10048692.file.myqcloud.com/record/introduce/2526/2526_1484645349.mp3", "https://heydo-10048692.file.myqcloud.com/record/introduce/2539/2539_1484645357.mp3", "https://heydo-10048692.file.myqcloud.com/record/introduce/2540/2540_1484645357.mp3", "https://heydo-10048692.file.myqcloud.com/record/introduce/2538/2538_1484645356.mp3", "https://heydo-10048692.file.myqcloud.com/record/introduce/2535/2535_1484645355.mp3", "https://heydo-10048692.file.myqcloud.com/record/introduce/2536/2536_1484645355.mp3", "https://heydo-10048692.file.myqcloud.com/record/introduce/2534/2534_1484645354.mp3", "https://heydo-10048692.file.myqcloud.com/record/introduce/2533/2533_1484645354.mp3", "https://heydo-10048692.file.myqcloud.com/record/introduce/2554/2554_1484645363.mp3", "https://heydo-10048692.file.myqcloud.com/record/introduce/2522/2522_1484645348.mp3", "https://heydo-10048692.file.myqcloud.com/record/introduce/2556/2556_1484645364.mp3", "https://heydo-10048692.file.myqcloud.com/record/introduce/2515/2515_1484645348.mp3", "https://heydo-10048692.file.myqcloud.com/record/introduce/2541/2541_1484645358.mp3", "https://heydo-10048692.file.myqcloud.com/record/introduce/2542/2542_1484645358.mp3", "https://heydo-10048692.file.myqcloud.com/record/introduce/2543/2543_1484645359.mp3", "https://heydo-10048692.file.myqcloud.com/record/introduce/2544/2544_1484645359.mp3", "https://heydo-10048692.file.myqcloud.com/record/introduce/2551/2551_1484645362.mp3", "https://heydo-10048692.file.myqcloud.com/record/introduce/2545/2545_1484645360.mp3", "https://heydo-10048692.file.myqcloud.com/record/introduce/2547/2547_1484645360.mp3", "https://heydo-10048692.file.myqcloud.com/record/introduce/2550/2550_1484645362.mp3", "https://heydo-10048692.file.myqcloud.com/record/introduce/2552/2552_1484645363.mp3" ]

image_list = [
    "https://heydopic-10048692.image.myqcloud.com/956db975218456db55b27e4572584af3", 
    "https://heydopic-10048692.image.myqcloud.com/3bdad6130222a4b2a592f64c980da9d6", 
    "https://heydopic-10048692.image.myqcloud.com/ee5388754da1a427b934226935320251", 
    "https://heydopic-10048692.image.myqcloud.com/1ae74fad04776ffcac27d1095cf43c45", 
    "https://heydopic-10048692.image.myqcloud.com/373fe55f3279dd511a82087869bf1809", 
    "https://heydopic-10048692.image.myqcloud.com/1a237912c2604c3cd5efa83920507e22", 
    "https://heydopic-10048692.image.myqcloud.com/59474131c28ee172fff02fa44ff799ec", 
    "https://heydopic-10048692.image.myqcloud.com/031bd7944d08c57282a055bff4f8742a", 
    "https://heydopic-10048692.image.myqcloud.com/e643ce509b8124acd8646407a0bfc24a", 
    "https://heydopic-10048692.image.myqcloud.com/f730fc5aeaaba3493579aec03dd4d3d9", 
    "https://heydopic-10048692.image.myqcloud.com/4cbc3636b9ff3adf0024335fa18fb22f", 
    "https://heydopic-10048692.image.myqcloud.com/c317099f28d8d27a71a86b005d7ade95", 
    "https://heydopic-10048692.image.myqcloud.com/0f7b743b34eaef180f25a109a7396e89", 
    "https://heydopic-10048692.image.myqcloud.com/db3041ef32b374e8e8e3025abf52265a", 
    "https://heydopic-10048692.image.myqcloud.com/8612c0252aa2a541f1f94a103e209095", 
    "https://heydopic-10048692.image.myqcloud.com/396d439b01425fad97e9b0da54eeb58a", 
    "https://heydopic-10048692.image.myqcloud.com/38e78790f6492d26df7a983f0b1d2d87", 
    "https://heydopic-10048692.image.myqcloud.com/3cdfdf4a3b028a35e3f77eeaf554a4b8", 
    "https://heydopic-10048692.image.myqcloud.com/2fe6516981b40058a1b7c83dd3f16699", 
    "https://heydopic-10048692.image.myqcloud.com/a3786b17e450317f405beaae1fc5c17b", 
    "https://heydopic-10048692.image.myqcloud.com/2a974c785460f4a2484d5363b9e4a717", 
    "https://heydopic-10048692.image.myqcloud.com/1dd80a1683e2a633f3b7ab77a534bf31", 
    "https://heydopic-10048692.image.myqcloud.com/9b6c07826aca164efc79adae2b3bee3b", 
    "https://heydopic-10048692.image.myqcloud.com/8d0a7c512d574951ef3991b6b1c75ad0", 
    "https://heydopic-10048692.image.myqcloud.com/c1c3cb046dd78f8d4a59c510aa1bd956", 
    "https://heydopic-10048692.image.myqcloud.com/4b63ea3d38fbae972a950c1e1f098202", 
    "https://heydopic-10048692.image.myqcloud.com/18ef2f1c1891be8548b6099cb3af58f2", 
    "https://heydopic-10048692.image.myqcloud.com/5692076e512954aef929831eba743595", 
    "https://heydopic-10048692.image.myqcloud.com/3d659f21f22b0de03abb5336ef69df4a", 
    "https://heydopic-10048692.image.myqcloud.com/c6c45e7d01f998ddb91bd3560a534076", 
    "https://heydopic-10048692.image.myqcloud.com/1603ea891d2a819a842c41a09af97ba5", 
    "https://heydopic-10048692.image.myqcloud.com/6831822915e0c57729cb3f5e5428239e", 
    "https://heydopic-10048692.image.myqcloud.com/7951f2dc7a8294edd76947c3ce4a72c0", 
    "https://heydopic-10048692.image.myqcloud.com/20e42ab6cb77a3fd231d8e6ecd33918f", 
    "https://heydopic-10048692.image.myqcloud.com/73e946738218dd0fd4913076f315fef8", 
    "https://heydopic-10048692.image.myqcloud.com/b3c4ea81a431e72636f52ad9e64f8f1b", 
    "https://heydopic-10048692.image.myqcloud.com/d438e37c56da3a1b176874e3430697af"
]

birth_list = [
    "1994-09-12",
    "1995-03-27",
    "1993-01-12",
    "1996-03-23",
    "1997-01-22",
    "1991-05-12",
    "1996-08-19",
    "1992-11-23",
    "1993-12-24",
    "1994-09-23",
    "1995-07-02",
    "1996-08-21",
    "1997-11-12",
    "1998-12-01",
    "1997-04-01",
    "1996-05-06",
    "1995-06-07",
    "1994-07-09",
    "1993-05-29",
    "1992-10-18",
    "1991-08-02",
    "1992-12-13",
    "1993-06-23",
    "1994-09-03",
    "1995-02-07",
    "1996-10-21",
    "1997-05-07",
    "1996-10-18",
]

phone_list = [
    91283785769,
    93746582648,
    98274526475,
    91635856732,
    93746284756,
    93647587263,
    99727663523,
    92762834642,
    93351384124,
    97367623352,
    97367365123,
    93763675172,
    93463746732,
    94763725265,
    93476735134,
    94874876234,
    97675232445,
    97867523244,
    97657838066,
    97753846284,
    95374828453,
    97462748562,
    94762248571,
    97645776243,
    97532846245,
    93253747183,
    95327273623,
    96556445623
]

def write_user():
    for n in range(0, 28):
        t = datetime.datetime.now().timetuple()
        timeStamp = str(int(time.mktime(t)))
        openid = "chatpa_childuser1234" + timeStamp

        user = User(
            id=User.objects.all().count()+1,
            openid=openid,
            is_block=0,
            user_type=2,
            nickname=name_list[n],
            desc=desc_list[n],
            phone="",
            gender=2,
            image=image_list[n],
            constellation=u'摩羯座',
            occupation="",
            blood_type="",
            birth_date=datetime.date(1995, 1, 1),
            emotional="",
            total_time=0,
            total_call_time=0,
            total_income=0,
            total_amount=0,
            audio_room_id="",
            now_price=0,
            listen_url=audio_list[n],
            url_duration=5,
            created_at=datetime.datetime.now(),
            source=0,
            platform=2,
            channel="child",
            experience=0,
            ticket=0,
            cost=0,
        )
        user_identity = LuckIDInfo.objects.filter(id_assign=0, id_type=0).order_by('id').first()
        user_identity.id_assign = 1
        user_identity.save()
        user.identity = int(user_identity.user_id)
        user.save()
        
        account = Account(
            user=user,
            diamond=0,
            last_diamond=0,
            update_time=datetime.datetime.now(),
        )
        account.save()
        print user.id
        time.sleep(1)

def update_user():
    users = User.objects.filter(user_type=2)
    i = 0
    for user in users:
        user.birth_date = datetime.datetime.strptime(birth_list[i], '%Y-%m-%d')
        user.constellation = User.zodiac(birth_list[i])
        user.phone = str(phone_list[i])
        user.save()
        i += 1

    for phone in phone_list:
        phone_password = PhonePassword(phone=str(phone), password=u"25d55ad283aa400af464c76d713c07ad")
        phone_password.save()



tag_list = [
    "丝袜诱惑,器大活好,角色扮演",
    "专注开车,老司机,交换秘密",
    "污妖王,丝袜诱惑,甜美声优",
    "器大活好,老司机,角色扮演",
    "专注开车,污妖王,交换秘密",
    "丝袜诱惑,专注开车,清新可人",
    "器大活好,专注开车,女王大人",
    "老司机,丝袜诱惑,清新可人",
    "污妖王,丝袜诱惑,霸道御姐",
    "丝袜诱惑,器大活好,女王大人",
    "污妖王,老司机,丝袜诱惑",
    "器大活好,专注开车,清纯学妹",
    "交换秘密,傲娇萝莉,角色扮演",
    "角色扮演,甜美声优,丝袜诱惑",
    "文艺青年,清纯学妹,交换秘密",
    "角色扮演,交换秘密",
    "女王大人,丝袜诱惑",
    "撩妹专家,甜美声优,傲娇萝莉",
    "角色扮演,丝袜诱惑",
    "清纯学妹,甜美声优,交换秘密",
    "霸道御姐,丝袜诱惑,撩妹专家",
    "角色扮演,清纯学妹,文艺青年",
    "污妖王,交换秘密",
    "清新可人,清纯学妹,甜美声优",
    "老司机,丝袜诱惑",
    "污妖王,丝袜诱惑",
    "专注开车,清纯学妹,老司机,角色扮演",
    "清纯学妹,交换秘密,甜美声优,傲娇萝莉"
]

def update_tags():
    users = User.objects.filter(user_type=2)
    i = 0
    for user in users:
        UserTags.update_usertags(user_id=user.id, tag_str=tag_list[i])
        i += 1

location_list = [
"天津市",
"重庆市",
"上海市",
"石家庄市",
"沧州市",
"呼和浩特市",
"赤峰市",
"沈阳市",
"长春市",
"白山市",
"哈尔滨市",
"苏州市",
"连云港市",
"杭州市",
"温州市",
"合肥市",
"阜阳市",
"南昌市",
"新余市",
"青岛市",
"威海市",
"郑州市",
"武汉市",
"昆明市",
"长沙市",
"广州市",
"成都市",
"西安市",
]

def update_location():
    users = User.objects.filter(user_type=2)
    i = 0
    for user in users:
	user.province = ""
        user.city = location_list[i]
        user.district = ""
        user.save()
        i += 1



