#!/usr/bin/env python

import subprocess
import os
import sys
import time

path = os.getcwd()

chisel_cmd = path + '/bin/chisel server --port 8080 --socks5'
cracker_cmd = path + '/bin/cracker-server -addr 0.0.0.0:18080 -secret saveme'
ssserver_cmd = 'ssserver -p 58443 -k changeme -m rc4-md5'
gost_cmd = path + '/bin/gost -L socks://:1080 -L ss://rc4-md5:changeme@:50443'

## logs ##
chisel_f = open(path + "/logs/chisel-server.log", "a+")
cracker_f = open(path + "/logs/cracker-server.log", "a+")
ssserver_f = open(path + "/logs/ssserver.log", "a+")
gost_f = open(path + "/logs/gost.log", "a+")

## run them ##
chisel = subprocess.Popen(chisel_cmd.split(), stderr=chisel_f, stdout=chisel_f)
cracker = subprocess.Popen(cracker_cmd.split(), stderr=cracker_f, stdout=cracker_f)
ssserver = subprocess.Popen(ssserver_cmd.split(), stderr=ssserver_f, stdout=ssserver_f)
gost = subprocess.Popen(gost_cmd.split(), stderr=gost_f, stdout=gost_f)

reload = True
 
while True:
    cracker_f.flush()
    gost_f.flush()
    if reload == True and os.path.isfile(path + '/.ssh/passwd') :
        password = open(path + "/.ssh/passwd", "r").read().strip()
        gost_cmd = path + '/bin/gost -L socks://:1080 -L ss://rc4-md5:%s@:50443' % password
        ssserver_cmd = 'ssserver -p 58443 -k %s -m rc4-md5' % password
        gost.kill()
        ssserver.kill()
        gost = subprocess.Popen(gost_cmd.split(), stderr=gost_f, stdout=gost_f)
        ssserver = subprocess.Popen(ssserver_cmd.split(), stderr=ssserver_f, stdout=ssserver_f)
        reload = False
    time.sleep(10)
