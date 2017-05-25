#!/bin/bash

PROJDIR="/mydata/python/live_video/app"
PIDFILE="$PROJDIR/app.heydo.pid"
ERRORLOG="/mydata/logs/cms_error.log"
OUTLOG="/mydata/logs/cms_std_out.log"
APP_EXEC="python manage.py runfcgi method=prefork daemonize=true host=127.0.0.1"
NUM_PROC=10000
NUM_PROCS=4
MIN_SPARE=2
MAX_SPARE=6

cd $PROJDIR


function start_server() {
    cd $PROJDIR
    ulimit -n 65535
    $APP_EXEC port=$NUM_PROC minspare=$MIN_SPARE maxspare=$MAX_SPARE maxchildren=$NUM_PROCS  outlog=$OUTLOG errlog=$ERRORLOG
}

function stop_server() {
    ps aux | grep "$APP_EXEC" | grep "$NUM_PROC" | awk '{print $2}' | xargs kill -9
}

case "$1" in
start)
    start_server
;;
stop)
    stop_server
;;
restart)
    stop_server
    start_server
;;
*)
    echo 'Usage: app.sh [start|stop|restart]'
esac

