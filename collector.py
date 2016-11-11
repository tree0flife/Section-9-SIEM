#!/usr/bin/python

import os
import re
import zipfile
import shutil
import getpass
#from pyutmp import UtmpFile.

class globs(object):
	
	def __init__(self):
		self.user = []
		self.path = []
		self.setup(self.user, self.path)
	
    # apt-history individual ???
	def setup(self, user, path):
		spam = os.listdir('/home/')

		for line in spam:
			self.user.append(line)
			self.path.append('/home/%s/.bash_history' % line)

#################################################################
# 					        Open file                           #
#################################################################
def openfile(name, rasp):
	output_file = open(name, 'w')
	if name == 'apt-hist.log':
		path = '/var/log/apt/history.log'
	elif name == 'bashhist.log':
		path = rasp.path[0]
	else:
		path = '/var/log/%s' % name

	with open(path, 'r') as f:
		for line in f:
			output_file.write(line)
	output_file.close()
	f.close()

#################################################################
# 					Begin Zipping and Cleanup					#
#################################################################
def cleanup(pathdir):
    os.chdir(pathdir[:-5])

    zip_name = zipfile.ZipFile("package.zip", "w", zipfile.ZIP_DEFLATED)
    dirlist = os.listdir(pathdir)
    for list in dirlist:
        get_file = os.path.join(pathdir, list)
        zip_name.write(get_file, list)

    zip_name.close()
    shutil.rmtree(pathdir)

#################################################################
# 							System Logs							#
# 						     ( MAIN )                           #
#################################################################
#if __name__ == "__main__":
def execute():

    print "Working..."
    pathdir = os.getcwd() + '/temp'
    os.mkdir(pathdir, 0700)
    os.chdir(pathdir)

    rasp = globs()

    openfile('dpkg.log', None)
    openfile('auth.log', None)
    openfile('kern.log', None)
    openfile('syslog', None)
    openfile('apt-hist.log', None)
    openfile('bashhist.log', rasp)

    cleanup(pathdir)
    print "Done.."

#For when the user logged in (Requires py-utmp)
#
#utmp_o = open("utmp.log", "w")
#for utmp in UtmpFile():
#	if utmp.ut_user_process:
#		utmp_o.write('%s logged in at %s on tty %s\n' % (utmp.ut_user, time.ctime(utmp.ut_time), utmp.ut_line))
#utmp_o.close()


#################################################################
# 							Browser Logs						#
# 								NOTE: 							#
#	Network logs (traffic) could be better logged from pcaps	#
#################################################################
#chrome_o = open("chromehist.log", "w")
#dbpath = '/home/%s/.config/google-chrome/Default/History' % rasp.user[0] # error here obv
#conn = sqlite3.connect(dbpath)
#cursor = conn.execute("SELECT * from urls")
#for line in cursor:
#	chrome_o.write('%s || %s || %s\n' % (line[1].encode('utf-8'), line[2].encode('utf-8'), line[3]))
#chrome_o.close()
#
#chrome_d_o = open("chromedl.log", "w")
#cursor_d = conn.execute("SELECT tab_url, url from downloads AS C JOIN downloads_url_chains AS R ON C.id=R.id")
#for line in cursor_d:
#	chrome_d_o.write('%s ||| %s\n' % (line[0], line[1]))
#chrome_d_o.close()
#
#
#profilepath = '/home/%s/.mozilla/firefox/profiles.ini' % user[0]
#tmp = open(profilepath, 'r')
#for line in tmp:
#	match = re.match(r'Path=', line, re.M|re.I)
#	if match:
#		profilepath = '/home/%s/.mozilla/firefox/%s' % (user[0], line[5:-1])
#		break
#tmp.close()
#
#firefox_o = open("firefox.log", "w")
#firefox_o.close()
