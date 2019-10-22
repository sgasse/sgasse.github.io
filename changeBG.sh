#!/bin/bash


while [ 1 ]
do
    cd /var/www/simongasse.de/img
    rm bg.jpg
    cp bg_ice_small.jpg bg.jpg
    sleep 20s
    rm bg.jpg
    cp bg_sea_small.jpg bg.jpg
    sleep 20s
done
