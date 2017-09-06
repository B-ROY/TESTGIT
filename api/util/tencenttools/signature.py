#coding=utf-8
#!/bin/bash
__author__ = 'zen'
import os
from django.conf import settings

"""
1、这个是为了在运行中生成腾讯云的秘钥，进行接口调用，主要是给云通信im平台使用
2、腾讯云用户登录使用
"""
def gen_signature(appid, content):

    tool_path = settings.SIG_TOOL_PATH
    key_path = settings.SIG_KEY_PATH
    sig_path = settings.SIG_PATH  #'/mydata/python/live_video/api/util/tencenttools/tls_sig_api-linux-64/tools'

    cmd = '%s/tls_licence_tools gen %s/private_key %s/%s_sig %s %s >&null;cat %s/%s_sig' % (
        tool_path, key_path, sig_path ,content , appid, content, sig_path, content
    )

    p = os.popen(cmd)
    sig = p.read()
    #remove key file
    rm_cmd = 'rm -f %s/%s_sig' % (sig_path, content)
    os.system(rm_cmd)
    
    return sig

if __name__ == "__main__":
    print gen_signature(appid=10048692, content='1234') #这里仅仅是测试使用
