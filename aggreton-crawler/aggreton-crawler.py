import json
from optparse import OptionParser
import sys
import os
import importlib

if not os.environ.has_key('AGGRETON_CRAWLER'):
    raise Exception('AGGRETON_CRAWLER should be assinged in environment variables')
    sys.exit(1)

AGGRETON_CRAWLER = os.environ['AGGRETON_CRAWLER'].strip()

if not os.path.exists(AGGRETON_CRAWLER):
    raise Exception('AGGRETON_CRAWLER directory does not exist')
    sys.exit(1)

import logging
import inspect
from apscheduler.scheduler import Scheduler
import signal
import daemon
from daemon.pidfile import PIDLockFile

sys.path.append("%s/scheduler/modules" % AGGRETON_CRAWLER)

logging.basicConfig(level='DEBUG', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger_file_handler = logging.FileHandler('%s/logs/scheduler/ndash-scheduler.log' % AGGRETON_CRAWLER)
logger_file_handler.setLevel(logging.DEBUG)
logger_file_handler.setFormatter(logger_formatter)
logger = logging.getLogger('ndash-scheduler')
logger.addHandler(logger_file_handler)

if __name__ == "__main__":
    logger.info("starting aggreton crawler")
    parser = OptionParser(usage="%prog [-d/--daemon] [-r/--run]", version="%prog 1.0")
    parser.add_option("-d", "--daemon", dest="daemon", action="store_true", help="run as a daemon")
    parser.add_option("-r", "--run", dest="run", action="store_true", help="run as a batch process")
    parser.add_option("-m", "--module", dest="module", help="module name to run in instance run mode with -r option")
    (options, args) = parser.parse_args()
    logger.debug("starting scheduler with options: %s" % options)
    if not options.daemon and not options.run:
        parser.print_usage()
        sys.exit(0)
    logger.info("option: %s" % options)
    if options.daemon:
        log_directory = "%s/scheduler/logs" % AGGRETON_CRAWLER
        if not os.path.exists(log_directory):
            os.mkdir(log_directory)
        scheduler_log_filename = "%s/ndash-scheduler-daemon.log" % log_directory
        daemonLogFile = open(scheduler_log_filename, 'a+')
        # daemon.DaemonContext.files_preserve = [daemonLogFile]
        pidlock_filename = "%s/pid/ndash-scheduler.pid" % AGGRETON_CRAWLER
        logger.info("locking %s" % pidlock_filename)
        pidlock_fd = PIDLockFile(pidlock_filename)
        if pidlock_fd.is_locked():
            print "Error! %s file is already locked. DAEMON is terminated." % pidlock_filename
            logger.critical("pid file '%s' is exists" % pidlock_filename)
            sys.exit(1)
        working_directory = "%s/scheduler" % AGGRETON_CRAWLER
        logger.info("setting daemon mode")
        with daemon.DaemonContext(pidfile=pidlock_fd, working_directory=working_directory,
                # stdout=sys.stdout,
                # stderr=sys.stderr,
                files_preserve = [logger_file_handler.stream, daemonLogFile]):
            logger.info("initializing daemon")
            try:
                logging.basicConfig(level='DEBUG', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                sched = Scheduler()
                logger.info("loading scheduler conf file")
                scheduler_conf = json.loads(open("%s/scheduler/conf/ndash-scheduler.json" % AGGRETON_CRAWLER).read())
                for schedule_item in scheduler_conf['schedule-list']:
                    logger.info("loading shcedule module [%s.%s]" % (schedule_item['module_name'], schedule_item['class_name']))
                    scheduler_module = __import__(schedule_item['module_name'])
                    scheduler_class = getattr(scheduler_module, schedule_item['class_name'])
                    scheduler_instance = scheduler_class()
                    sched.add_cron_job(scheduler_instance.run,
                                       year=schedule_item['year'],
                                       month=schedule_item['month'],
                                       day=schedule_item['day'],
                                       week=None,
                                       day_of_week=None,
                                       hour=schedule_item['hour'],
                                       minute=schedule_item['minute'])
                sched.start()
                signal.pause()
                # sched.shutdown()
            except Exception, e:
                logger.exception(e)
                print e
        logger.info("scheduler daemon is terminated")
        daemonLogFile.close()
    else:
        scheduler_conf = json.loads(open("%s/scheduler/conf/ndash-scheduler.json" % AGGRETON_CRAWLER).read())
        func_list = {}
        for schedule_item in scheduler_conf['schedule-list']:
            print("loading shcedule module [%s.%s]" % (schedule_item['module_name'], schedule_item['class_name']))
            scheduler_module = __import__(schedule_item['module_name'])
            scheduler_class = getattr(scheduler_module, schedule_item['class_name'])
            scheduler_instance = scheduler_class()
            func_list[schedule_item['module_name']] = {
                'fullname':"%s.%s" % (schedule_item['module_name'], schedule_item['class_name']),
                'func':scheduler_instance.run
            }

        if options.module is None:
            for func_key in func_list.keys():
                print("loading shcedule module [%s]" % (func_list[func_key]['fullname']))
                # scheduler_module = __import__(schedule_item['module_name'])
                # scheduler_class = getattr(scheduler_module, schedule_item['class_name'])
                # scheduler_instance = scheduler_class()
                # scheduler_instance.run()
                print("running [%s]" % (func_list[func_key]['fullname']))
                func_list[func_key]['func']()
        else:
            if func_list.has_key(options.module):
                print("running [%s]" % (func_list[options.module]['fullname']))
                func_list[options.module]['func']()
            else:
                print("'%s' does not exist" % options.module)


    logger.info("terminating aggreton-crawler")
