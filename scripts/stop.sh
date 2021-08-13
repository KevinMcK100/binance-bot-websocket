#!/bin/bash

TIMESTAMP=`date +%Y-%m-%d_%H-%M-%S`
cd /home/ubuntu/binance-bot-websocket/
echo "[$TIMESTAMP] Stopping binance-bot-websocket service..."
echo "[$TIMESTAMP] Stopping binance-bot-websocket service..." >> "status.log"
SERVICE="python binance-bot-websocket.pyz"
if pidof $SERVICE  >/dev/null
then
    PID=`pidof $SERVICE`
    echo "[$TIMESTAMP] $SERVICE running on PID $PID. Stopping..."
    echo "[$TIMESTAMP] $SERVICE running on PID $PID. Stopping..." >> "status.log"
    kill $PID >/dev/null
    echo "[$TIMESTAMP] $SERVICE running on PID $PID. Stoped."
    echo "[$TIMESTAMP] $SERVICE running on PID $PID. Stoped." >> "status.log"
else
    echo "[$TIMESTAMP] $SERVICE already stopped."
    echo "[$TIMESTAMP] $SERVICE already stopped." >> "status.log"
fi