#!/bin/bash

if [[ "${DZ_HOME}" == "" ]]; then
	echo "DZ_HOME environment variable should be assigned"
	exit 1
fi

pid_filename="${DZ_HOME}/pid/dramazine-webapp.pid"
if [ ! -e $pid_filename ]; then
    echo "DRAMAZINE web was not stared"
    exit 1
fi
pid=`cat ${DZ_HOME}/pid/dramazine-webapp.pid`
kill -HUP $pid
echo "DRAMAZINE web reload"
