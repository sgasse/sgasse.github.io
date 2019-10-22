FROM nginx:latest
COPY simongasse.de /var/www/simongasse.de
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY changeBG.sh /root/changeBG.sh
COPY startup.sh /root/startup.sh
CMD ["/bin/bash", "/root/startup.sh"]
EXPOSE 80

