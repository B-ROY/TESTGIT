import re
import os
import tencentyun
import hmac
import urllib2
import random
import time
import binascii
import base64
import hashlib
import json

__author__ = 'zen'

APPID = '10048692'
BUCKET = 'heydopic'
SECRET_ID = 'AKIDgknyBYkNKnpONeweTRwK9t6Nn0jn78yG'
SECRET_KEY = 'fBCXVJK1PpWPtYizb7vIGVMIJFm90GBa'

UPLOAD_TYPE_FILE = 1
UPLOAD_TYPE_BIN = 2


class UploadImage(object):

    def __init__(self, file_handler, save_path=''):
        self.file_handler = file_handler
        self.save_path = save_path
        filename = self.file_handler.name.replace(" ",'')
        file_name_t = re.sub(u'[\u4e00-\u9fa5]', 'X', filename)
        file_name_t = re.sub(u'[\uFF00-\uFFFF]', 'X', file_name_t)

        self.out_file_name = "%s_%s" % (int(time.time()), file_name_t)
        self.file_id = "%s_%s" % (int(time.time()), hashlib.md5(filename).hexdigest())

    def save_to_local(self):
        local_file_path = os.path.join(self.save_path, self.out_file_name)

        temp_file = local_file_path + '.tmp'
        output_file = open(temp_file, 'wb')
        # Finally write the data to a temporary file
        self.file_handler.incoming_file.seek(0)
        h = hashlib.md5()
        while True:
            data = self.file_handler.incoming_file.read(2 << 16)
            if not data:
                break
            output_file.write(data)
            h.update(data)
        output_file.close()
        os.rename(temp_file, local_file_path)

    def push_to_qclude(self):
        image = tencentyun.ImageV2(
            APPID, SECRET_ID, SECRET_KEY)

        return image.upload_binary(
            self.file_handler,
            bucket=BUCKET,
            fileid=self.file_id)

    @classmethod
    def push_binary_to_qclude(cls,binary,price=0):

        image = tencentyun.ImageV2(
            APPID, SECRET_ID, SECRET_KEY)

        if price == 0:
            pic_bucket = "hdlive"
        else:
            pic_bucket = "heydopic"

        return image.upload_binary(
            binary,
            bucket=pic_bucket,
            fileid= hashlib.md5("logo"+str(int(time.time()) ) ).hexdigest() )



def delete_pic(file_id):
    secret_key = "fBCXVJK1PpWPtYizb7vIGVMIJFm90GBa"
    appid = "10048692"
    bucket = "hdlive"
    secret_id = "AKIDgknyBYkNKnpONeweTRwK9t6Nn0jn78yG"
    expiredTime = int(time.time()) + 999
    currentTime = time.time()
    rand = random.randint(0, 9999999)
    userid = "0"

    delete_url = "http://web.image.myqcloud.com/photos/v2/%s/%s/%s/%s/del" % (appid, bucket, userid, file_id)

    plain_text = "a=%s&b=%s&k=%s&e=%s&t=%s&r=%s&u=%s&f=%s" % \
                 (appid, bucket, secret_id, expiredTime, currentTime, rand, userid, file_id)

    b = hmac.new(secret_key, plain_text, hashlib.sha1)
    s = b.hexdigest()
    s = binascii.unhexlify(s)
    s += plain_text
    signature = base64.b64encode(s).rstrip()

    headers = {
        "Host": "web.image.myqcloud.com",
        "Authorization": signature,
        "Content-Length": 0
    }
    print delete_url
    req = urllib2.Request(delete_url, data="", headers=headers)
    return json.loads(urllib2.urlopen(req).read())


def porncheck(pic_url):
    porncheck_url = "http://service.image.myqcloud.com/detection/porn_detect"

    secret_key = "fBCXVJK1PpWPtYizb7vIGVMIJFm90GBa"
    appid = "10048692"
    bucket = "hdlive"
    secret_id = "AKIDgknyBYkNKnpONeweTRwK9t6Nn0jn78yG"
    expiredTime = int(time.time()) + 999
    currentTime = time.time()
    rand = random.randint(0, 9999999)
    userid = "0"

    plain_text = "a=%s&b=%s&k=%s&e=%s&t=%s&r=%s&u=%s" % \
                 (appid, bucket, secret_id, expiredTime, currentTime, rand, userid)

    b = hmac.new(secret_key, plain_text, hashlib.sha1)
    s = b.hexdigest()
    s = binascii.unhexlify(s)
    s += plain_text
    signature = base64.b64encode(s).rstrip()

    body = {
        "appid": appid,
        "bucket": bucket,
        "url_list": [
            pic_url
        ]
    }

    headers = {
        "Host": "service.image.myqcloud.com",
        "Content-Type": "Application/json",
        "Authorization": signature,
        "Content_lenth": len(json.dumps(body))
    }
    req = urllib2.Request(porncheck_url, data=json.dumps(body), headers=headers)
    return json.loads(urllib2.urlopen(req).read())

if __name__ == "__main__":
    f = open('/Users/yinxing/e857d628a6e213558dd18a67bf9d666a.gif','rb')
    print dir(f)
    up = UploadImage(f)
    print up.push_to_qclude()
