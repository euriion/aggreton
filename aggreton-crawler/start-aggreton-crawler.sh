#!/bin/bash
#----------------------------------------------------------
# Aggretion start script
# author: Seonghak Hong
#----------------------------------------------------------

if [[ "${AGGRETON_CRAWLER_HOME}" == "" ]]; then
	echo "AGGRETON_CRAWLER_HOME enviroment variable should be assigned"
	exit 1
fi

pidfilename="${AGGRETON_CRAWLER_HOME}/pid/aggreton-crawler.pid"

if [[ ! -e $pidfilename ]]; then
    echo "starting aggreton crawler"
    cd ${AGGRETON_CRAWLER_HOME}/
    find ${AGGRETON_CRAWLER_HOME}/modules/ -name *.pyc | xargs -n 1 rm
    /usr/bin/python aggreton-crawler.py --daemon
else
	echo "aggreton crawler is already run"
	echo "checking the $pidfilename"
fi
