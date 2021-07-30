#!/bin/bash
#----------------------------------------------------------
# Aggretion start script
# author: Seonghak Hong
#----------------------------------------------------------

if [[ "${AGGRETON_CRAWLER_HOME}" == "" ]]; then
	echo "AGGRETON_CRAWLER_HOME enviroment variable should be assigned"
	exit 1
fi

pidfilename="${AGGRETON_CRAWLER_HOME}/pid/ndash-scheduler.pid"

if [[ ! -e "$pidfilename" ]]; then
	echo "ndash-scheduler is not running"
	echo "please checking if $pidfilename is existing"
	ls $pidfilename
else
	cat $pidfilename | xargs kill
	echo "ndash-scheduler has been stopped!"
	if [[ -e $pidfilename ]]; then
		rm $pidfilename
	fi
fi
