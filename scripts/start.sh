#!/bin/sh

TIMESTAMP=`date +%Y-%m-%d_%H-%M-%S`
cd /home/ubuntu/binance-bot-websocket/
echo "[$TIMESTAMP] Starting binance-bot-websocket order monitoring service..."
echo "[$TIMESTAMP] Starting binance-bot-websocket order monitoring service..." >> status.log
. venv/bin/activate
nohup python binance-bot-websocket.pyz > info.log 2> error.log &
echo "[$TIMESTAMP] Service started."
echo "[$TIMESTAMP] Service started." >> status.log