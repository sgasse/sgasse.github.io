FROM nginx:latest
COPY simongasse.de /var/www/simongasse.de
COPY nginx.conf /etc/nginx/conf.d/default.conf
