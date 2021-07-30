#!/bin/bash

if [[ "${DZ_HOME}" == "" ]]; then
	echo "DZ_HOME environment variable should be assigned"
	echo "DZ_HOME should have the path of Nsight directory which are root directory of this total package"
	exit 1
fi

GUNICON_BIN=`which gunicorn`  # Gunicorn path
MAX_CHILDREN=10  # Max children process count of Gunicorn
BIND_PORT=30080  # Listening port
BIND_ADDRESS=0.0.0.0
PID_FILENAME="${DZ_HOME}/pid/dramazine-webapp.pid"
echo "DRAMAZINE web starting"
# sudo -E ${GUNICON_BIN} dramazine-webapp:app -w ${MAX_CHILDREN} -D --bind ${BIND_ADDRESS}:${BIND_PORT} -p ${PID_FILENAME}
# echo "sudo -E ${GUNICON_BIN} dramazine-webapp:app -w ${MAX_CHILDREN} -D --bind ${BIND_ADDRESS}:${BIND_PORT} -p ${PID_FILENAME}"
${GUNICON_BIN} dramazine:app -w ${MAX_CHILDREN} -D --bind ${BIND_ADDRESS}:${BIND_PORT} -p ${PID_FILENAME} --log-file ./guincorn-error.log
#pid=`cat $PID_PID_FILENAME`
#echo "PID is $pid"

#watchmedo shell-command \
#  --patterns="*.py;" \
#  --recursive \
#  --command='echo "${watch_src_path}" && kill -HUP `cat $PID_PID_FILENAME`' . &