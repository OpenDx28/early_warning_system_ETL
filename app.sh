#!/bin/bash
cd /app
start_time=$(date +%s)
/usr/local/bin/python /app/sist_alerta_temprana/main.py
end_time=$(date +%s)
elapsed_seconds=$((end_time - start_time))
echo "$(date) - Terminado en $elapsed_seconds segundos" >> /var/log/cron.log