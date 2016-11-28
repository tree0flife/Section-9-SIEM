#!/bin/bash

spam=`pidof python client.py`

pid2=`echo $spam | cut -d ' ' -f1`
pid1=`echo $spam | cut -d ' ' -f2`

if [ "$pid2" -gt "$pid1" ]; then
    kill -s SIGTERM $pid2
    echo "killed a child! you sicko!"
fi

kill -s SIGTERM $pid1
echo "killed the parent"
