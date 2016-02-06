'''
To use the external commands
First run script for run
'''

import os
import numpy as np
import time

fin = "./fin"

fout = "./fout"

print os.path.exists(fout)
'''
if os.path.exists("fout"):
    os.unlink(fout)
    os.unlink(fin)
'''
print os.path.exists(fout)

try:

    os.mkfifo(fin)

    os.mkfifo(fout)

except OSError as e:
    print e.errno
    print e.filename
    print e.strerror

i = 0
while True:
    time.sleep(0.5)   # 1/90
    i += 1
    # print "go"

    wp = open(fout, 'wb+')

    wp.write(str([i, 0, 0, np.random.randint(0, 2)]))

    wp.close()

    print "closed"
    '''
    rp = open(fin, 'rb+')   # r+ or rb

    print rp

    try:
        response = rp.read()
    finally:
        response = ""

    print response

    rp.close()
    '''

'''
from subprocess import *
import os

FIFO_PATH = '/tmp/my_fifo'

if os.path.exists(FIFO_PATH):
    os.unlink(FIFO_PATH)

if not os.path.exists(FIFO_PATH):
    os.mkfifo(FIFO_PATH)
    my_fifo = open(FIFO_PATH, 'w+')
    print "my_fifo:", my_fifo

print open(FIFO_PATH, 'r').readline()

os.unlink(FIFO_PATH)
'''