#!/usr/bin/env python

import subprocess
import os

cmd = os.getcwd() + '/cracker-server -addr 0.0.0.0:8080 -secret saveme'

## run it ##
p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
 
## But do not wait till netstat finish, start displaying output immediately ##
while True:
    out = p.stderr.read(1)
    if out == '' and p.poll() != None:
        break
    if out != '':
        sys.stdout.write(out)
        sys.stdout.flush()
