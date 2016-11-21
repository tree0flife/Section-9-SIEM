#!/usr/bin/python

# TARGET IP:PORT    24.150.80.188 : 3000

import socket
import sys
import time
import os #for filesize Ryan
import collector
from multiprocessing import Process, Queue

# not yet implemented in this program. Considering using SCAPY Lib.
# from tear import pcapkiller 


#################################################################
#			CREATE CONNECTION			#
#################################################################
def createConnection(flag): #create connection to client Ryan
    counter = 1
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            # sock.connect(("localhost", 9999)) # for testing locally
            sock.connect(('24.150.80.188', 3000))
            print '[+] Connected'
	    return sock

        except socket.error:
	    print '[-] Connection [' + str(counter) + '] Refused - Retrying'
            time.sleep(5)

	    counter += 1
	    if flag == 1:
		continue

	    if counter == 4:
		return -1

#################################################################
#                        AUTHENTICATION                         #
#	 NOTE: need to clean up or put in another module	#
#################################################################
def login(sock): #login to the server Ryan
    try:
        authCheck = open ("creds.txt", "r+")
    except IOError:
        authCheck = open ("creds.txt", "w")

    if os.stat("creds.txt").st_size == 0:
    	while True:
	    username = raw_input('Enter your username: ')
	    password = raw_input('Enter your password: ')
	    tok = 'none'
	    sock.send(username)
	    time.sleep(1)
	    sock.send(password)
	    time.sleep(1)
	    sock.send(tok)
	    print 'waiting for server response'
	    response = sock.recv(1024).decode('utf-8')
	    print 'got response'
	    if response == 'welcome':
		print 'accepted'
		authCheck.write(username + '\n')
		authCheck.write(password + '\n')
		print 'waiting for token'
		tok = sock.recv(1024).decode('utf-8')
		print 'got token'
		authCheck.write(tok + '\n')
		break
	    else:
		print 'Login failed, please try again'
    else:
    	clientID = authCheck.readline().rstrip('\n')
	clientPWD = authCheck.readline().rstrip('\n')
	clientTOK = authCheck.readline().rstrip('\n')
	sock.send(clientID)
	time.sleep(1)
        sock.send(clientPWD)
	time.sleep(1)
        sock.send(clientTOK)
        response = sock.recv(1024).decode('utf-8')
        if response != 'welcome':
	    print 'Login failed, please try again'
	    while True:
		username = raw_input('Enter your username: ')
		password = raw_input('Enter your password: ')
		tok = 'none'
		sock.send(username)
		time.sleep(1)
		sock.send(password)
		time.sleep(1)
		sock.send(tok)
		print 'waiting for server response'
		response = sock.recv(1024).decode('utf-8')
		print 'got response'
		if response == 'welcome':
			print 'accepted'
			authCheck.write(username + '\n')
			authCheck.write(password + '\n')
			print 'waiting for token'
			tok = sock.recv(1024).decode('utf-8')
			print 'got token'
			authCheck.write(tok + '\n')
			break
		else:
			print 'Login failed, please try again'

#################################################################
#                          DISPATCH                             #
#	NOTE: need to check for connection before sending	#
#################################################################
def dispatch(sock):
    print '[*] Opening file'
    f = open('final_package.zip', 'rb')
    l = f.read(1024)
    print '[*] Sending file'
    while(l):
        sock.send(l)
        l = f.read(1024)

    f.close()
    sock.close()
    print '[*] SUCCESS'
    print '[*] Connection closed'


#################################################################
#                                                               #
#                           ( MAIN )                            #
#                                                               #
#################################################################
if __name__ == "__main__":

    sock = createConnection(0)

    # If client cannot establish connection, fork. Have the parent continuously try to
    # connect. And have the child continuously collect log data
    if sock == -1:
	q = Queue()
	p = Process(target=collector.execute, args=(1, q))
	p.start()
	sock = createConnection(1)
	q.put('done')
	p.join()

    # login(sock)

    # Initial Execute and Dispatch 
    collector.execute(0, None)
    dispatch(sock)

    # sock.close()


    # NOTE: need to modify to watch for certain messages(signals) sent from the server
    #       (ex. server sends REFRESH, client execute()'s and sends data)
    #
    #       So should there be a constant connection between client and server? I Could fork
    #	    another process that waits for incoming connections and when it recieves
    #	    one from the server. The server will send a message like REFRESH, then send a
    #	    signal to this process that "speeds up" the collection and sends it off.
    while True:
        #time.sleep(300)
        time.sleep(30)
        print 'collecting...'
        collector.execute(0, None)
        print 'sending...'
        dispatch(sock)
