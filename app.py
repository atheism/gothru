#!/usr/bin/env python

import subprocess
import os
import sys
import time

cracker_cmd = '/opt/app-root/src/bin/cracker-server -addr 0.0.0.0:8080 -secret saveme'
gost_cmd = '/opt/app-root/src/bin/gost -L socks://:1080 -L ss://rc4-md5:changeme@:58443'
ss_cmd = '/opt/app-root/src/bin/ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o PasswordAuthentication=no root@fastrouter.f3322.net -p 19860 -R 58443:fastrouter.f3322.net:58443 -CNq'
socks_cmd = '/opt/app-root/src/bin/ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o PasswordAuthentication=no root@fastrouter.f3322.net -p 19860 -R 1080:fastrouter.f3322.net:1080 -CNq'

## logs ##
cracker_f = open("/opt/app-root/src/logs/cracker-server.log", "aw+")
gost_f = open("/opt/app-root/src/logs/gost.log", "aw+")
ss_f = open("/opt/app-root/src/logs/ss.log", "aw+")
socks_f = open("/opt/app-root/src/logs/socks.log", "aw+")

## run them ##
cracker = subprocess.Popen(cracker_cmd, shell=True, stderr=cracker_f, stdout=cracker_f)
gost = subprocess.Popen(gost_cmd, shell=True, stderr=gost_f, stdout=gost_f)
ss = subprocess.Popen(ss_cmd, shell=True, stderr=ss_f, stdout=ss_f)
socks = subprocess.Popen(socks_cmd, shell=True, stderr=socks_f, stdout=socks_f)
 
while True:
    if ss.poll() != None:
        ss = subprocess.Popen(ss_cmd, shell=True, stderr=ss_f, stdout=ss_f)
    if socks.poll() != None:
        socks = subprocess.Popen(socks_cmd, shell=True, stderr=socks_f, stdout=socks_f)
    time.sleep(10)
