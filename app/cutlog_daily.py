# # coding = utf-8

import re
import datetime
import os
from app.originallogs import OriginalLog
from tornado.web import decode_signed_value

cookie_secret = "a3643412085026643529f7fe032646c8"


class CutLog(object):

    LOG_ROOT = "/mydata/logs/nginx/access"
    # LOG_ROOT = "D:/temptemp4.log"
    @classmethod
    def write_orignal_log(cls,time):
	
        log_file = open(os.path.join(cls.LOG_ROOT, "%s.log") % time,"r+")


        ip = r"?P<ip>[\d.]*"
        year = r"?P<year>\d+"
        month = r"?P<month>\d+"
        day = r"?P<day>\d+"
        time = r"?P<time>\S+"
        method = r"?P<method>\S+"
        cookie = r"?P<cookie>[\S\s]+"
        uri = r"?P<uri>\S+"
        argument = r"?P<argument>\S+"

        status_code = r"?P<status>\d+"
        response_time = r"?P<responsetime>[\d.]+"
        ua = r"?P<ua>[\S\s]+"

        p = re.compile(
            r"(%s)\ \"(%s)-(%s)-(%s)\S(%s)\+\S+\ (%s)\ (%s)\ \"(%s)\"\ \"(%s)\"\ \"[\S\s]+\"\ (%s)\ \d+\ (%s)\ \"(%s)\"" % (
            ip, year, month, day, time, method, cookie, uri, argument, status_code, response_time, ua))


        error_num = 0
        num_lines = 0
        for line in log_file:
            m = p.findall(line)
            if not m:
                print line
            log = m[0]
            ori_log = OriginalLog()
            ori_log.ip = log[0]
            ori_log.year = int(log[1])
            ori_log.month = int(log[2])
            ori_log.day = int(log[3])
            ori_log.time = log[4]
            cookie = log[6]
            if "user_token=" in cookie:


                user_token = cookie.split("user_token=")[1].decode("string_escape").split(";")[0]
                if user_token :
                    if user_token[0] == "\"" and user_token[-1] == "\"":
                        user_token = user_token[1:-1]
                    ori_log.user_id = decode_signed_value(secret=cookie_secret, name="user_token", value=user_token)

            ori_log.uri = log[7]
            argument = log[8]
            if argument:
                arg_dic = {}
                args = argument.split("&")
                for arg in args:
                    arg_part = arg.split("=")
                    if arg_part[0] == "_t_" or arg_part[0] == "_s_":
                        continue
                    if arg_part[0] == "guid":
                        ori_log.guid = arg_part[1].decode("string_escape")
                        continue
                    if len(arg_part) == 1:
                        arg_dic[arg_part[0]] = ""
                    else:
                        arg_dic[arg_part[0]] = arg_part[1].decode("string_escape")
                if arg_dic:
                    ori_log.args = arg_dic

            ori_log.status_code = log[9]
            ori_log.request_time = float(log[10])
            ua = log[11]
            if ua and ua != "-":
                try:
                    uas = ua.split(";")
                    ori_log.app_name = uas[0]
                    ori_log.version_name = uas[1]
                    ori_log.platform = uas[2]
                    ori_log.os = uas[3]
                    ori_log.phone_name = uas[4]
                    if uas[2] == "Android":
                        ori_log.channel = uas[5]
                    else:
                        ori_log.channel = "appstore"
                except Exception, e:
                    error_num += 1
                    ori_log.app_name = ""
                    ori_log.version_name = ""
                    ori_log.platform = ""
                    ori_log.os = ""
                    ori_log.phone_name = ""
                    ori_log.channel = ""


            ori_log.save()
            num_lines += 1
            print num_lines
        print error_num

    @classmethod
    def write_all_oringal_log(cls):
        OriginalLog.drop_collection()
        cls.write_orignal_log()



