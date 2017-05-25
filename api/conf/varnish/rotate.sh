#!/bin/bash
# set file path
ACCESS_LOG=/opt/logs/varnish/log
# rename log
mv $ACCESS_LOG $ACCESS_LOG.`date -d yesterday +%Y%m%d`
touch $ACCESS_LOG
/etc/init.d/syslog-ng restart
/bin/kill -HUP `cat  /opt/logs/varnish/varinsh.pid 2>/dev/null`
/usr/bin/varnishncsa  -m "TxHeader:X-Cache: HIT" -F '"%{X-Real-Ip}i" "%{%Y-%m-%dT%H:%M:%S+08:00}t" %m "%U" "%q" - %s %b %D "%{User-Agent}i"' -P /opt/logs/varnish/varinsh.pid  -a -w /opt/logs/varnish/log.pipe -D