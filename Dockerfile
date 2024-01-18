FROM python:3-alpine
WORKDIR /app

COPY sist_alerta_temprana /app/sist_alerta_temprana/
COPY requirements.txt . 

RUN apk add apk-cron && \
    chmod +x ./sist_alerta_temprana/main.py && \
    pip install -r requirements.txt && \
    touch /var/run/crond.pid && \
    touch /var/log/cron.log

#COPY app.sh /app/
#RUN chmod 777 /app/app.sh
#RUN crontab -l | { cat; printf "0 * * * * sh /app/app.sh\n"; } | crontab -
# ----
#COPY entrypoint.sh /app
#ENTRYPOINT exec sh /app/entrypoint.sh
WORKDIR /app/sist_alerta_temprana
