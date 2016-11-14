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
	authCheck = open ("/home/matrix/testing/Server/users.txt", "r+")
	confUser = 0

	while True:
		cont = 0
		counter = 0
		print ('getting user info')
		data = conn.recv(1024)
		clientID = data.decode('utf-8')
		data = conn.recv(1024)
		clientPWD = data.decode('utf-8')
		data = conn.recv(1024)
		clientTOK = data.decode('utf-8')
		print ('checking info')
		for userInfo in authCheck:
			userInfo = userInfo.rstrip('\n')
			if counter == 0:
				if clientID == userInfo:
					cont = 1
					counter = 1
				else:
					cont = 0
					counter = 1
			elif counter == 1:
				if clientPWD == userInfo and cont == 1:
					cont = 2
					counter = 2
				else:
					cont = 0
					counter = 2
			elif counter == 2:
				if clientTOK == userInfo and cont == 2:
					print ('matched token')
					conn.send(str.encode('welcome'))
					confUser = 1
					break
				elif clientTOK == 'none' and cont == 2:
					print ('empty token')
					conn.send(str.encode('welcome'))
					token = random.randrange(100000, 999999)
					conn.send(str.encode(str(token)))
					authCheck.write(str(token))
					confUser = 1
					break
				else:
					print ('token mismatch')
					cont = 0
					counter = 0
		if confUser == 0:
			conn.send(str.encode('Invaild Login'))
			print ('sent failed')
		elif confUser == 1:
			break

	threaded_client(conn)

def threaded_client(conn):
	#conn.send(str.encode("Login Succeeded"))
	file = open("/home/matrix/testing/Server/tmp/myData.zip", "wb")

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
