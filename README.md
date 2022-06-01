Utility to retry `dr reset` on a cluster until the cluster passes the validation of being reset correctly.

Testing for below in the output of `exec @Statistics xdcr_readiness 0` -

`IS_READY = false` \
`DRROLE_STATE =STOPPED` \
`DRCONS_STATE =DISABLE` \
`DRCONS_ISPAUSED =false`
