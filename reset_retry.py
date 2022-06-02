#!/usr/bin/env python

import os, time
from voltdbclient import *

SLEEP_INTERVAL=5
SERVER='localhost'
PORT=21212
USE_SSL=False
USERNAME='admin'
PASSWORD='admin'

def main():
    os.system(f'voltadmin dr reset --force -u {USERNAME} -p {PASSWORD}')
#    os.system("voltadmin dr reset --force)

    client = FastSerializer(SERVER, PORT, USE_SSL, USERNAME, PASSWORD)
#   client = FastSerializer(SERVER, PORT)
    proc = VoltProcedure( client, "@Statistics", [FastSerializer.VOLTTYPE_STRING, FastSerializer.VOLTTYPE_INTEGER] )
    response = proc.call([ "xdcr_readiness", 0])

    table = response.tables[0]

    if len(table.tuples) == 0:
        print(" ERROR - No response to @Statistics query. Are you able to connect to your Volt cluster?")
    else:
        check_and_retry(table.tuples)

def check_and_retry(tuples):
    if (check_col_for_value_mismatch(tuples, 4, 'STOPPED')):
        print("Validation Failed. Check values below.")
        print(tuples)
        time.sleep(SLEEP_INTERVAL)
        main()

def check_col_for_value_mismatch(tuples, index, value):
    for row in tuples:
        if(value != row[index]):
            return True
    return False

main()
