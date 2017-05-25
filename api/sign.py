#coding=utf-8
import urlparse
import hashlib
import time
    
def sign(url):

    purl=urlparse.urlparse(url)
    path = purl.path
    query = urlparse.parse_qsl(purl.query,True)
    t = str(int(time.time()))
    #secret = "821l1i1x3fv8vs3dxlj1v2x91jqfs3om"
    #guid before 9c553730ef5b6c8c542bfd31b5e25b69
    
    #heydo gen secret key()
    secret = "3ffa2b792e03d62c4cdcd4e88ed87c68"

    qs = sorted(query, key=lambda d:d[0])
    print qs
    query = ''.join([u'%s=%s' % (k, unicode(v, 'utf8')) for (k, v) in qs if k != '_s_' and k!="_t_"])

    s = "GET" + ":" + path + ":" + query  + ":" +  t + ":"  + secret
    print s
    m = hashlib.md5()
    m.update(s)
    s = m.hexdigest()
    print url + "&_t_=" + t + "&_s_=" + s
    return s


if __name__ == '__main__':
    
    print sign("http://115.159.112.32/live/room/gift_list?guid=1e9c4397fe8eff199b0ff213fffc2293&_test_user=undefined")
