
import socket
import sys
import random
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

def authUser(conn):
	data = conn.recv(1024)
	clientID = data.decode('utf-8')
	data = conn.recv(1024)
	clientPWD = data
	data = conn.recv(1024)
	clientTOK = data
	confUser = 0

	authCheck = open ("/home/matrix/testing/Server/users.txt", "r")

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
	
	if confUser == 0:
		conn.send(str.encode("Login Failed")

	else
		threaded_client(conn)

def threaded_client(conn):
	conn.send(str.encode("Login Succeeded"))
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

	start_new_thread(authUser,(conn,))
