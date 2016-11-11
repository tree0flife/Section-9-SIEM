#!/usr/bin/python

import os
import re
import zipfile
import shutil
import getpass
#from pyutmp import UtmpFile

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
# 		            Open file                           #
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
# 		     Begin Zipping and Cleanup			#
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
#			   System Logs			        #
# 			    ( MAIN )                            #
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
