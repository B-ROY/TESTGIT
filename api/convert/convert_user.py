__author__ = 'zen'


def convert_user(user, with_detail=False):
    return user.get_normal_dic_info()


def convert_audioroom(audioroom, with_detail=False):
    return audioroom.normal_info()


def convert_videoroom(videoroom, with_detail=False):
    return videoroom.normal_info()


def convert_picture(picture, with_detail=False):
    return picture.normal_info()


def convert_real_picture(picture, with_detail=False):
    return picture.real_info()


def convert_comment(comment, with_detail=False):
    return comment.normal_info()
