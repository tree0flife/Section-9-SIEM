#!/bin/bash

name=siem9

if [[ $USER != "root" ]]; then
    echo "You will have errors if you don't run this as root"
    exit
fi

case "$1" in 
    'install')
        mkdir /root/siem9
        cp client.py /root/siem9
        cp collector.py /root/siem9
        cp tear.py /root/siem9
        chmod 750 /root/siem9/*
        
        cp siem9 /etc/init.d/$name

	update-rc.d -f $name remove
	update-rc.d $name defaults

        echo 'successfully installed.'
        ;;
    'uninstall')
	update-rc.d -f $name remove

        rm -r /root/siem9
        rm /etc/init.d/siem9

	su $USER -c "systemctl daemon-reload"

        echo 'successfully uninstalled.'
        ;;
    *)
        echo "usage: install|uninstall"
        ;;
esac
