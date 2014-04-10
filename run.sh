#!/bin/sh
kill `cat /home/webchao/server.pid`
cd /home/webchao
python ./manage.py runfcgi host=127.0.0.1 port=8080 pidfile=/home/webchao/server.pid
