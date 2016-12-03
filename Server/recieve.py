
import socket
import errno
import sys
import os
import random
import fnmatch
import sqlite3
import time
from zipfile import *

def checkDatabase (clientID, clientPWD, clientTOK):
	connection = sqlite3.connect('siem_site/test.sqlite3')
	if clientTOK == 'none':
		cursor = connection.execute("SELECT user, pass from auth where user = ? AND pass = ?", (clientID, clientPWD,))
		data = cursor.fetchone()
		if not data:
			#print('login failed')
			return 0
		else:
			token = random.randrange(100000, 999999)
			connection.execute("DELETE FROM auth WHERE USER = ?", (clientID,));
			connection.execute("INSERT INTO auth VALUES (?, ? , ?)", (clientID, clientPWD, token,));
			connection.commit()
			#print('login succeeded')
			return token
	else:
		cursor = connection.execute("SELECT user, pass, token from auth where user = ? AND pass = ? AND token = ?", (clientID, clientPWD, clientTOK,))
		data = cursor.fetchone()
		if not data:
			#print('login failed')
			return 0
		else:
			#print('login succeeded')
			return 1

########### Make a backup of the new file if a file already exists with the same name ###########
def makeBackup (filename, clientID):
	backupCounter = 0
	if os.path.isfile('/UserStorage/' + clientID + '/' + filename):
		pass
	while (1):
		if os.path.isfile('/UserStorage/' + clientID + '/' + filename + '.bak' + backupCounter):
			backupCounter += 1
		else:
			os.rename('/UserStorage/' + clientID + '/' + filename, '/UserStorage/' + clientID + '/' + filename + '.bak' + backupCounter)
			break


########## Authenticate the user before trying to recieve a file :) ##########
def authUser(conn, addr):
	#tryCount = 0

	#Try to authenticate the user 5 times
	#while tryCount < 5:
	while (1):
		#tryCount += 1
		#Try to recieve login information from the client
		#print ('getting info')
		try:
			data = conn.recv(1024)
			clientID = data.decode('utf-8')
			data = conn.recv(1024)
			clientPWD = data.decode('utf-8')
			data = conn.recv(1024)
			clientTOK = data.decode('utf-8')
		#Detect if client breaks or loses connection
		except socket.error as e:
			#Output if client closed the connection
			if e.errno == errno.EPIPE:
				print ('\tConnection closed at ' + addr[0])
				#kill the current child process
				os._exit(0)
			#Output if another error has occured
			else:
				print ('\tError: ' + e + ' at ' + addr[0])
				os._exit(0)

		#print ('checking database')
		result = checkDatabase (clientID, clientPWD, clientTOK)
		if result > 1:
			conn.send(str.encode('welcome'))
			conn.send(str.encode(str(result)))
			break
		elif result == 1:
			conn.send(str.encode('welcome'))
			break
		else:
			conn.send(str.encode('Invalid Login'))

	recieveZipFile(conn, clientID, addr)

########## keeping so we can still test if database isnt working yet ###########
def oldConnect ():
	authCheck = open ("/home/debo/SoftEng/Section-9-SIEM/Server/users.txt", "r+")
	confUser = 0
	tryCount = 0

	#Try to authenticate the user 5 times
	while tryCount < 5 and confUser == 0:
		authCheck.seek(0, 0)
		cont = 0
		counter = 0
		userPasses = 0
		token = 0
		redo = 0
		needTok = 0
		for userInfo in authCheck:
			userPasses += 1
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
					try:
						conn.send(str.encode('welcome'))
					except socket.error as e:
						if e.errno == errno.EIPIE:
							print ('\tConnection closed at ' + addr[0])
							os._exit(0)
						else:
							print ('\tError: ' + e + ' at ' + addr[0])
							os._exit(0)
					confUser = 1
					break
				elif clientTOK == 'none' and cont == 2:
					try:
						conn.send(str.encode('welcome'))
						token = random.randrange(100000, 999999)
						conn.send(str.encode(str(token)))
					except socket.error as e:
						if e.errno == errno.EPIPE:
							print ('\tConnection closed at ' + addr[0])
							os._exit(0)
						else:
							print ('\tError: ' + e + ' at ' + addr[0])
							os._exit(0)
					confUser = 1
					newTok = 1
					break
				else:
					cont = 0
					counter = 0

		if confUser == 1:
			break

		if (userPasses % 2) == 0 and (userPasses % 3) != 0:
			if clientTOK == 'none':
				try:
					conn.send(str.encode('welcome'))
					token = random.randrange(100000, 999999)
					conn.send(str.encode(str(token)))
				except socket.error as e:
					if e.errno == errno.EPIPE:
						print ('\tConnection closed at ' + addr[0])
						os._exit(0)
					else:
						print ('\tError: ' + e + ' at ' + addr[0])
						os._exit(0)
				needTok = 1
				break
		else:
			try:
				conn.send(str.encode('Invalid Login'))
			except socket.error as e:
				if e.errno == errno.EPIPE:
					print ('\tConnection closed at ' + addr[0])
					os._exit(0)
				else:
					print ('\tError: ' + e + ' at ' + addr[0])
					os._exit(0)

		tryCount += 1

	if needTok == 1:
		authCheck.seek(0, 0)
		while redo < userPasses:
			authCheck.readline()
			redo += 1
		authCheck.truncate()
		authCheck.write(str(token) + '\n')
	recieveZipFile(conn, clientID, addr)

########## Reccieve, store, extract the zip files containing the log files ##########
def recieveZipFile(conn, clientID, addr):
	#Create the storage path for the users if the folder does not yet exist
	userPath = r'/UserStorage/'
	if not os.path.exists(userPath):
		#set the permisions so only root can access the folder
		os.makedirs(userPath, mode = 700)

	#Create a zip file including the client's ID
	file = open("/UserStorage/" + clientID + ".zip", "wb")

	#Keep recieving data from the client and copying it into the create zip file
	while True:
		try:
			data = conn.recv(1024)
			file.write (data)
		#stop it the client has no more data to send
		except ConnectionResetError:
			break
		#quit if the connection ends abruptly
		except socket.error as e:
			if e.errno == errno.EPIPE:
				print ('\tConnection closed as ' + clientID + ' at ' + addr[0])
				os._exit(0)
			else:
				print ('\tError: ' + e + ' as ' + clientID + ' at ' + addr[0])
				os._exit(0)
		#stop at the end of the file
		if not data:
			break
	#close and save the file
	file.close()


	#check if the storage for the users exists, if not create it as root only
	currentUserPath = r'/UserStorage/' + clientID + '/'
	if not os.path.exists(currentUserPath):
		os.makedirs(currentUserPath, mode = 700)

#	for filename in os.listdir('/UserStorage/' + clientID + '/'):
#		if fnmatch.fnmatch(filename, 'bashhist*.log'):
#			makeBackup(filename)
#		if fnmatch.fnmatch(filename, 'timestamp*.txt'):
#			makeBackup(filename)

	#try and open the extract the zip file tho the client's folder
	try:
		zipArch = ZipFile ("/UserStorage/" + clientID + ".zip", "r")
		zipArch.extractall("/UserStorage/" + clientID + "/")
		zipArch.close()
		for pack in os.listdir("/UserStorage/" + clientID + "/"):
			if fnmatch.fnmatch(pack, 'package_*.zip'):
				zipArch = ZipFile ("/UserStorage/" + clientID + "/" + pack.strip('\n'), "r")
				zipArch.extractall("/UserStorage/" + clientID + "/")
				zipArch.close()
				print ('extracted')
				timestamp = open ("/UserStorage/" + clientID + "/USERINFO", "r")
				coltime = timestamp.readline().strip('\n')
				timestamp.close()
				#for file in os.listdir("/UserStorage/" + clientID + "/"):
				if os.path.isfile("/UserStorage/" + clientID + "/bashhist.log"):
					os.rename ("/UserStorage/" + clientID + "/bashhist.log", "/UserStorage/" + clientID + "/bashhist." + coltime + ".log")
				os.remove("/UserStorage/" + clientID + "/" + pack)
	#catch if the zip file is invalid
	except BadZipFile:
		print ('\tError extracting zip file as ' + clientID + ' at ' + addr[0])
		conn.close()
		os._exit(0)

	#display everything completed successfully
	print ('\tCompleted successfuly as ' + clientID + ' at ' + addr[0] + '\n')
	conn.close()
	os._exit(0)

#main part of the program
if __name__ == '__main__':
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	port = 3000
	host = ''

	try:
		s.bind((host, port))
	except socket.error as e:
		print(str(e))

	s.listen(100)
	print('Listening for connections:')

	while (1):

		#wait until a connection is recieved
		try:
			conn, addr = s.accept()
		except KeyboardInterrupt:
			print ('Reciever closed')
			os._exit(0)
		print ('Connected to: '+addr[0]+':'+str(addr[1]))

		#create a child which will 
		cld = os.fork()
		if cld == 0:
			suc = authUser(conn, addr)
			if suc == 1:
				print ('\tOperation failed at ' + addr[0] + '\n')
