#!/usr/bin/python

# TARGET IP:PORT    24.150.80.188 : 3000

import signal
import re
import socket
import sys
import time
import os 
import collector
from multiprocessing import Process, Queue
import subprocess as sub


#################################################################
#			CREATE CONNECTION			#
#################################################################
def createConnection(flag): #create connection to client Ryan
    counter = 1
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            #sock.connect(("localhost", 9999)) # for testing locally
            sock.connect(('24.150.80.188', 3000))
	    if flag == 2:
		return sock
            login(sock)
            print '[+] Connected'
            return sock

        except socket.error:
            print '[-] Connection [' + str(counter) + '] Refused - Retrying'
            time.sleep(5)

            counter += 1
            if flag == 1:
                time.sleep(1)
                continue

            if counter == 4:
                return -1

#################################################################
#                        AUTHENTICATION                         #
#################################################################
def login(sock): #login to the server

    pathdir = '/root/siem9/UserCreds/';

    if not os.path.exists(pathdir):
        os.makedirs(pathdir)

    #Check file user creds already stored, if not create a file file to store them
    try:
        authCheck = open (pathdir + 'creds.txt', "r+")
    except IOError:
        authCheck = open (pathdir + 'creds.txt', "w")

    #Check if the file was just created, otherwise read the file and send login info
    if os.stat(pathdir + "creds.txt").st_size == 0:
        #repeat until successful login
        while True:
            #get login info from user
            username = raw_input('\tEnter your username: ')
            password = raw_input('\tEnter your password: ')
            tok = 'none'
            #send login info to server (wait times are so they don't combine)
            sock.send(username)
            time.sleep(1)
            sock.send(password)
            time.sleep(1)
            sock.send(tok)
            #get response if login was successful or not
            response = sock.recv(1024).decode('utf-8')
            #if the login was successful save the login info to the file
            if response == 'welcome':
                authCheck.write(username + '\n')
                authCheck.write(password + '\n')
                #recieve token from server since first time login
                tok = sock.recv(1024).decode('utf-8')
                authCheck.write(tok + '\n')
                break
            else:
                print '[-] Login: Failed, please try again'
    else:
        #read login file and send info to server
        clientID = authCheck.readline().rstrip('\n')
        clientPWD = authCheck.readline().rstrip('\n')
        clientTOK = authCheck.readline().rstrip('\n')
        sock.send(clientID)
	print 'sent id'
        time.sleep(1)
        sock.send(clientPWD)
	print 'sent pass'
        time.sleep(1)
        sock.send(clientTOK)
	print 'sent token'
        #login status message from server
        response = sock.recv(1024).decode('utf-8')
        #ask for user to enter login info on fail
	print 'got response'
        if response != 'welcome':
            print '[-] Login: Failed, please try again'
            authCheck.close()
            os.remove(pathdir + "creds.txt")
            authCheck = open (pathdir + 'creds.txt', "w")
            #repeat until successful login
            while True:
                #ask user for login info
                username = raw_input('\tEnter your username: ')
                password = raw_input('\tEnter your password: ')
                tok = 'none'
                sock.send(username)
                time.sleep(1)
                sock.send(password)
                time.sleep(1)
                sock.send(tok)
                print '\twaiting for server response'
                response = sock.recv(1024).decode('utf-8')
                print '\tgot response'
                if response == 'welcome':
                    print '\taccepted'
                    authCheck.write(username + '\n')
                    authCheck.write(password + '\n')
                    print '\twaiting for token'
                    tok = sock.recv(1024).decode('utf-8')
                    print '\tgot token'
                    authCheck.write(tok + '\n')
                    break
                else:
                    print '\tLogin failed, please try again'

    authCheck.close()

#################################################################
#                     CONNECTION HANDLER                        #
#################################################################
def conn_handle(sock):
    # If client cannot establish connection, fork. Have the parent continuously try to
    # connect. And have the child continuously collect log data
    if sock == -1:
	q = Queue()
	p = Process(target=collector.execute, args=(1, q, str(sys.argv[1])))
	p.start()
        sock = createConnection(1)
	q.put('done')
	p.join()
        return sock
    return sock

#################################################################
#                          DISPATCH                             #
#################################################################
def dispatch(sock):
    dirlist=os.listdir('/root/siem9/')
    for line in dirlist:
        match = re.search(r'final_package_.*.zip', line, re.M|re.I)
        if (match):
            print '[*] Opening file'
            f = open(match.group(), 'rb')
            l = f.read(1024)
            print '[*] Sending file'
            while(l):
                try:
                    sock.send(l)
                    l = f.read(1024)
		    print f.tell()
		    if (f.tell() % 1024) > 0:
			sock.send(l)
			os.remove(match.group())
			break
                except socket.error:
		    print '[-] ERROR: No connection. Aborting.'
		    f.close()
		    sock.close()
		    return 1
	    f.close()

    time.sleep(1)
    sock.send('done')
    sock.close()
    print '[*] SUCCESS'
    print '[*] Connection closed'
    #return 0

#################################################################
#			    BUTTER				#
#################################################################
def butter(sock):
    output = open("/root/siem9/network", "w")
    myHost = sock.getsockname()[0]
    server = sub.Popen(('tcpdump', '-q', '-nn', 'host', myHost), stdout=output)
    return server, sock

#################################################################
#                        SIGNAL HANDLER                         #
#################################################################
def signal_handler(signal, frame):
    exit()

#################################################################
#                                                               #
#                           ( MAIN )                            #
#                                                               #
#################################################################
if __name__ == "__main__":

    signal.signal(signal.SIGTERM, signal_handler)

    sock = createConnection(2)
    sock = conn_handle(sock)
    sock.send('getting IP')
    p, sock = butter(sock)
    sock.close()

    # NOTE: need to modify to watch for certain messages(signals) sent from the server
    #       (ex. server sends REFRESH, client execute()'s and sends data)
    #
    #       So should there be a constant connection between client and server? I Could fork
    #	    another process that waits for incoming connections and when it recieves
    #	    one from the server. The server will send a message like REFRESH, then send a
    #	    signal to this process that "speeds up" the collection and sends it off.
    while True:
        time.sleep(15)
	p.terminate()
	p.wait()

        print 'collecting...'
        collector.execute(0, None, str(sys.argv[1]))
        print 'sending...'

        sock = createConnection(0)
        sock = conn_handle(sock)
	p, sock = butter(sock)
	dispatch(sock)
