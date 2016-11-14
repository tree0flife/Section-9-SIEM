#!/usr/bin/python

import os
import re
import time
import zipfile
import shutil
import getpass
#from pyutmp import UtmpFile

#------------------------Class Definition------------------------#
class globs(object):

    def __init__(self, user, path, package):
        self.user = getpass.getuser() 
        self.path = None
	self.package = 0 
        self.setup(self.user, self.path)

    def setup(self, user, path):
	self.path = '/home/%s/.bash_history' % self.user

#################################################################
# 		            Open file                           #
#################################################################
def openfile(name, rasp):
    output_file = open(name, 'w')
    if name == 'apt-hist.log':
        path = '/var/log/apt/history.log'
    elif name == 'bashhist.log':
        path = rasp.path
    else:
        path = '/var/log/%s' % name

    with open(path, 'r') as f:
        for line in f:
            output_file.write(line)
    output_file.close()
    f.close()

#################################################################
# 		     Begin Zipping and Cleanup			#
#################################################################
def cleanup(pathdir, rasp):

    record = '%s,%s' % (rasp.user, time.strftime('%d-%m-%Y_%H-%M-%S'))
    r = open(record, 'w')
    r.close()

    os.chdir(pathdir[:-5])

    zip_name = zipfile.ZipFile("package_" + rasp.package + ".zip", "w", zipfile.ZIP_DEFLATED)
    dirlist = os.listdir(pathdir)
    for list in dirlist:
        get_file = os.path.join(pathdir, list)
        zip_name.write(get_file, list)

    zip_name.close()
    shutil.rmtree(pathdir)

#################################################################
#			   RUN					#
#################################################################
def run(rasp):
	print "Working..."
	pathdir = os.getcwd() + '/temp'
	os.mkdir(pathdir, 0700)
	os.chdir(pathdir)


	openfile('dpkg.log', None)
	openfile('auth.log', None)
	openfile('kern.log', None)
	openfile('syslog', None)
	openfile('apt-hist.log', None)
	openfile('bashhist.log', rasp)

	cleanup(pathdir, rasp)
	print "Done.."

#################################################################
#			   System Logs			        #
# 			    ( MAIN )                            #
#################################################################
def execute(idle, q):

    rasp = globs()
    run(rasp)

    # If idle is 1, the client could not establish a connection
    # The collector will continuously run until its notified a connection has been made
    if idle == 1:
	time = 0
	while q.empty() == True:
	    time.sleep(1)
	    time += 1
	    if time == 300:
		rasp.package += 1
		run(rasp)
    else:
	run(rasp)
