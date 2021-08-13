#!/bin/bash

TIMESTAMP=`date +%Y-%m-%d_%H-%M-%S`
cd /home/ubuntu/binance-bot-websocket/
echo "[$TIMESTAMP] Restarting binance-bot-websocket service..."
echo "[$TIMESTAMP] Restarting binance-bot-websocket service..." >> "status.log"
./stop.sh
./start.sh