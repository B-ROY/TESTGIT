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

def convert_activity(activity, with_detail=False):
    return activity.normal_info()

def convert_vip(vip, with_detail=False):
    return vip.normal_info()

def convert_tools(tools, with_detail=False):
    return tools.normal_info()

def convert_columns(column, with_detail=False):
    return column.normal_info()

def convert_user_moment(user_moment, with_detail=False):
    return user_moment.normal_info()

def convert_comment(comment, with_detail=False):
    return comment.normal_info()

def convert_vip_privilege(privilege, with_detail=False):
    return privilege.normal_info()

def convert_about_me_message(message, user_id, with_detail=False):
    return message.normal_info(user_id)
