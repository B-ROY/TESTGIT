import hashlib
import hmac
from hashlib import sha1
import sys
import time
import ctypes


def generate_public_sharing_key(appID, appCertificate, channelName, unixTs, randomInt, uid, expiredTs):
    return generate_dynamic_key(appID, appCertificate, channelName, unixTs, randomInt, uid, expiredTs, "APSS")


def generate_recording_key(appID, appCertificate, channelName, unixTs, randomInt, uid, expiredTs):
    return generate_dynamic_key(appID, appCertificate, channelName, unixTs, randomInt, uid, expiredTs, "ARS")


def generate_media_channel_key(appID, appCertificate, channelName, unixTs, randomInt, uid, expiredTs):
    return generate_dynamic_key(appID, appCertificate, channelName, unixTs, randomInt, uid, expiredTs, "ACS")


def generate_dynamic_key(appID, appCertificate, channelName, unixTs, randomInt, uid, expiredTs, servicetype):
    uid = ctypes.c_uint(uid).value
    key = "\x00" * (32 - len(appID)) + appID
    signature = generate_signature(appID, appCertificate, channelName, unixTs, randomInt, uid, expiredTs, servicetype)
    version = '{0:0>3}'.format(4)
    ret = version + str(signature) + \
        appID + \
        '{0:0>10}'.format(unixTs) + \
        "%.8x" % (int(randomInt) & 0xFFFFFFFF) + \
        '{:0>10}'.format(expiredTs)
    return ret


def generate_signature(appID, appCertificate, channelName, unixTs, randomInt, uid, expiredTs, servicetype):
    key = "\x00" * (32 - len(appID)) + appID
    content = servicetype + key +\
        '{:0>10}'.format(unixTs) + \
        "%.8x" % (int(randomInt) & 0xFFFFFFFF) + \
        str(channelName) +\
        '{:0>10}'.format(uid) + \
        '{:0>10}'.format(expiredTs)
    signature = hmac.new(appCertificate, content, sha1).hexdigest()
    return signature


def generate_signalingkey(appID, appCertificate, uid, expiredTs):
    s = uid + appID + appCertificate + str(expiredTs)
    m = hashlib.md5()
    m.update(s)
    s = m.hexdigest()
    return "1:"+appID+":"+str(expiredTs)+":"+s
