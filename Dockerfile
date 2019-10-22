FROM nginx:latest
COPY simongasse.de /var/www/simongasse.de
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY startup.sh /root/startup.sh
RUN chmod +x /root/startup.sh
CMD ["nginx"]
#CMD ["/root/startup.sh", "&&", "nginx", "-g", "daemon", "off"]
EXPOSE 80

