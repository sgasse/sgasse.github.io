FROM alpine:3.11.6

RUN apk add --no-cache \
    uwsgi-python3 \
    python3 \
    py-pip \
    sqlite

RUN mkdir /db

COPY requirements.txt /confs/requirements.txt
RUN pip3 install --no-cache-dir -r /confs/requirements.txt

COPY app /www/app
EXPOSE 3947

CMD [ "uwsgi", "/www/app/app.ini"]

