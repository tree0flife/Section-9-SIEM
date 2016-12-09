#!/usr/bin/python

############################################################
#                           NOTE:                          #
#                 Need to filter only IP's                 #
############################################################

import os
import time
import signal
import subprocess as sub

class pcapkiller:

    def call(self, name, num):
        name = name + time.strftime('_%d-%m-%Y_%H-%M-%S') + '_' + str(num) + '.pcap'
        p = sub.Popen(('tcpdump', '-w', name))
        return p

    def tcpdump(self, name):
        p = self.call(name, 0)
        while True:
            for x in range(0, 120):
                time.sleep(1)
                if x == 110:
                    f = p
                    p = self.call(name, x)
                    time.sleep(10)
                    f.terminate()
                    f.wait()
                    break
    def nucleas(self, p):
        f = p
        p = butter(q)
        f.terminate()
        f.wait()
        o.close()

    def butter(self, q):
        with open('shasta', 'w') as output:
            server = sub.Popen(('tcpdump', '-q', '-n', 'host', '10.16.27.8'), stdout=output)
            while q.empty() == True:
                time.sleep(1)
            server.communicate()
            server.terminate()
            server.wait()
            output.close()
