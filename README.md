IoT Data Management Framework
==============================
IOTDMF is IoT data management framework based on Python Tornado back end + Bootstrap front end.

Revision History
------------------
[v03 2016-2-26 Aixi Wang]
* added simple device managemnt support
* fixed /download/xxx issue


[v02 2016-2-10 Aixi Wang]
* added ops,btc page
* updated item in pages to bootstrap style
* removed jpg_xxx related routines


[v01 2016-2-8 Aixi Wang]
* based on data-view
* changed to Tornado + Bootstrap framework


Architect
------------------
Bootstrap page <--> Tornado REST API server <--> JSON RPC server.

JSON RPC server is not included in this project.


How to test
--------------
* install tornado lib
* step1. python api-tornado.py
* step2. access http://127.0.0.1:8081/
       username: xxx
       password: xxx

How to develop
--------------
api-tornado.py  -- main REST API implementation
/static, /js    -- static pages


TODO List
-----------------------------------
* implement btc.html full function


Contact me
--------------
aixi.wang@hotmail.com


Donate
-------------
Bitcoin address: 1Aixi7ZpzQGMzVjx39GFCxVWpLpjTpcPgr
