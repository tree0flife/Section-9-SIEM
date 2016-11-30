import os
import fnmatch
import time

########## Parse the bash files ##########
def runBash (filename, folder):
	#Formating for clarity in output
	print ("\nUser: " + folder)
	print ("File: " + filename)

	#Open the file to parse and create a list of key terms to search for
	fileToParse = open ("/UserStorage/" + folder + "/Parsing" + filename)
	keyTerms = ('nmap', 'sudo', 'cp', 'rm', 'ps', 'chmod', 'chown', 'netstat', 'kill', 'pid', 'apt', 'stat')

	#Parse the file and search for key terms
	for line in fileToParse:
		line = line.rstrip('\n')
		for term in keyTerms:
			if fnmatch.fnmatch (line, term + "*"):
				#send flag to database
				#print ('Flagged command: ' + line)
				nothing = 1
		if 'su' == line or fnmatch.fnmatch (line, 'su *') or fnmatch.fnmatch (line, '*/ *') or fnmatch.fnmatch (line, '*/'):
			#send flag to database
			#print ('Flagged command: ' + line)
			nothing = 1
	fileToParse.close()

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

if __name__ == '__main__':
	#constantly running features:
		#parse bash (done but can add more terms)
		#parse pcap (have to discuss what we are looking for)
		#scan user storage folder for usernames (done)
		#check if file to parse exists (done)
		#parse then move file file to permanent folder (done)
		#use multiprocessing (done)

	count = 0
	#while (count < 1):
	while (1):
		#print(time.strftime('%d-%m-%Y_%H-%M-%S'))
		count += 1
		for folder in os.listdir("/UserStorage/"):
			if os.path.isdir("/UserStorage/" + folder):
				for filename in os.listdir("/UserStorage/" + folder + "/"):
					if fnmatch.fnmatch("/UserStorage/" + folder + "/" + filename, "/UserStorage/" + folder + "/" + "Parsing*"):
						continue
					else:
						try:
							if fnmatch.fnmatch (filename, "*.bak*"):
								fileString = "/UserStorage/" + folder + "/" + filename
								backupStart = fileString.find (".bak")
								backupNumber = int(fileString[backupStart + 4:])
								backupNumberDigits = len(fileString) - 54
								if backupNumber == 0 and not os.path.isfile(fileString[:-5]):
									os.rename(fileString, fileString[:-5])
								elif backupNumber > 0  and not os.path.isfile(fileString[:-(4 + backupNumberDigits)]):
									os.rename(fileString, fileString[:-(backupNumberDigits)] + str(backupNumber-1))
							else:
								os.rename ("/UserStorage/" + folder + "/" + filename, "/UserStorage/" + folder + "/Parsing" + filename)
								child = os.fork()
								if child == 0:
									if fnmatch.fnmatch("/UserStorage/" + folder + "/Parsing" + filename, "/UserStorage/" + folder + "/" + "Parsingbashhist*.log"):
										runBash(filename, folder)
									os._exit(0)
						except FileNotFound:
							print ("File " + filename + " was no longer found")
