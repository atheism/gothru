#!/usr/bin/env python

import subprocess
import os
import sys
import time

chisel_cmd = '/opt/app-root/src/bin/chisel server --port 8080 --socks5'
cracker_cmd = '/opt/app-root/src/bin/cracker-server -addr 0.0.0.0:18080 -secret saveme'
ssserver_cmd = 'ssserver -p 58443 -k changeme -m rc4-md5'
gost_cmd = '/opt/app-root/src/bin/gost -L socks://:1080 -L ss://rc4-md5:changeme@:50443'
ss_cmd = '/opt/app-root/src/bin/ssh -o ServerAliveInterval=15 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o PasswordAuthentication=no root@fastrouter.f3322.net -p 19860 -R 0.0.0.0:58443:0.0.0.0:58443 -CNq'
socks_cmd = '/opt/app-root/src/bin/ssh -o ServerAliveInterval=15 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o PasswordAuthentication=no root@fastrouter.f3322.net -p 19860 -R 0.0.0.0:1080:0.0.0.0:1080 -CNq'

## logs ##
chisel_f = open("/opt/app-root/src/logs/chisel-server.log", "a+")
cracker_f = open("/opt/app-root/src/logs/cracker-server.log", "a+")
ssserver_f = open("/opt/app-root/src/logs/ssserver.log", "a+")
gost_f = open("/opt/app-root/src/logs/gost.log", "a+")
ss_f = open("/opt/app-root/src/logs/ss.log", "a+")
socks_f = open("/opt/app-root/src/logs/socks.log", "a+")

## run them ##
chisel = subprocess.Popen(chisel_cmd.split(), stderr=chisel_f, stdout=chisel_f)
cracker = subprocess.Popen(cracker_cmd.split(), stderr=cracker_f, stdout=cracker_f)
ssserver = subprocess.Popen(ssserver_cmd.split(), stderr=ssserver_f, stdout=ssserver_f)
gost = subprocess.Popen(gost_cmd.split(), stderr=gost_f, stdout=gost_f)
ss = subprocess.Popen(ss_cmd.split(), stderr=ss_f, stdout=ss_f)
socks = subprocess.Popen(socks_cmd.split(), stderr=socks_f, stdout=socks_f)

reload = True
 
while True:
    cracker_f.flush()
    gost_f.flush()
    ss_f.flush()
    socks_f.flush()
    if ss.poll() != None and os.path.isfile('/opt/app-root/src/.ssh/done') :
        ss = subprocess.Popen(ss_cmd.split(), stderr=ss_f, stdout=ss_f)
    if socks.poll() != None and os.path.isfile('/opt/app-root/src/.ssh/done') :
        socks = subprocess.Popen(socks_cmd.split(), stderr=socks_f, stdout=socks_f)
    if reload == True and os.path.isfile('/opt/app-root/src/.ssh/passwd') :
        password = open("/opt/app-root/src/.ssh/passwd", "r").read().strip()
        gost_cmd = '/opt/app-root/src/bin/gost -L socks://:1080 -L ss://rc4-md5:%s@:50443' % password
        ssserver_cmd = 'ssserver -p 58443 -k %s -m rc4-md5' % password
        gost.kill()
        ssserver.kill()
        gost = subprocess.Popen(gost_cmd.split(), stderr=gost_f, stdout=gost_f)
        ssserver = subprocess.Popen(ssserver_cmd.split(), stderr=ssserver_f, stdout=ssserver_f)
        reload = False
    time.sleep(10)
