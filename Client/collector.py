#!/usr/bin/python

import os
import re
import time
import zipfile
import signal
import shutil
import getpass

login = "" 

#------------------------Class Definition------------------------#
class globs(object):

    def __init__(self, user):
        self.user = user 
	global login
	login = user
        self.pathdir = None 
        self.bashpath = '/home/%s/.bash_history' % self.user 
        self.package = 0

#################################################################
#                            OPEN FILE                          #
#################################################################
def openfile(name, rasp):
    output_file = open(name, 'w')
    if name == 'apt-hist.log':
        path = '/var/log/apt/history.log'
    elif name == 'bashhist.log':
        path = rasp.bashpath
    else:
        path = '/var/log/%s' % name
    with open(path, 'r') as f:
        for line in f:
            output_file.write(line)

    output_file.close()
    f.close()

#################################################################
#                            CLEANUP                            #
#################################################################
def cleanup(rasp):
    record = 'USERINFO'
    r = open(record, 'w')
    r.write(time.strftime('%d-%m-%Y_%H-%M-%S') + "\n")
    r.write(rasp.user)
    r.close()

    os.chdir(rasp.pathdir)

    zip_name = zipfile.ZipFile('package_' + str(rasp.package) + '.zip', 'w', zipfile.ZIP_DEFLATED)
    dirlist = os.listdir(rasp.pathdir + '/temp')
    for list in dirlist:
        get_file = os.path.join(rasp.pathdir + '/temp/', list)
        zip_name.write(get_file, list)

    zip_name.close()
    shutil.rmtree(rasp.pathdir + '/temp')

#################################################################
#                            GIFT WRAP                          #
#################################################################
def giftwrap(pathdir):
    os.chdir(pathdir.strip('deliverables'))
    zip_name = zipfile.ZipFile('final_package_' + time.strftime('%d-%m-%Y_%H-%M-%S') + '.zip', 'w', zipfile.ZIP_DEFLATED)
    dirlist = os.listdir(pathdir)
    for list in dirlist:
        get_file = os.path.join(pathdir, list)
        zip_name.write(get_file, list)

    zip_name.close()
    shutil.rmtree(pathdir)

#################################################################
#                               RUN                             #
#################################################################
def run(rasp):
    print 'Working...'
    os.mkdir(rasp.pathdir + '/temp', 0700)
    os.chdir(rasp.pathdir + '/temp')
    openfile('dpkg.log', None)
    openfile('auth.log', None)
    openfile('kern.log', None)
    openfile('syslog', None)
    openfile('apt-hist.log', None)
    openfile('bashhist.log', rasp)
    cleanup(rasp)
    print 'Done..'

#################################################################
#                        SIGNAL HANDLER                         #
#################################################################
def signal_handler(signal, frame):
    pathdir = '/root/siem9/deliverables' 

    if pathdir.split('/')[-1:] == 'deliverables':
        os.chdir(pathdir.split('/')[-1:])
        execute(0, None)
    else:
        giftwrap(pathdir)

    exit()

#################################################################
#                            EXECUTE                            #
#################################################################
def execute(idle, q, user):

    signal.signal(signal.SIGTERM, signal_handler)

    rasp = globs(user)
    rasp.pathdir = '/root/siem9/deliverables'

    if os.path.exists(rasp.pathdir) != True:
        os.makedirs(rasp.pathdir, 0700)

    if idle == 1:
        run(rasp)
        timer = 0
        while q.empty() == True:
            time.sleep(1)
            timer += 1
            if timer == 300:
                timer = 0
                rasp.package += 1
                run(rasp)

        giftwrap(rasp.pathdir)
    else:
        run(rasp)
        giftwrap(rasp.pathdir)
