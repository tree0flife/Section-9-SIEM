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
		authCheck.seek(0, 0)
		cont = 0
		counter = 0
		userPasses = 0
		token = 0
		redo = 0
		#print ('getting user info')
		data = conn.recv(1024)
		clientID = data.decode('utf-8')
		data = conn.recv(1024)
		clientPWD = data.decode('utf-8')
		data = conn.recv(1024)
		clientTOK = data.decode('utf-8')
		#print ('checking info')
		for userInfo in authCheck:
			#print (userInfo)
			userPasses += 1
			userInfo = userInfo.rstrip('\n')
			if counter == 0:
				if clientID == userInfo:
					#print ('correct user')
					cont = 1
					counter = 1
				else:
					#print ('incorrect user')
					cont = 0
					counter = 1
			elif counter == 1:
				if clientPWD == userInfo and cont == 1:
					#print ('correct pass')
					#savePos = authCheck.tell()
					cont = 2
					counter = 2
				else:
					#print ('incorrect pass')
					cont = 0
					counter = 2
			elif counter == 2:
				if clientTOK == userInfo and cont == 2:
					#print ('matched token')
					conn.send(str.encode('welcome'))
					confUser = 1
					break
				elif clientTOK == 'none' and cont == 2:
					#print ('empty token')
					conn.send(str.encode('welcome'))
					token = random.randrange(100000, 999999)
					conn.send(str.encode(str(token)))
					#authCheck.seek(savePos)
					#authCheck.write(str(token) + '\n')
					confUser = 1
					break
				elif cont == 2:
					#print ('token mismatch')
					cont = 0
					counter = 0
				else:
					print ('token failed')

		if confUser == 1:
			break

	if (userPasses % 2) == 0 and (userPasses % 3) != 0:
		if clientTOK == 'none':
			#print ('empty token')
			conn.send(str.encode('welcome'))
			token = random.randrange(100000, 999999)
			conn.send(str.encode(str(token)))
		else:
			conn.send(str.encode('Invalid Login'))
			print ('sent failed message')

	authCheck.seek(0, 0)
	#print (str(userPasses))
	while redo < userPasses:
		authCheck.readline()
		redo += 1
	authCheck.truncate()
	#authCheck.seek(userPasses, 0)
	print (authCheck.readline().rstrip('\n') + " TEST")
	#authCheck.seek(-1, 1)
	authCheck.write(str(token) + '\n')
	threaded_client(conn)

def threaded_client(conn):
	#conn.send(str.encode("Login Succeeded"))
	file = open("/home/matrix/testing/Server/tmp/myData.zip", "wb")
	#zipArch = ZipFile ("/home/matrix/testing/Server/tmp/myData.zip", "w")

	while True:
		try:
			data = conn.recv(1024)
			file.write (data)
		except ConnectionResetError:
			break
		if not data:
			break
	file.close()
	zipArch = ZipFile ("/home/matrix/testing/Server/tmp/myData.zip", "r")
	zipArch.extractall("/home/matrix/testing/Server/clientInfo")
	conn.close()
	zipArch.close()

while (1):

	conn, addr = s.accept()
	print ('connected to: '+addr[0]+':'+str(addr[1]))

	start_new_thread(authUser,(conn,))
