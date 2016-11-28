#!/bin/bash

# put the entire command you used to run the client between ""
spam=`pgrep -f "python client.py"`
# PID=`pgrep -f "/usr/bin/python /root/siem9/client.py"`

pid2=`echo $spam | cut -d ' ' -f1`
pid1=`echo $spam | cut -d ' ' -f2`

if [ "$pid2" -gt "$pid1" ]; then
    kill -s SIGTERM $pid2
    echo "killed a child! you sicko!"
fi

kill -s SIGTERM $pid1
echo "killed the parent"
