#!/bin/bash

function setWinter {
    rm bg.jpg
    cp bg_ice_small.jpg bg.jpg
}

function setSpring {
    rm bg.jpg
    cp bg_lawn_small.jpg bg.jpg
}

function setSummer {
    rm bg.jpg
    cp bg_sea_small.jpg bg.jpg
}

function setFall {
    rm bg.jpg
    cp bg_field_small.jpg bg.jpg
}


month=$(date +%m)

while [ 1 ]
do
    cd /var/www/simongasse.de/img
    if [ "$month" == "1" ]; then
        setWinter
    elif [ "$month" == "2" ]; then
        setWinter
    elif [ "$month" == "3" ]; then
        setWinter
    elif [ "$month" == "4" ]; then
        setSpring
    elif [ "$month" == "5" ]; then
        setSpring
    elif [ "$month" == "6" ]; then
        setSummer
    elif [ "$month" == "7" ]; then
        setSummer
    elif [ "$month" == "8" ]; then
        setSummer
    elif [ "$month" == "9" ]; then
        setFall
    elif [ "$month" == "10" ]; then
        setFall
    elif [ "$month" == "11" ]; then
        setWinter
    elif [ "$month" == "12" ]; then
        setWinter
    fi
    sleep 3d
done

