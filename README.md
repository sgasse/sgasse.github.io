# Personal Landingpage with HTML, CSS, nginx and docker

This repository features my basic personal landing page with HTML and CSS, served via nginx. It includes a few decent animations. Everything works without JavaScript.

# Certificate setup

The nginx server needs to run to enable responding to ACME challenges which is needed to obtain certificates via letsencrypt. However, without any certificates, launching nginx will fail. One possibility would be to launch nginx with two different configurations; once without certificates and SSL block and once with. However instead, we will launch nginx with self-signed certificates, obtain correct certificates and then reload.

Create DH parameters:
```
openssl dhparam -out data/certbot/conf/ssl-dhparams.pem 4096
```

Create self-signed certificate to launch for SSL testing:
```
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout privkey.pem -out fullchain.pem -config simongasse_selfsigned.conf
```

Start just nginx:
```
docker-compose up --force-recreate -d nginx
```

Delete self-signed certificates:
```
docker-compose run --rm --entrypoint "\
    rm -Rf /etc/letsencrypt/live/simongasse.de && \
    rm -Rf /etc/letsencrypt/archive/simongasse.de && \
    rm -Rf /etc/letsencrypt/renewal/simongasse.de.conf" certbot
```

Request certificates from letsencrypt:
```
docker-compose run --rm --entrypoint "\
    certbot certonly --webroot -w /var/www/certbot \
    --email changeme@ymail.com \
    -d simongasse.de -d www.simongasse.de -d gitlab.simongasse.de \
    --rsa-key-size 4096 \
    --agree-tos \
    --force-renewal" certbot
```

Reload nginx:
```
docker-compose exec nginx nginx -s reload
```
