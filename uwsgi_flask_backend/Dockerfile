FROM alpine:3.11.6

EXPOSE 3947
COPY simongasse.de /www/simongasse.de
COPY requirements.txt /confs/requirements.txt

RUN apk add --no-cache \
    uwsgi-python3 \
    python3

RUN pip3 install --no-cache-dir -r /confs/requirements.txt

# exclude IP in socket definition when running with docker-compose
CMD [ "uwsgi", "--socket", ":3947", \
                "--plugin", "python", \
                "--wsgi-file", "/www/simongasse.de/landingPage.py", \
                "--callable", "app", \
                "--processes", "2", \
                "--threads", "2", \
                "--stats", ":9191"]

