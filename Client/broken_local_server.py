#!/usr/bin/python


#############################################
#					    #
#	Test Server for local machine	    #
#					    #
#############################################

import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", 9999))
sock.listen(10)

i = 0
while True:

    sc, address = sock.accept()
    print '[*] ADDRESS:', address, 'connected'

    f = open('file_' + str(i) + '.zip', 'wb')
    i += 1 # to identify each file/connection
    while True:
        l = sc.recv(1024)
        while(l):
            f.write(l)
            l = sc.recv(1024)
    f.close()
    sc.close()
    break
    
sock.close()

