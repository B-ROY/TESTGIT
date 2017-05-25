/*-
 * Copyright (c) 2006 Verdens Gang AS
 * Copyright (c) 2006-2011 Varnish Software AS
 * All rights reserved.
 *
 * Author: Poul-Henning Kamp <phk@phk.freebsd.dk>
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL AUTHOR OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR 
 * BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 * WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
 * OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
 * EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * The default VCL code.
 *
 * NB! You do NOT need to copy & paste all of these functions into your
 * own vcl code, if you do not provide a definition of one of these
 * functions, the compiler will automatically fall back to the default
 * code from this file.
 *
 * This code will be prefixed with a backend declaration built from the
 * -b argument.
 */

/*
    only record hit log

    varnishncsa  -m "TxHeader:X-Cache: HIT" -F '%h "%{%Y-%m-%dT%H:%M:%S+08:00}t" %m "%U" "%q" - %s %b %D "%{User-Agent}i"' -P /opt/logs/varnish/varinsh.pid  -a -w /opt/logs/varnish/log -D

    varnishd -a 0.0.0.0:81 -f /etc/varnish/default.vcl -T 0.0.0.0:2003  -s malloc,2G -p thread_pools=4 -p thread_pool_min=5 00 -p thread_pool_max=5000  -p thread_pool_add_delay=2  
    curl -v -H "User-Agent:aas" 'http://10.103.13.18:2002/layout/android3_0/play/detail?pid=69b81504767483cf&id=XNjAyNzY2MTA4&guid=1e9c4397fe8eff199b0ff213fffc2293'

    for test
    curl -v -H "User-Agent:HeyDo;2.2;Android;4.0.3;X907"  'http://10.105.28.41:88/catetory/apps?category_id=3&guid=1e9c4397fe8eff199b0ff213fffc2293'
*/

C{
#include <errno.h>
#include <limits.h>
}C


probe healthcheck {
    .url = "/";
    .interval = 10s;
    .timeout = 3s;
    .window = 16;
    .threshold = 3;
    .initial = 3;
}


#backend api_server1 {
#    .host = "10.103.28.191";
#    .port = "80";
#    .connect_timeout = 3s;
#    .first_byte_timeout = 3s;
##    .between_bytes_timeout = 3s;
#    .probe = healthcheck;
#}

#backend api_server2 {
#    .host = "10.103.28.192";
#    .port = "80";
#    .connect_timeout = 3s;
#    .first_byte_timeout = 3s;
#    .between_bytes_timeout = 3s;
#    .probe = healthcheck;
#}
backend api_server3 {
    .host = "10.105.28.145";
    .port = "80";
    .connect_timeout = 3s;
    .first_byte_timeout = 3s;
    .between_bytes_timeout = 3s;
    .probe = healthcheck;
}

backend api_server4 {
    .host = "10.105.28.146";
    .port = "80";
    .connect_timeout = 3s;
    .first_byte_timeout = 3s;
    .between_bytes_timeout = 3s;
    .probe = healthcheck;
}

backend api_server5 {
    .host = "10.105.28.141";
    .port = "80";
    .connect_timeout = 3s;
    .first_byte_timeout = 3s;
    .between_bytes_timeout = 3s;
    .probe = healthcheck;
}

backend api_server6 {
    .host = "10.105.28.142";
    .port = "80";
    .connect_timeout = 3s;
    .first_byte_timeout = 3s;
    .between_bytes_timeout = 3s;
    .probe = healthcheck;
}

backend api_server7 {
    .host = "10.105.28.143";
    .port = "80";
    .connect_timeout = 3s;
    .first_byte_timeout = 3s;
    .between_bytes_timeout = 3s;
    .probe = healthcheck;
}

backend api_server8 {
    .host = "10.105.28.144";
    .port = "80";
    .connect_timeout = 3s;
    .first_byte_timeout = 3s;
    .between_bytes_timeout = 3s;
    .probe = healthcheck;
}


director default round-robin {
    #{ .backend = api_server1; }
    #{ .backend = api_server2; }
    { .backend = api_server3; }
    { .backend = api_server4; }
    { .backend = api_server5; }
    { .backend = api_server6; }
    { .backend = api_server7; }
    { .backend = api_server8; }
}


acl purge {
     "localhost";
     "10.0.0.0"/8;
}

sub vcl_recv {
    #set req.backend = default;

    if (req.backend.healthy) {
        set req.grace = 1m;
    } else {
        set req.grace = 30m;
    }

    unset req.http.If-Modified-Since;

    if (req.request == "PURGE" || req.http.Is-Update-Cache == "YES" ) {
            if (!client.ip ~ purge) {
                error 405 "Not allowed.";
            }
            
            return (lookup);
    }

    if (req.restarts == 0) {
    	if (req.http.x-forwarded-for) {
    	    set req.http.X-Forwarded-For = req.http.X-Forwarded-For + ", " + client.ip;
            set req.http.X-Real-Ip = client.ip;
    	} else {
    	    set req.http.X-Forwarded-For = client.ip;
            set req.http.X-Real-Ip = client.ip;
    	}
    }

    if (req.http.Accept-Encoding) {
            if (req.http.Accept-Encoding ~ "gzip") {
                    set req.http.Accept-Encoding = "gzip";
            } elsif (req.http.Accept-Encoding ~ "deflate") {
                    set req.http.Accept-Encoding = "deflate";
            } else {
                # unkown algorithm
                set req.http.Accept-Encoding = "";
            }                                            
    }


    if (req.request != "GET" &&
      req.request != "HEAD" &&
      req.request != "PUT" &&
      req.request != "POST" &&
      req.request != "TRACE" &&
      req.request != "OPTIONS" &&
      req.request != "DELETE") {
        /* Non-RFC2616 or CONNECT which is weird. */
        return (pipe);
    }
    if (req.request != "GET") {
        /* We only deal with GET by default */
        return (pipe);
    }
    if (req.http.Authorization) {
        /* Not cacheable by default */
        return (pipe);
    }

    if(req.url ~ "upload" ||
       req.url ~ "comment" ||
       req.url ~ "comments" ||
       req.url ~ "\/user\/" ||
       req.url ~ "adv"
       ){
        return (pipe);
    }

    return (lookup);
}

sub vcl_pipe {
    # Note that only the first request to the backend will have
    # X-Forwarded-For set.  If you use X-Forwarded-For and want to
    # have it set for all requests, make sure to have:
    # set bereq.http.connection = "close";
    # here.  It is not set by default as it might break some broken web
    # applications, like IIS with NTLM authentication.
    return (pipe);
}

sub vcl_pass {
    return (pass);
}

sub vcl_hash {

    #弹窗管理接口 游戏推荐接口 传pid
    if (req.url ~ "/app/main_client/exit_popup/get" ||
        req.url ~ "/app/recommend"
    ){
        hash_data(regsuball(req.url,"(&|\?)(s|e|t|sessionid|deviceid|brand|btype|os_ver|imei|os|idfa|ouid|guid|_s_|_e_|_t_|operator|network|vdid|ouid|mac)\b(=[^&]*)+",""));
    }

    else{
        hash_data(regsuball(req.url,"(&|\?)(pid|s|e|t|sessionid|deviceid|brand|btype|os_ver|imei|os|idfa|ouid|guid|_s_|_e_|_t_|operator|network|vdid|ouid|mac)\b(=[^&]*)+",""));
    }

    if(req.http.Accept-Encoding!=""){
        hash_data(req.http.Accept-Encoding);
    }

    if (req.http.User-Agent ~ "(.*?);(.*?);(.*?);(.*?);(.*)") {
         hash_data(regsub(req.http.User-Agent , "(.*?);(.*?);(.*?);(.*?);(.*)" , "\1:\3"));
    }
    return (hash);
}

sub vcl_hit {
  
    if (req.request == "PURGE"  || req.http.Is-Update-Cache == "YES" ) {
            purge;
            error 200 "Purged.";
    }

    return (deliver);
}

sub vcl_miss {

    if (req.request == "PURGE"  || req.http.Is-Update-Cache == "YES") {
                purge;
                error 200 "Purged.";
    }
    
    if (req.http.Range) {
       set bereq.http.Range = req.http.Range;
    }

    unset bereq.http.If-Modified-Since;
    unset bereq.http.If-None-Match;
    
    return (fetch);
}

sub vcl_fetch {

    if (beresp.status == 500) {
            return(restart);
    }
    else if(beresp.status == 410) {
          set beresp.ttl = 0s;
          set beresp.grace = 0s;
    }
    else if (beresp.status == 200) {
        if (beresp.ttl <= 0s ||
            beresp.http.Set-Cookie ||
            beresp.http.Vary == "*") {
              /*
              * Mark as "Hit-For-Pass" for the next 2 minutes
              */
              set beresp.ttl = 30s;
              return (hit_for_pass);
        }
        else{
            set beresp.grace = 30m;
        }
    }
    return (deliver);
}

 
/**
 *   {{{ sub extend_cache_control | vcl_fetch
 *
 *   Adds custom Cache-Control directive to control how long Varnish
 *   keeps the item in cache.
 *
 */
// sub extended_cache_control
// {   
//     /* For 2.1 change obj. to beresp. */
//     if (obj.http.Cache-Control ~ "v-max-age=[0-9]+") {
//         /* Copy the ttl part from original header */
//         set obj.http.X-Cache-Control-TTL = regsub(obj.http.Cache-Control, ".*v-max-age=([0-9]+).*", "\1");
// C{
//         {    
//             char *x_end = 0;
//             /* For trunk this needs to be HDR_BERESP */
//             const char *x_hdr_val = VRT_GetHdr(sp, HDR_OBJ, "\024X-Cache-Control-TTL:");
//             if (x_hdr_val) {
//                 long x_cache_ttl = strtol(x_hdr_val, &x_end, 0);
//                 if (ERANGE != errno && x_end != x_hdr_val && x_cache_ttl >= 0 && x_cache_ttl < INT_MAX) {
//                     /* for trunk this needs be VRT_l_beresp_ttl */
//                     VRT_l_obj_ttl(sp, (x_cache_ttl * 1));
//                 }
//             }
//         }
// }C
//         unset obj.http.X-Cache-Control-TTL;
//     }
// }
/* }}} */



sub vcl_deliver {

    if (obj.hits > 0) {
        unset resp.http.Set-Cookie;
        unset resp.http.X-Varnish;
        unset resp.http.Via;
        set resp.http.X-Cache = "HIT";
      } else {
        unset resp.http.X-Varnish;
        unset resp.http.Via;
        set resp.http.X-Cache = "MISS";
    }

    if(req.http.If-None-Match && req.http.If-None-Match == resp.http.Etag){
        unset resp.http.Content-Type;
        unset resp.http.Content-Encoding;
        unset resp.http.Accept-Ranges;
    }

    return (deliver);
}

sub vcl_error {
    set obj.http.Content-Type = "text/html; charset=utf-8";
    set obj.http.Retry-After = "5";
    synthetic {"
<?xml version="1.0" encoding="utf-8"?>
<!DO http://www.varnish-cache.org/ticket/451CTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
 "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
  <head>
    <title>"} + obj.status + " " + obj.response + {"</title>
  </head>
  <body>
    <h1>Error "} + obj.status + " " + obj.response + {"</h1>
    <p>"} + obj.response + {"</p>
    <h3>Guru Meditation:</h3>
    <p>XID: "} + req.xid + {"</p>
    <hr>
    <p>Varnish cache server</p>
  </body>
</html>
"};
    return (deliver);
}

sub vcl_init {
	return (ok);
}

sub vcl_fini {
	return (ok);
}
