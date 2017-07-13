
#将代码放到服务器之后需要执行的命令
SRC_TAR = "live_video.tar.gz"

echo "make source dir"
mkdir -p /mydata/python
mv /mydata/downloads/$SRC_DIR /mydata/python
cd /mydata/python
tar -xzvf $SRC_DIR



echo "make logs dir"
mkdir -p /mydata/logs/nginx/access
mkdir -p /mydata/logs/nginx/error
mkdir -p /mydata/logs/nginx/statis
mkdir -p /mydata/logs/tornado
mkdir -p /mydata/run

ln -s /mydata/python/live_video/api/conf/nginx/lua /mydata/nginx/conf/lua
ln -s /mydata/python/live_video/api/conf/nginx/nginx.conf /mydata/nginx/conf/nginx.conf
ln -s /mydata/python/live_video/api/conf/nginx/live.video.api.com /mydata/nginx/conf/live.video.api.com

echo "start nginx"
ldconfig
/mydata/nginx/sbin/nginx -c /mydata/nginx/conf/nginx.conf


yum install crontabs

#################################################
#Edit crontab file
num=$( cat /var/spool/cron/root|grep -c logrotate-nginx )
if [ $num = 0 ];then
   echo "OK-O-O-O write hosts"
   read i
   echo '0 0 * * * /mydata/python/live_video/api/bin/logrotate-nginx.sh > /dev/null 2>&1'>>/var/spool/cron/root
   echo '5 0 * * * /mydata/python/live_video/api/bin/logrotate.sh > /dev/null 2>&1'>>/var/spool/cron/root
   echo '#Delete old more than 7 days log files'>>/var/spool/cron/root
   echo '22 2 * * * find /mydata/logs/ -mtime +7 -type f -name "*log*" -exec rm -rf {} \;'>>/var/spool/cron/root
fi

wget https://pypi.python.org/packages/source/r/rsa/rsa-3.4.tar.gz#md5=9e78250000664a0be51966951d06cc17 --no-check-certificate
tar zxf rsa-3.4.tar.gz
cd rsa-3.4
python setup.py install

#register service
chmod +x /mydata/python/live_video/api/main.py
chmod +x /mydata/python/live_video/api/bin/*

cp /mydata/python/live_video/api/bin/init.d/tornado /etc/init.d/
cp /mydata/python/live_video/api/bin/init.d/nginx /etc/init.d/

chkconfig --add nginx
chkconfig nginx on
chkconfig --add tornado
chkconfig tornado on

#启动、停止等nginx操作用 /etc/init.d/nginx start|stop|restart 等


 #/usr/local/bin/python /usr/local/bin/supervisord -c /etc/supervisord.conf
 # /usr/bin/memcached -d -U 11211 -p 11211 -u nobody -m 200 -c 10000 -P /var/run/memcached/memcached.11211.pid
 # create database livevideo_platform  CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
 # vim /usr/share/mysql/charsets/Index.xml utf8-> utf8mb4

#安装pip


#安装facebook python
pip install facebook-sdk