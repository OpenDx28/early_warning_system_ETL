#!/bin/sh

/usr/sbin/crond -f
while true; do echo "Started" > /var/log/cron.log ; sleep 9999; done
