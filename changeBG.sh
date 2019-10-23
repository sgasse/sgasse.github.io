#!/bin/bash

function checkAndSetBackground {
    if [ "$(cat curBG.info)" != "$1" ]; then
        rm bg.jpg
        cp "$1" bg.jpg
        echo "$1" > curBG.info
    fi
}

function setWinter {
    checkAndSetBackground "bg_ice_small.jpg"
}

function setSpring {
    checkAndSetBackground "bg_lawn_small.jpg"
}

function setSummer {
    checkAndSetBackground "bg_sea_small.jpg"
}

function setFall {
    checkAndSetBackground "bg_field_small.jpg"
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
    sleep 12h
done

