upstream live_api {
    server 127.0.0.1:9000 fail_timeout=0;
}

# init lua
lua_code_cache on;



server {
    listen 80;
    server_name api.v1.iwala.cn;
    charset utf-8;

    set $x_remote_addr $proxy_add_x_forwarded_for;

    if ($x_remote_addr = "") {
        set $x_remote_addr $remote_addr;
    }

    location ~ \.(gif|jpg|png)$ {
        access_log off;
        proxy_pass          http://live_api;
        proxy_connect_timeout 3;
        proxy_send_timeout 3;
        proxy_read_timeout 3;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ \.css$ {
        access_log off;
        proxy_pass          http://live_api;
        proxy_connect_timeout 3;
        proxy_send_timeout 3;
        proxy_read_timeout 3;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /doc {
        access_log off;
        proxy_pass          http://live_api;
        proxy_connect_timeout 3;
        proxy_send_timeout 3;
        proxy_read_timeout 3;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /sign  {
        access_log off;
        proxy_pass          http://live_api;
        proxy_connect_timeout 3;
        proxy_send_timeout 3;
        proxy_read_timeout 3;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /app/inital  {
        proxy_pass          http://live_api;
        proxy_connect_timeout 3;
        proxy_send_timeout 3;
        proxy_read_timeout 3;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /v1/alarm  {
        proxy_pass          http://live_api;
        proxy_connect_timeout 3;
        proxy_send_timeout 3;
        proxy_read_timeout 3;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /live/report/ioslogs  {
        proxy_pass          http://live_api;
        proxy_connect_timeout 3;
        proxy_send_timeout 3;
        proxy_read_timeout 3;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /image/porn_detect  {
        proxy_pass          http://live_api;
        proxy_connect_timeout 3;
        proxy_send_timeout 3;
        proxy_read_timeout 3;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /live/login {

        access_by_lua_file conf/lua/check_pid_signature.lua;

        proxy_pass          http://live_api;
        proxy_connect_timeout 12;
        proxy_send_timeout 12;
        proxy_read_timeout 12;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /api/live/do/pay {
        access_by_lua_file conf/lua/check_pid_signature.lua;

        proxy_pass          http://live_api;
        proxy_connect_timeout 12;
        proxy_send_timeout 12;
        proxy_read_timeout 12;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /notice {
        proxy_pass          http://live_api;
        proxy_connect_timeout 12;
        proxy_send_timeout 12;
        proxy_read_timeout 12;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /audio/user_subscribe {
        proxy_pass          http://live_api;
        proxy_connect_timeout 12;
        proxy_send_timeout 12;
        proxy_read_timeout 12;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /live/user/imcallback {
        proxy_pass          http://live_api;
        proxy_connect_timeout 12;
        proxy_send_timeout 12;
        proxy_read_timeout 12;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /api/live/applepay/verify {
        access_by_lua_file conf/lua/check_pid_signature.lua;
        proxy_pass          http://live_api;
        proxy_connect_timeout 12;
        proxy_send_timeout 12;
        proxy_read_timeout 12;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /live/user/real_name {
        proxy_pass          http://live_api;
        proxy_connect_timeout 12;
        proxy_send_timeout 12;
        proxy_read_timeout 12;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /live/user/video/auth/submit {
        proxy_pass          http://live_api;
        proxy_connect_timeout 12;
        proxy_send_timeout 12;
        proxy_read_timeout 12;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;

    }
    location ~ /live/sms/login {
        proxy_pass          http://live_api;
        proxy_connect_timeout 12;
        proxy_send_timeout 12;
        proxy_read_timeout 12;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /live/withdraw/login {
        proxy_pass          http://live_api;
        proxy_connect_timeout 12;
        proxy_send_timeout 12;
        proxy_read_timeout 12;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /live/withdraw/h5_request {
        proxy_pass          http://live_api;
        proxy_connect_timeout 12;
        proxy_send_timeout 12;
        proxy_read_timeout 12;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /log/audio/callInfo {
        proxy_pass          http://live_api;
        proxy_connect_timeout 12;
        proxy_send_timeout 12;
        proxy_read_timeout 12;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location / {

        access_by_lua_file conf/lua/check_pid_signature.lua;

        proxy_pass          http://live_api;
        proxy_connect_timeout 3;
        proxy_send_timeout 3;
        proxy_read_timeout 3;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }
}

server {


        listen 443 default ssl;
        ssl on;
        server_name api.v1.iwala.cn;
        ssl_certificate /mydata/nginx/conf/ssl/1_api.mobile.iwala.cn_bundle.crt;
        ssl_certificate_key /mydata/nginx/conf/ssl/2_api.mobile.iwala.cn.key;
	ssl_session_cache shared:SSL:10m;
        ssl_session_timeout 10m;
	ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:HIGH:!aNULL:!MD5:!RC4:!DHE;
        ssl_prefer_server_ciphers on;
	#add_header Strict-Transport-Security "max-age=31536000";

        set $x_remote_addr $http_x_real_ip;
        if ($x_remote_addr = "") {
            set $x_remote_addr $remote_addr;
        }
    location ~ \.(gif|jpg|png)$ {
        access_log off;
        proxy_pass          http://live_api;
        proxy_connect_timeout 3;
        proxy_send_timeout 3;
        proxy_read_timeout 3;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ \.css$ {
        access_log off;
        proxy_pass          http://live_api;
        proxy_connect_timeout 3;
        proxy_send_timeout 3;
        proxy_read_timeout 3;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /doc {
        access_log off;
        proxy_pass          http://live_api;
        proxy_connect_timeout 3;
        proxy_send_timeout 3;
        proxy_read_timeout 3;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /sign  {
        access_log off;
        proxy_pass          http://live_api;
        proxy_connect_timeout 3;
        proxy_send_timeout 3;
        proxy_read_timeout 3;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /app/inital  {
	proxy_next_upstream http_502 http_504 error timeout invalid_header;
        proxy_pass          http://live_api;
        proxy_connect_timeout 3;
        proxy_send_timeout 3;
        proxy_read_timeout 3;
        proxy_redirect      off;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        #proxy_set_header    Range $http_range;
	proxy_set_header X-Forwarded-Proto https; 
    }

    location ~ /v1/alarm  {
        proxy_pass          http://live_api;
        proxy_connect_timeout 3;
        proxy_send_timeout 3;
        proxy_read_timeout 3;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /live/report/ioslogs  {
        proxy_pass          http://live_api;
        proxy_connect_timeout 3;
        proxy_send_timeout 3;
        proxy_read_timeout 3;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /image/porn_detect  {
        proxy_pass          http://live_api;
        proxy_connect_timeout 3;
        proxy_send_timeout 3;
        proxy_read_timeout 3;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /live/login {

        access_by_lua_file conf/lua/check_pid_signature.lua;

        proxy_pass          http://live_api;
        proxy_connect_timeout 12;
        proxy_send_timeout 12;
        proxy_read_timeout 12;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /api/live/do/pay {
        access_by_lua_file conf/lua/check_pid_signature.lua;

        proxy_pass          http://live_api;
        proxy_connect_timeout 12;
        proxy_send_timeout 12;
        proxy_read_timeout 12;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /notice {
        proxy_pass          http://live_api;
        proxy_connect_timeout 12;
        proxy_send_timeout 12;
        proxy_read_timeout 12;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /audio/user_subscribe {
        proxy_pass          http://live_api;
        proxy_connect_timeout 12;
        proxy_send_timeout 12;
        proxy_read_timeout 12;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /live/user/imcallback {
        proxy_pass          http://live_api;
        proxy_connect_timeout 12;
        proxy_send_timeout 12;
        proxy_read_timeout 12;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /api/live/applepay/verify {
        access_by_lua_file conf/lua/check_pid_signature.lua;
        proxy_pass          http://live_api;
        proxy_connect_timeout 12;
        proxy_send_timeout 12;
        proxy_read_timeout 12;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /live/user/real_name {
        proxy_pass          http://live_api;
        proxy_connect_timeout 12;
        proxy_send_timeout 12;
        proxy_read_timeout 12;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /live/sms/login {
        proxy_pass          http://live_api;
        proxy_connect_timeout 12;
        proxy_send_timeout 12;
        proxy_read_timeout 12;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /live/withdraw/login {
        proxy_pass          http://live_api;
        proxy_connect_timeout 12;
        proxy_send_timeout 12;
        proxy_read_timeout 12;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /live/withdraw/h5_request {
        proxy_pass          http://live_api;
        proxy_connect_timeout 12;
        proxy_send_timeout 12;
        proxy_read_timeout 12;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }
    location ~ /live/user/real_name {
        proxy_pass          http://live_api;
        proxy_connect_timeout 12;
        proxy_send_timeout 12;
        proxy_read_timeout 12;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /activity/invite_ranklist {
        proxy_pass          http://live_api;
        proxy_connect_timeout 12;
        proxy_send_timeout 12;
        proxy_read_timeout 12;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }

    location ~ /live/user/video/auth/submit {
        proxy_pass          http://live_api;
        proxy_connect_timeout 12;
        proxy_send_timeout 12;
        proxy_read_timeout 12;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;

    }

    location ~ /log/audio/callInfo {
        proxy_pass          http://live_api;
        proxy_connect_timeout 12;
        proxy_send_timeout 12;
        proxy_read_timeout 12;
        proxy_redirect      default;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        proxy_set_header    Range $http_range;
    }


    location / {

        #access_by_lua_file conf/lua/check_pid_signature.lua;
	proxy_next_upstream error timeout invalid_header http_500 http_502 http_503;

        proxy_pass          http://live_api;
        proxy_connect_timeout 3;
        proxy_send_timeout 3;
        proxy_read_timeout 3;
        proxy_redirect      off;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header    X-Real-IP $x_remote_addr;
        proxy_set_header    Host $http_host;
        #proxy_set_header    Range $http_range;
	proxy_set_header X-Forwarded-Proto https; 
    }
               
}


