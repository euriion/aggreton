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
sudo -E kill $pid
echo "DRAMAZINE web stopping"
#cat ${DZ_HOME}/pid/dramazine-webapp.pid | xargs kill
# sudo rm ${DZ_HOME}/pid/dramazine-webapp.pid
#ps aux | grep gunicorn | grep "dramazine-webapp" | awk '{print $2}' | xargs kill
