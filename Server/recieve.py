
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
	#conn.send(str.encode('Welcome\n'))

	#zipArch = ZipFile ("myData.zip", "w")
	# file = open("myData.zip", "ab")

	file = open("myData.zip", "w+b")

	#while True:
	#filesize = conn.recv(1024)
	#data = conn.recv(1024)

	#print ("loop 1")
	#reply = 'Server output: ' + data.decode('utf-8')
	while True:
		try:
			data = conn.recv(1024)
			file.write (data)
		except ConnectionResetError:
			break
		if not data:
			break
	#conn.sendall(str.encode(reply))
	file.close()
	#zipArch = ZipFile ("myData.zip", "r")
	#zipArch.extractall("/home/matrix/info")
	conn.close()
	#zipArch.close()
	print ("I'm done!")

while (1):

	conn, addr = s.accept()
	print ('connected to: '+addr[0]+':'+str(addr[1]))

	start_new_thread(threaded_client,(conn,))
