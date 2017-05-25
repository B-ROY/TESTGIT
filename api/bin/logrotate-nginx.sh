#!/bin/bash
# set file path
NGINX_ACCESS_LOG=/mydata/logs/nginx/access/log
NGINX_ERROR_LOG=/mydata/logs/nginx/error/log
NGINX_STATIS_LOG=/mydata/logs/nginx/statis/log
# rename log
mv $NGINX_ACCESS_LOG $NGINX_ACCESS_LOG.`date -d yesterday +%Y%m%d`
mv $NGINX_ERROR_LOG $NGINX_ERROR_LOG.`date -d yesterday +%Y%m%d`
mv $NGINX_STATIS_LOG $NGINX_STATIS_LOG.`date -d yesterday +%Y%m%d`
touch $NGINX_ACCESS_LOG
touch $NGINX_STATIS_LOG
#/etc/init.d/syslog-ng restart
# restart nginx
#[ ! -f /opt/nginx/logs/nginx.pid ] || kill -USR1 $(cat /opt/nginx/logs/nginx.pid)
/etc/init.d/nginx reload

LOG_DIR=/mydata/logs/nginx/access
O_LOG_FILE=log.pipe
today=`date -d"$0 day ago" +%Y-%m-%d`
yestoday=`date -d"1 day ago $today" +%Y-%m-%d`
sed -n "/$yestoday/,/$today/p" ${LOG_DIR}/${O_LOG_FILE}|grep -v 123.206.1.186|grep guid > $LOG_DIR/$yestoday.log
#sed -n "/$yestoday/,/$today/p" ${LOG_DIR}/${O_LOG_FILE} > $LOG_DIR/$yestoday.log

#cat $LOG_DIR/$O_LOG_FILE | grep "$yestoday" | grep /app/inital | grep -v heydo| grep 200 | awk '{print $4, $6, $11, $12, $13}' | sort | uniq | sort -nr > $LOG_DIR/guid-$yestoday.log
#cat $LOG_DIR/$O_LOG_FILE | grep "$yestoday" | grep /audio/[^sig] | grep -v heydo | grep 200 > $LOG_DIR/audio-$yestoday.log
#cat $LOG_DIR/$O_LOG_FILE | grep "$yestoday" | grep /picture/[^view] | grep -v list | grep -v heydo | grep 200 > $LOG_DIR/picture-$yestoday.log
month=`date -d"$yestoday" +%Y-%m`
mv $LOG_DIR/$yestoday.log $LOG_DIR/$month/

