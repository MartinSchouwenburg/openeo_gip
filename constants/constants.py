from enum import Enum

DTUNKNOWN = 0
DTINTEGER = 1
DTFLOAT = 2
DTSTRING = 4
DTRASTER = 8
DTERROR = 16
DTRASTER = 32
DTTABLE = 64
DTFEATURES = 128
DTLIST = 256
DTNUMBER = DTINTEGER | DTFLOAT
DTRASTERLIST = DTLIST | DTRASTER

UNDEFNUMBER = 10**20 - 1

PDUNKNOWN = 0
PDUSERDEFINED = 1
PDPREDEFINED = 2
PDPROCESSGRAPH = 4

STATUSQUEUED = "queued"
STATUSCREATED = "created"
STATUSRUNNING = "running"
STATUSSTOPPED = "canceled"
STATUSFINISHED = "finished"
STATUSUNKNOWN = "unknown"
CUSTOMERROR = "custom error"





