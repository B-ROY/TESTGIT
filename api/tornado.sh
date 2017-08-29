#!/bin/bash

APP_DIR=/mydata/python/live_video/api

APP_EXEC="/mydata/python2.7/bin/python main.py"

LOG_DIR=/mydata/logs/tornado/
LOG_LEVEL=error

#TODO 这里上线后修改为100
WORKER_NUM=2
PORTS=(9000)
#PORTS=(9005)

#TODO 上线后修改DOC为FALSE
function start_server() {
    cd $APP_DIR
    chmod +x main.py
    ulimit -n 65535
    for port in "${PORTS[@]}";
    do
        echo $port
        $APP_EXEC -port=$port -doc=False -worker=$WORKER_NUM -logging=$LOG_LEVEL -log_file_prefix=$LOG_DIR/$port.log &
    done
}

function stop_server() {
    for port in "${PORTS[@]}";
    do
        ps aux | grep "$APP_EXEC" | grep "$port" | awk '{print $2}' | xargs kill -9
    done
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
    echo 'Usage: bin/tornado.sh [start|stop|restart]'
esac
