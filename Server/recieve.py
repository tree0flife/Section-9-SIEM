import socket
import sys
import os
import random
#from _thread import *
#from multiprocessing import Pool
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
	print (os.getlogin())
	authCheck = open ("/home/matrix/testing/Server/users.txt", "r+")
	confUser = 0

	while confUser == 0:
		authCheck.seek(0, 0)
		cont = 0
		counter = 0
		userPasses = 0
		token = 0
		redo = 0
		needTok = 0
		print ('Getting user info:')
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
			#	print (clientID)
				if clientID == userInfo:
					print ('\tUsername: pass')
					cont = 1
					counter = 1
				else:
					print ('\tUsername: fail')
					cont = 0
					counter = 1
			elif counter == 1:
			#	print (clientPWD)
				if clientPWD == userInfo and cont == 1:
					print ('\tPassword: pass')
					cont = 2
					counter = 2
				else:
					print ('\tPassword: fail')
					cont = 0
					counter = 2
			elif counter == 2:
			#	print (clientTOK)
				if clientTOK == userInfo and cont == 2:
					print ('\tToken: match')
					conn.send(str.encode('welcome'))
					confUser = 1
					break
				elif clientTOK == 'none' and cont == 2:
					print ('\tToken: generating')
					conn.send(str.encode('welcome'))
					token = random.randrange(100000, 999999)
					conn.send(str.encode(str(token)))
					#authCheck.seek(savePos)
					#authCheck.write(str(token) + '\n')
					confUser = 1
					newTok = 1
					break
				else:
					print ('\tToken: fail')
					cont = 0
					counter = 0

		if confUser == 1:
			break

		#print ('got here')
		if (userPasses % 2) == 0 and (userPasses % 3) != 0:
			if clientTOK == 'none':
				print ('empty token')
				conn.send(str.encode('welcome'))
				token = random.randrange(100000, 999999)
				conn.send(str.encode(str(token)))
				needTok = 1
				break
		else:
			conn.send(str.encode('Invalid Login'))
			print ('sent failed message')

	if needTok == 1:
		authCheck.seek(0, 0)
		#print (str(userPasses))
		while redo < userPasses:
			authCheck.readline()
			redo += 1
		authCheck.truncate()
		#authCheck.seek(userPasses, 0)
		print (authCheck.readline().rstrip('\n') + " TEST")
		#authCheck.seek(-1, 1)
		#print ("This is the token: " + str(token))
		authCheck.write(str(token) + '\n')
	threaded_client(conn, clientID)

def threaded_client(conn, clientID):
	#conn.send(str.encode("Login Succeeded"))
	userPath = r'/UserStorage/'
	if not os.path.exists(userPath):
		os.makedirs(userPath, mode = 700)
	file = open("/UserStorage/" + clientID + ".zip", "wb")
	#zipArch = ZipFile ("/UserStorage/" + clientID + ".zip", "w")

	#with ZipFile('/UserStorage/' + clientID + '.zip', 'w') as zipArch:
	while True:
		try:
			data = conn.recv(1024)
			file.write (data)
		except ConnectionResetError:
			break
		if not data:
			break
	file.close()

	currentUserPath = r'/UserStorage/' + clientID + '/'
	if not os.path.exists(currentUserPath):
		os.makedirs(currentUserPath)

	try:
		zipArch = ZipFile ("/UserStorage/" + clientID + ".zip", "r")
	#except BadZipFile:
		#print ('Error reading zip file')
		#zipArch.close()

	#try:
		#print (zipArch.getinfo(date_time))
		#with zipArch.open("auth.log") as pack:
		#	print (pack.getinfo(date_time))
		zipArch.extractall("/UserStorage/" + clientID + "/")
		zipArch.close()
	except BadZipFile:
		print ('Error extracting zip file')

	print ('Completed successfuly')
	conn.close()
	os._exit(0)

while (1):

	conn, addr = s.accept()
	print ('connected to: '+addr[0]+':'+str(addr[1]))

	#start_new_thread(authUser,(conn,)) enable this again when complete
	cld = os.fork()
	if cld == 0:
		try:
			authUser(conn)
		except socket.error as e:
			if e.error == errno.EPIPE:
				print ('Connection closed')
			else:
				print ('Error: ' + e)
