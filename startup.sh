#!/bin/bash

echo "Starting nginx"
#nginx -g 'daemon off;'
nginx
/bin/bash /root/changeBG.sh
