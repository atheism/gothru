#!/usr/bin/env python

import subprocess
import os
import sys
import time

if __name__ == '__main__':
    path = os.getcwd()

    port = os.environ['PORT']
    password = os.environ['SECRET']

    cracker_cmd = path + '/bin/cracker-server -addr 0.0.0.0:' + port + ' -secret ' + password
    ssserver_cmd = 'ssserver -p 58443 -k ' + password + ' -m rc4-md5'

    ## logs ##
    cracker_f = open(path + "/logs/cracker-server.log", "a+")
    ssserver_f = open(path + "/logs/ssserver.log", "a+")

    ## run them ##
    cracker = subprocess.Popen(cracker_cmd.split(), stderr=cracker_f, stdout=cracker_f)
    ssserver = subprocess.Popen(ssserver_cmd.split(), stderr=ssserver_f, stdout=ssserver_f)


    loop = 0
    while True:
        print("keep alive")
        time.sleep(15)
        loop = loop + 1
