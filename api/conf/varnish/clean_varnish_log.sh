#!/bin/bash
# set file path
VARNISH_ACCESS_LOG_PATH=/opt/logs/varnish

HISTORY_LOG_NAME_PREFIX=log.

# clean 7 days ago log every day
need_delete_access_log=${VARNISH_ACCESS_LOG_PATH}/${HISTORY_LOG_NAME_PREFIX}$(date -d "7 days ago" +%Y%m%d)
rm -rf ${need_delete_access_log}
