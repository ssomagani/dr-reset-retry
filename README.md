# dr-reset-retry

An example script to retry `dr reset` on a cluster until the cluster passes the validation of being reset correctly

## Requirements
Python3

## Steps to Run
1. Update reset_retry.py to add in the Volt cluster hostname and security
2. Copy the two files (reset_retry.py, voltdbclient.py) onto a machine that can access the Volt cluster. 
3. Execute reset_retry.py

## Explanation
Testing for below in the output of `exec @Statistics xdcr_readiness 0` -

`DRROLE_STATE =STOPPED`
