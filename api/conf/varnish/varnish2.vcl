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

    varnishd -a 0.0.0.0:81 -f /etc/varnish/default.vcl -T 0.0.0.0:2003  -s malloc,2G -p thread_pools=4 -p thread_pool_min=500 -p thread_pool_max=5000  -p thread_pool_add_delay=2  
    curl -v -H "User-Agent:aas" 'http://10.103.13.18:2002/layout/android3_0/play/detail?pid=69b81504767483cf&id=XNjAyNzY2MTA4&guid=1e9c4397fe8eff199b0ff213fffc2293'
*/

/*
probe healthcheck {
    .url = "/test/helloworld";
    .interval = 60s;
    .timeout = 3s;
    .window = 8;
    .threshold = 3;
    .initial = 3;
} 
*/                

backend default {
    .host = "10.103.13.18";
    .port = "82";
    .connect_timeout = 2s;
    .first_byte_timeout = 3s;
    .between_bytes_timeout = 10s;
    //.probe = healthcheck;
}

/*
director default round-robin {
    { .backend = api_server1; }
}
*/


acl purge {
     "localhost";
      "10.0.0.0"/8; 
     ! "10.103.6.1";
}

sub vcl_recv {
    #set req.backend = default;

    if (req.backend.healthy) {
        set req.grace = 1m;
    } else {
        set req.grace = 1h;
    }

    if (req.request == "PURGE" || req.http.Is-Update-Cache == "YES" ) {
            if (!client.ip ~ purge) {
                error 405 "Not allowed.";
            } 
            return (pass);
    }

    unset req.http.If-Modified-Since;
    if (req.restarts == 0) {
    	if (req.http.x-forwarded-for) {
    	    set req.http.X-Forwarded-For = req.http.X-Forwarded-For ", " client.ip; 
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

    if(req.url ~ "/v3_1/home" ||
       req.url ~ "/recommended_channels" ||
       req.url ~ "/todou/play/detail/desc" ||
       req.url ~ "/v3_3/album/videos"){
        return (lookup);
    }
    else{      
        return (pipe);   
    }
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

    if(req.url ~ "/recommended_channels"){
        set req.hash += regsuball(req.url,"&?(guid|_s_|_e_|_t_)\b(=[^&]*)?","");
    }else{
        set req.hash += regsuball(req.url,"&?(guid|pid|_s_|_e_|_t_)\b(=[^&]*)?","");
    }

    set req.hash += req.http.Accept-Encoding;

    return (hash);
}

sub vcl_hit {
  
    if (req.request == "PURGE") {
            set obj.ttl = 0s;
            error 200 "Purged.";
    }

    if (!obj.cacheable) { 
       return (pass); 
    } 

    return (deliver);
}

sub vcl_miss {
   if (req.request == "PURGE") {
       error 404 "Not in cache";
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
    else if (beresp.status == 200) {
        if (beresp.http.Set-Cookie ||
              beresp.http.Vary == "*") {
		    /*
		    * Mark as "Hit-For-Pass" for the next 2 minutes
		    */
           //do nothing
        }else{
            //force cache obj 5m
            if( req.url ~ "/v3_1/home" ||
                req.url ~ "/recommended_channels" ||
                req.url ~ "/v3_3/album/videos"){

                set beresp.ttl = 1m;
            }
            else{
                set beresp.ttl = 30m;
            }
        } 
        set beresp.grace = 1h; 
    }

    return (deliver);
}

sub vcl_deliver {

    if (obj.hits > 0) {
        remove resp.http.Set-Cookie; 
        remove resp.http.X-Varnish; 
        remove resp.http.Via;
        set resp.http.X-Cache = "HIT";
      } else {
        remove resp.http.X-Varnish; 
        remove resp.http.Via;
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
    synthetic {""};
    return (deliver);
}
