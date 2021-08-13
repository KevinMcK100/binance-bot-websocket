#!/bin/bash

TIMESTAMP=`date +%Y-%m-%d_%H-%M-%S`
cd /home/ubuntu/binance-bot-websocket
echo "[$TIMESTAMP] Starting log file cleanup..."
echo "[$TIMESTAMP] Starting log file cleanup..." >> status.log

ARCHIVE_DIR=archive
if [ -d $ARCHIVE_DIR ]; then
    rm -rf $ARCHIVE_DIR
fi

mkdir $ARCHIVE_DIR
DATE=`date "+%Y%m%d"`
mv info.log $ARCHIVE_DIR/info-$DATE.log
mv error.log $ARCHIVE_DIR/error-$DATE.log
mv app.py.log $ARCHIVE_DIR/app.py-$DATE.log
mv status.log $ARCHIVE_DIR/status-$DATE.log

echo "[$TIMESTAMP] Log cleanup complete. All log files moved to $ARCHIVE_DIR directory"
echo "[$TIMESTAMP] Log cleanup complete. All log files moved to $ARCHIVE_DIR directory" >> status.log

./restart.sh