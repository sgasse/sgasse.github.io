#!/bin/bash

echo "Starting personal homepage container"

# start nginx in foreground if only command to keep container alive
#nginx -g 'daemon off;'

# start nginx in the background
nginx

# change background image according to season, keep container alive
/bin/bash /root/changeBG.sh

