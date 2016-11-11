
import socket
import sys
from _thread import *
from zipfile import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
port = 3000
host = ''

try:
	s.bind((host, port))
except socket.error as e:
	print(str(e))

s.listen(100)
print('Listening for connections')

def threaded_client(conn):
	data = conn.recv(1024)
	clientID = data.decode('utf-8')
	data = conn.recv(1024)
	clientPWD = data
	data = conn.recv(1024)
	clientTOK = data
	authUser = 0

	authCheck = open ("/home/matrix/testing/Server/users.txt", "r")

	for user in authCheck:
		if clientID = f.readline():
			if 
		file = open("/home/matrix/testing/Server/tmp/myData.zip", "w+b")

		while True:
			try:
				data = conn.recv(1024)
				file.write (data)
			except ConnectionResetError:
				break
			if not data:
				break
		file.close()
		zipArch = ZipFile ("myData.zip", "r")
		zipArch.extractall("/home/matrix/testing/Server/clientInfo")
		conn.close()
		zipArch.close()
		authUser = 1

while (1):

	conn, addr = s.accept()
	print ('connected to: '+addr[0]+':'+str(addr[1]))

	start_new_thread(threaded_client,(conn,))
