#!/bin/bash

TIMESTAMP=`date +%Y-%m-%d_%H-%M-%S`
cd /home/ubuntu/binance-bot-websocket/

SERVICE="python binance-bot-websocket.pyz"

if pidof $SERVICE  >/dev/null
then
    echo "[$TIMESTAMP] $SERVICE is running"
    echo "[$TIMESTAMP] $SERVICE is running" >> "status.log"
else
    echo "[$TIMESTAMP] $SERVICE was not running. Starting..."
    echo "[$TIMESTAMP] $SERVICE was not running. Starting..." >> "status.log"
    ./start.sh
fi