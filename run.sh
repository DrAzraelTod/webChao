#!/bin/sh
kill `cat /home/webchao/server.pid`
cd /home/webchao
su www-data -c "/home/webchao/manage.py runfcgi method=threaded host=127.0.0.1 port=8081 pidfile=/home/webchao/server.pid"
