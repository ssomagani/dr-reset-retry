#!/usr/bin/env python

import os, time, logging
from voltdbclient import *

SLEEP_INTERVAL=5
SERVER='localhost'
PORT=21212
USE_SSL=False
USERNAME='admin'
PASSWORD='admin'

LOGFILE='dr_reset_retry.log'
RUN_COUNTER=0
logger = logging.getLogger()
fileHandler = logging.FileHandler(LOGFILE)
consoleHandler = logging.StreamHandler()

def init():
    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)
    logger.info("INITIALIXING")
    main()

def main():
    os.system(f'voltadmin dr reset --force -u {USERNAME} -p {PASSWORD}')
#    os.system("voltadmin dr reset --force)
    global RUN_COUNTER
    RUN_COUNTER  +=1
    logger.warning(f'Ran DR RESET {RUN_COUNTER} times so far')

    time.sleep(SLEEP_INTERVAL)

    client = FastSerializer(SERVER, PORT, USE_SSL, USERNAME, PASSWORD)
#   client = FastSerializer(SERVER, PORT)
    proc = VoltProcedure( client, "@Statistics", [FastSerializer.VOLTTYPE_STRING, FastSerializer.VOLTTYPE_INTEGER] )
    response = proc.call([ "xdcr_readiness", 0])

    table = response.tables[0]

    if len(table.tuples) == 0:
        logger.error("No response to @Statistics query. Are you able to connect to your Volt cluster?")
    else:
        check_and_retry(table.tuples)

def check_and_retry(tuples):
    for row in tuples:
        if(row[4] == 'PENDING' or row[4] == 'STOPPED'):
            logger.warning("Validation Failed. Check values below.")
            logger.warning(tuples)
            time.sleep(SLEEP_INTERVAL)
            main()
    logger.warning("DR RESET succeeded")

init()
