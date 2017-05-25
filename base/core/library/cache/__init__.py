# -*- coding: utf-8 -*-
__author__ = 'zen'
import logging
import time
import functools
import hashlib
import inspect
import pickle
import pylibmc
from django.conf import settings
from base.core.util import dateutils

# print  settings.memcache_settings
memcache_settings  =  settings.memcache_settings
func_cache = pylibmc.Client(
    memcache_settings["func_cache"],
    binary=True,
    behaviors={"tcp_nodelay": True, "ketama": True}
)

page_cache = pylibmc.Client(
    memcache_settings["page_cache"],
    binary=True,
    behaviors={"tcp_nodelay": True, "ketama": True}
)

fragment_cache = pylibmc.Client(
    memcache_settings["fragment_cache"],
    binary=True,
    behaviors={"tcp_nodelay": True, "ketama": True}
)

user_cache = pylibmc.Client(
    memcache_settings["user_cache"],
    binary=True,
    behaviors={"tcp_nodelay": True, "ketama": True}
)


def get_plus_json(key, func, expire_m=None, expire_s=None, is_update=False, set_retry=True, not_valid_check={}):
    key_expire_name = "api.expired_at"
    raw_content = None

    if not is_update:
        n = time.time()
        content = page_cache.get(key)
        try:
            u = time.time() - n
            if u > 1:
                logging.error("get key %s use %s", key, u)
        except Exception, e:
            pass

        if content:
            if isinstance(content, dict) and content.has_key(key_expire_name):
                if content.get(key_expire_name) > int(time.time()):
                    #cache not expired
                    logging.debug("get key from cache:%s" % key)
                    return [content, ]
                else:
                    #cache expired,need to get new one
                    #if get new key exception use old one
                    logging.debug("expired %s" % key)
                    raw_content = content

    def get_and_set():
        try:
            #get result from origin function
            result = func()
            if result:
                #new version key result
                #{
                #   "api.body" : xxxxx
                #   "api.expire" :  1363672663
                #}
                valid = True
                if not_valid_check:
                    if isinstance(result, list):
                        for r in result:
                            for k, v in not_valid_check.iteritems():
                                if r.get(k) == v:
                                    valid = False
                                    break

                if valid:
                    logging.debug("set new version data")

                    data = {key_expire_name: int(time.time() + expire_m)}
                    for r in result:
                        data.update(r)

                    logging.debug("get data add set key:%s" % key)
                    page_cache.set(key, data, expire_s)
                    return [data, ]
        except Exception, e:
            logging.error(e)

            if raw_content:
                logging.debug("exception use old key:%s" % key)
                if set_retry:
                    #set 10 minute retry
                    data = raw_content
                    data.update({key_expire_name: int(time.time() + settings.cache_expire_15M)})

                    page_cache.set(key, data, expire_s)
                return [raw_content, ]
            else:
                #must be evctions or old key
                logging.error(e)
                raise e


    #default pool0 one hour after be expired.
    expire_m = expire_m or settings.cache_expire_1H
    #expire_m = 3 for test
    #2h not expire
    expire_s = expire_s or expire_m + settings.cache_expire_2H
    #key for mutex
    key_mutex = '%s_mutex' % key

    if page_cache.add(key_mutex, 1, settings.cache_expire_1M):
        #only allow one
        logging.debug("*mutex: %s" % key_mutex)
        try:
            raw_content = get_and_set()
        finally:
            logging.debug("delete mutex key:%s" % key_mutex)
            #delate mutex key
            page_cache.delete(key_mutex)
    else:
        #on key expire be mutex go here use old key to return
        logging.debug("*mutex locked: %s" % key)

        if not raw_content:
            #retry to get from func() ,normally not go here ,must be evictions
            logging.debug("* evictions: %s" % key)
            import timeit

            n = timeit.default_timer()
            raw_content = get_and_set()
            spend = timeit.default_timer() - n
            #todo logging.error spend url
            logging.error("* evictions: %s %s" % (func.func_closure[0].cell_contents.request.path, spend))

    return raw_content


def _encode_cache_key(k):
    if isinstance(k, (bool, int, long, float, str)):
        return str(k)
    elif isinstance(k, unicode):
        return k.encode('utf-8')
    elif isinstance(k, dict):
        import urllib

        for x in k.keys():
            k[x] = _encode_cache_key(k[x])
        return urllib.urlencode(sorted(k.items()), True)
    else:
        return repr(k)


def function_cache(cache_keys="", prefix='api#phone', suffix='fun', expire_time=60 * 60, is_update_cache='', extkws={}):
    u"""
      cache_keys：缓存取那些参数当key,key之间用豆号分割,空就是用函数所有参数
      prefix:前缀，suffix：后缀
      expire_time：缓存时间，defaut time 30'm
      is_update_cache="YES" or '' ，是否马上更新缓存,空到expire_time才更新缓存
      extkws={},追加缓存参数,同名覆盖缓存参数
      is_obd:"YES" or '' ,缓存运营管理
       生成ckey的长度len不超过200
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache_keys_list = []
            if cache_keys:
                cache_keys_list = cache_keys.split(',')
            arg_names, varargs, varkw, defaults = inspect.getargspec(func)
            #defaults
            _defargs = dict(zip(arg_names[-len(defaults):], defaults)) if defaults else {}
            _args1 = dict(zip(arg_names, args))
            _kwds = dict(_defargs, **_args1)
            _kwds.update(kwargs)
            _kwds.update(extkws)
            otheragrs = []
            if varargs:
                tmp = _args1.values()
                otheragrs = [v for v in args if v not in tmp]
                if otheragrs:
                    for i in xrange(0, len(otheragrs)):
                        _k = "_arg{}".format(i)
                        _kwds[_k] = otheragrs[i]

            if cache_keys_list:
                for k, v in _kwds.items():
                    if k not in cache_keys_list:
                        _kwds.pop(k, None)
            ckey = ""
            if _kwds:
                ckey = _encode_cache_key(_kwds)
            ckey = hashlib.md5(ckey).hexdigest()
            ckey = "{}#{}#{}".format(prefix, ckey, suffix)
            if len(ckey) > 200:
                ckey = ckey[:200]
            try:
                value = None if is_update_cache.upper() == 'YES' else func_cache.get(ckey)
                if value is None:
                    value = func(*args, **kwargs)
                    if value:
                        func_cache.set(ckey, value, expire_time)
                return value
            except Exception, e:
                return func(*args, **kwargs)

        wrapper.original_function = func
        wrapper.func_name = func.func_name
        wrapper.__doc__ = func.__doc__
        return wrapper

    return decorator


def page_static_cache(timeout=60 * 60 * 1, content_type="text/html", user_cache=True, host_cache=True,key_prefix=True):
    """
    page cache
    param:
    timeout:the deadline of cache  default is 1800
    """

    def _func(func):
        def wrap(request, *a, **kw):
            key = request.get_full_path()
            try:
                key = key.encode("utf-8")
            except Exception, e:
                key = str(key)

            if key_prefix:
                key = "%s:%s" % (dateutils.zero_date().strftime('%Y-%m-%d'), key)

            if user_cache:
                key = "%s:%s" % (key, request.user.id)

            if host_cache:
                key = "%s:%s" % (key, request.get_host())

            logging.debug("form get key:%s" % key)
            key = hashlib.md5(key).hexdigest()
            response = page_cache.get(key)
            if not response or settings.DEBUG:
                response = func(request, *a, **kw)
                if response:
                    logging.debug("form set key:%s" % key)
                    page_cache.set(key, pickle.dumps(response), timeout)
            else:
                response = pickle.loads(response)
                logging.debug("form get key:%s" % key)

            return response

        return wrap

    return _func
