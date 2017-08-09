#coding=utf-8

import json
from redis_model.redis_client import *
import re

def re_ip():
    ip1 = r"?P<ip1>[\d.]+"
    ip2 = r"?P<ip2>[\d.]+"
    loc1 = r"?P<loc1>[\S]+"
    loc2 = r"?P<loc2>[\S]+"

    p = re.compile(r"(%s)[\s]*(%s)[\s]*(%s)[\s]*(%s)" % (ip1, ip2, loc1, loc2))

    return p

def readip():
    file_name = "/Users/biweibiren/Downloads/ip.txt"

    with open(file_name, 'r') as f:
        print 1
        num = 0
        for line in f.readlines():
            m = p.findall(line)
            record = m[0]
            ip1 = record[0]
            ip2 = record[1]
            ip1s = ip1.split(".")
            ip2s = ip2.split(".")
            loc1 = record[2]
            if loc1.startswith("北京") or loc1.startswith("上海") or loc1.startswith("中国"):
                pass
        print num

def put():
    """
     ip库中截取的ip1 和 ip2 看是否有前两位不一样的
     第三位不一样 则 遍历所有第三位中间的存入redis
     以第三位做key 值位一个map map的key为第四位 值为地域
    """
    p = re_ip()
    file_name = "/mydata/downloads/ip.txt"

    with open(file_name, 'r') as f:
        print 1
        num = 0
        for line in f.readlines():
            m = p.findall(line)
            record = m[0]
            ip1 = record[0]
            ip2 = record[1]
            ip1s = ip1.split(".")
            ip2s = ip2.split(".")
            loc1 = record[2]
            if loc1.startswith("北京") or loc1.startswith("上海") or loc1.startswith("中国"):
                print line
                put_ip_to_redis(ip1,ip2,loc1)


def put_ip_to_redis(ip1,ip2,loc1,loc2=""):
    """key 为ip 前三部分"""
    ip1s = ip1.split(".")
    ip2s = ip2.split(".")

    ip1s = map(lambda x : int(x), ip1s)
    ip2s = map(lambda x : int(x), ip2s)

    for i1 in range(ip1s[0], ip2s[0]+1):
        l1 = 0
        r1 = 255
        if i1 == ip1s[0]:
            l1 = ip1s[1]
        if i1 == ip2s[0]:
            r1 = ip2s[1]

        for i2 in range(l1, r1+1):
            l2 = 0
            r2 = 255
            if i2 == l1 and i1 == ip1s[0]:
                l2 = ip1s[2]
            if i2 == r1 and i1 == ip2s[0]:
                r2 = ip2s[2]
            for i3 in range(l2, r2+1):
                s = str(i1)+"."+str(i2) + "." + str(i3)
                l3 = 0
                r3 = 255
                if i3 == l2 and i2 == ip1s[1] and i1 == ip1s[0]:
                    l3 = ip1s[3]
                if i3 == r2 and i2 == ip2s[1] and i1 == ip2s[0]:
                    r3 = ip2s[3]

                if loc1.startswith("北京") or loc1.startswith("中国"):
                    v = "北京"
                    # todo put l3_r3_v to redis

                    RQueueClient.getInstance().redis.lpush(s, str(l3) + "_" + str(r3) + "_" + v)
                    #RQueueClient.getInstance().redis.delete(s)
                if loc1.startswith("上海"):
                    v = "上海"
                    #RQueueClient.getInstance().redis.delete(s)
                    RQueueClient.getInstance().redis.lpush(s, str(l3) + "_" + str(r3) + "_" + v)