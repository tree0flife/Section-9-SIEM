
import os
import fnmatch
import time
import re
import sqlite3

def editFile(filename, folder, mode):
	oldLines = []
	curLine = 0
	with open("/UserStorage/" + folder + "/Parsing" + filename, "r") as oldFile:
		for line in oldFile:
			oldLines.append(line)

	if not (os.path.isfile("/UserStorage/" + folder + "/endOf" + mode)):
	    	return
	elif os.stat("/UserStorage/" + folder + "/endOf" + mode).st_size == 0:
		return
	else:
		endOfFile = open ("/UserStorage/" + folder + "/endOf" + mode, "r")

	endList = endOfFile.readlines()
	linesToCheck = sum(1 for line in open("/UserStorage/" + folder + "/endOf" + mode))

	if endOfFile:
		newFile = open("/UserStorage/" + folder + "/Parsing" + filename, "w")
		#numOfLines = sum(1 for line in open("/UserStorage/" + folder + "/Parsing" + filename))
		for line in oldLines:
			#print (endList[curLine].rstrip('\n') + "\t" + line.rstrip('\n') + "\t\t" + str(curLine) + "\t" + str(linesToCheck))
			if curLine == linesToCheck:
				newFile.write(line)
			elif line.rstrip('\n') == endList[curLine].rstrip('\n') and curLine < linesToCheck:
				curLine += 1
			elif curLine < linesToCheck:
				curLine == 0
		newFile.close()
	endOfFile.close()

########## Keep the last 25 lines of the previously parsed file ##########
def writeEndOfFile(filename, folder, mode):
	endOfFile = open ("/UserStorage/" + folder + "/endOf" + mode, "w")
	count = 0
	numOfLines = sum(1 for line in open("/UserStorage/" + folder + "/Parsing" + filename))

	with open("/UserStorage/" + folder + "/Parsing" + filename, "r") as file:
		for line in file:
			count += 1
			if count > numOfLines - 25:
				endOfFile.write(line)

	endOfFile.close()

########## Parse the bash files ##########
def run (filename, folder, mode, time):
	editFile(filename, folder, mode)

	#Formating for clarity in output
	print ("\nUser: " + folder)
	print ("File: " + filename)
	database = sqlite3.connect('siem_site/db.sqlite3')

	#Open the file to parse and create a list of key terms to search for
	fileToParse = open ("/UserStorage/" + folder + "/Parsing" + filename)
	if mode == 'Bash':
		table = 'core_bash_history'
		saveLocally, database = runBash(filename, folder, mode, fileToParse, database, time, table)
	elif mode == 'Network':
		table = 'core_network'
		saveLocally, database = runNetwork(filename, folder, mode, fileToParse, database, time, table)

	if database == 0:
		print ('saving')
		saveLocally.close()

	writeEndOfFile(filename, folder, mode)

	#Copy the saved data to the database if there is extra data to send and a connection
	if not (os.stat("/UserStorage/" + folder + "/databaseSave" + mode).st_size == 0):
		if database > 0:
			for line in saveLocally:
				database.execute("INSERT INTO " + table + " VALUES (?, ?, ?)", (folder, line, time))
				database.commit()
			saveLocally.close()
			os.remove("/UserStorage/" + folder + "/databaseSave" + mode)

	database.close()
	moveFile(filename, folder)
	#print ('Successfuly Ran')

def runNetwork (filename, folder, mode, fileToParse, database, time, table):
	keyTerms = ('24.150.80.188', '104.16.145.93', '66.147.244.82')
	#open file to save info if connection to database fails
	if os.path.isfile("/UserStorage/" + folder + "/databaseSave" + mode):
		saveLocally = open ("/UserStorage/" + folder + "/databaseSave" + mode, "a+")
	else:
		saveLocally = open ("/UserStorage/" + folder + "/databaseSave" + mode, "w+")

	#Parse the file and search for key terms
	for myline in fileToParse:
		next = 0
		#print (myline)
		myline = myline.rstrip('\n')
		line = myline.replace(".", " ").split()
		#print (line)
		#if len(line) > 6:
			#print (line)
			#print (line[3] + "." + line[4] + "." + line[5] + "." + line[6] +"\t" + keyTerms[0])
			#print (line[9] + "." + line[10] + "." + line[11] + "." + line[12])
		for term in keyTerms:
			#print ('checking')
			if next == 1:
				continue
			if len(line) > 12:
				ip = line[3] + "." + line[4] + "." + line[5] + "." + line[6]
				ip2 = line[9] + "." + line[10] + "." + line[11] + "." + line[12]
			if len(line) > 6 and ip == term:
				database, id = getID(database, table)
				if id >= 100:
					break
				spam = database.execute("INSERT INTO " + table + " VALUES (?, ?, ?, ?)", (id, folder, ip, time))
				database.commit()
				#print (spam)
				next = 1
				continue
				if database == 0:
					#print ('hi')
					#copy info to a file
					#print ("\tMatch: " + line[3] + "." + line[4] + "." + line[5] + "." + line[6])
					saveLocally.write(myline + "\n")
					continue
			elif len(line) > 12 and ip2 == term:
				database, id = getID(database, table)
				if id >= 100:
					break
				spam = database.execute("INSERT INTO " + table + " VALUES (?, ?, ?, ?)", (id, folder, ip2, time))
				database.commit()
				#print (spam)
				next = 1
				continue
				if database == 0:
					#print ('hi')
					#copy info to a file
					saveLocally.write(myline + "\n")
					continue

	database.commit()
	fileToParse.close()
	return saveLocally, database

def runBash (filename, folder, mode, fileToParse, database, time, table):
	keyTerms = ('nmap', 'sudo', 'cp', 'rm', 'ps', 'chmod', 'chown', 'netstat', 'kill', 'pid')
	#open file to save info if connection to database fails
	if os.path.isfile("/UserStorage/" + folder + "/databaseSave" + mode):
		saveLocally = open ("/UserStorage/" + folder + "/databaseSave" + mode, "a+")
	else:
		saveLocally = open ("/UserStorage/" + folder + "/databaseSave" + mode, "w+")

	#Parse the file and search for key terms
	for line in fileToParse:
		#print (line)
		next = 0
		line = line.rstrip('\n')
		for term in keyTerms:
			if next == 1:
				continue
			#print ('checking')
			if fnmatch.fnmatch (line, term + "*"):
				database, id = getID(database, table)
				if id >= 100:
					break
				database.execute("INSERT INTO " + table + " VALUES (?, ?, ?, ?)", (id, folder, term, time))
				database.commit()
				next = 1
				continue
				if database == 0:
					#print ('hi')
					#copy info to a file
					saveLocally.write(line + "\n")
					continue
			elif 'su' == line or fnmatch.fnmatch (line, 'su *') or fnmatch.fnmatch (line, '* / *') or fnmatch.fnmatch (line, '* /'):
				#send flag to database
				database, id = getID(database, table)
				if id >= 100:
					break
				database.execute("INSERT INTO " + table + " VALUES (?, ?, ?, ?)", (id, folder, term, time))
				database.commit()
				next = 1
				continue
				if database == 0:
					#print ('bye')
					#copy info to a file
					saveLocally.write(line + "\n")
					continue

	database.commit()
	fileToParse.close()
	return saveLocally, database

def getID(database, table):
	cursor = database.execute ("SELECT id from " + table)
	id = 0
	for row in cursor:
		id = row[0]
	id += 1
	return database, id

########## Move the file to a permanent location ##########
def moveFile(filename, folder):
	#Create Storage folder if it does not already exist
	storagePath = r'/PermanentStorage/'
	if not os.path.exists(storagePath):
		#set the permisions so only root can access the folder
		os.makedirs(storagePath, mode = 700)

	#Create user folder if it does not already exist
	userPath = r'/PermanentStorage/' + folder + '/'
	if not os.path.exists(userPath):
		#set the permisions so only root can access the folder
		os.makedirs(userPath, mode = 700)

	#Copy the file being parsed to permanent storage
	try:
		os.rename("/UserStorage/" + folder + "/Parsing" + filename, "/PermanentStorage/" + folder + "/" + filename)
	except FileNotFoundError:
		print ("Error moving file")
	#os.remove("/UserStorage/" + folder + "/Parsing" + filename)

if __name__ == '__main__':
	#constantly running features:
		#parse bash (done but can add more terms)
		#parse pcap (have to discuss what we are looking for)
		#scan user storage folder for usernames (done)
		#check if file to parse exists (done)
		#parse then move file file to permanent folder (done)
		#use multiprocessing (done)

	while (1):
		time.sleep(1)
		for folder in os.listdir("/UserStorage/"):
			if os.path.isdir("/UserStorage/" + folder):
				for filename in os.listdir("/UserStorage/" + folder + "/"):
					if fnmatch.fnmatch(filename, "Parsing*"):
						continue
					else:
						if fnmatch.fnmatch (filename, "*.bak*"):
							fileString = "/UserStorage/" + folder + "/" + filename
							backupStart = fileString.find (".bak")
							backupNumber = int(fileString[backupStart + 4:])
							backupNumberDigits = len(fileString) - 55
							if backupNumber == 0 and not os.path.isfile(fileString[:-5]):
								os.rename(fileString, fileString[:-5])
							elif backupNumber > 0  and not os.path.isfile(fileString[:-(4 + backupNumberDigits)]):
								os.rename(fileString, fileString[:-(backupNumberDigits)] + str(backupNumber-1))
						else:
							if fnmatch.fnmatch (filename, "bashhist*.log") or fnmatch.fnmatch (filename, "network*"):
								os.rename ("/UserStorage/" + folder + "/" + filename, "/UserStorage/" + folder + "/Parsing" + filename)
								child = os.fork()
								if child == 0:
									#print ('child ran')
									if fnmatch.fnmatch("/UserStorage/" + folder + "/Parsing" + filename, "/UserStorage/" + folder + "/" + "Parsingbashhist*.log"):
										run(filename, folder, "Bash", filename[16:33])
									elif fnmatch.fnmatch("Parsing" + filename, "Parsingnetwork*"):
										#print ('network ran')
										run(filename, folder, "Network", filename[15:32])
									else:
										print ('no match')
									os._exit(0)
