# coding=utf-8
from app.customer.models.bottle_message import BottleMessageText


def add_bottle_message():
    anchor_text = [
        "你做什么的呀？帅哥",
        "聊聊呗？我很无聊~",
        "男朋友出差了，一个人好无聊，来和我视频聊天吧",
        "你最喜欢聊什么话题，我来满足你",
        "唔，帅哥，想语聊吗",
        "各种爱，你想来吗",
        "我的声音特别好听，想让我哄睡觉吗",
        "你是土豪哥哥吗？我想蹂躏你",
        "我很高冷，从来不主动，需要你来引导",
        "我想和你聊聊比较隐私的话题",
        "最近我很烦，需要人来安慰",
        "我喜欢交友，你喜欢吗~",
        "我失恋了，你来陪陪我吧",
        "找大叔，带给我温暖和安全感",
        "让我来给你抚慰吧",
        "异地恋能接受吗",
        "不走心不走心，走肾了，快来吧",
        "帅哥，你想怎么玩",
        "只视频不聊天，快来快来",
        "打扮再美，穿的再贵，都是幌子，视频有料才是真的",
        "一个人睡觉~zZ",
        "求关注~求视频~",
        "如果喜欢我。直接视频发给我!"
        "一个人在无聊，在等你呢~",
        "哥哥无聊吗？跟我聊天吧~",
        "爱的~我在呢~来聊天~",
        "宝很无聊..",
        "不粘人 我很听话",
        "在吗？我们聊点什么吧~",
        "哈喽 在干嘛 ",
        "我很乖 你说我就敢做",
        "孤独难耐，可有同感。。。",
        "你的小可爱上线啦",
        "想不想看我新买的睡衣~",
        "好无聊，来视频撩",
        "么么哒~快来视频~",
        "嗨皮嗨皮",
        "来呀，造作呀",
        "亲爱的，我醒了，猜猜我在想什么",
        "自己在家。视频陪我好么。。",
        "哥哥。视频吗~等你哦~",
        "来视频吧~有惊喜~~",
        "哥哥~视频陪你好吗~",
        "视频聊天吗？",
        "我觉得如果不是和你聊天，我就无聊死了",
        "来搞点事情么？",
        "一个人无聊不，打个视频聊会儿天吧~",
        "野蛮女友，不给我打视频就打你",
        "视频秒接，你懂我的",
        "喜欢我就来视频吧，视频什么你懂哒",
        "直接视频，我很乖哒",
        "视频撩我，在线哦",
        "帅哥哥，我很乖，一心一意喜欢你",
        "哥哥，发我视频吧，人家等你呢",
        "好哥哥，求关注求花花，我会很温柔哒~",
        "帅哥哥，我是一株含苞待放的小花花，视频看我吧",
        "我是你的菜嘛，视频撩我吧`",
        "视频表演，有你想看的",
        "不管相隔多远，我们视频相见~",
        "你是个成熟的人嘛，希望你的成熟可以包容我的青涩",
        "别的小朋友都回家了，你什么时候来接我",
        "求关注，来视频，给你一个不一样的女朋友",
        "随心所欲，语音视频，我抱着手机等你~",
        "可以认识你嘛，视频开车兜兜风~",
        "工作辛苦了，让我给你放~松一下吧",
        "聊骚，聊污，视频听你的",
        "我的声音，让你麻酥酥~",
        "视频直接发，语音等你打",
        "家养小兔兔，爱吃萝卜爱吃菜",
        "帅锅，听说你不吸烟是吗？",
        "我有70是种方式跟你打开视频，一种是陪你聊侃大山，还有69",
        "颜值在线，视频有料，信我就来~",
        "我们的故事开始只差一个视频",
        "一直惦记着跟你视频，脸红心跳~",
        "等你打开视频，也许会想起在哪个路口见过我",
        "我做事就是精益求精",
        "不打视频我就不乖，咬你",
        "我就是我，是色色的烟火~",
        "天天在线，聊你想聊，看你想看~",
        ]
    user_text = [

    ]
    label = 0
    BottleMessageText.objects.filter(gender=1).delete()
    for text in anchor_text:
        label += 1
        BottleMessageText.create_message_text(label, text, 0, 1)

    label = 3000

    for text in user_text:
        label += 1
        BottleMessageText.create_message_text(label, text, 1, 2)
