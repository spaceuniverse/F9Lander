import os
import errno
import numpy as np
import time

fin = "./fin"

fout = "./fout"

try:

    os.mkfifo(fin)

    os.mkfifo(fout)

except OSError as e:
    print e.errno
    print e.filename
    print e.strerror


import errno

def safe_read(fd, size=1024):
   try:
      return os.read(fd, size)
   except OSError, exc:
      if exc.errno == errno.EAGAIN:
         return None
      raise

i = 0
pip = os.open(fin, os.O_RDONLY | os.O_NONBLOCK)
while True:
    time.sleep(0.25)
    i += 1
    print safe_read(pip)
    #data = os.read(new_pipe, 1024)
    #io = os.open(fin, os.O_NONBLOCK)
    '''
    rp = open(fin, 'r')   # r+ or rb

    response = rp.read()

    print "vector %s" % response, "\n"

    rp.close()
    '''
    print i

# http://stackoverflow.com/questions/14345816/how-to-read-named-fifo-non-blockingly
# http://stackoverflow.com/questions/34046083/understanding-named-pipes-fifo-in-python
# http://stackoverflow.com/questions/10021759/what-conditions-result-in-an-opened-nonblocking-named-pipe-fifo-being-unavai
#pipe_1 = os.open(pipe_1_name, os.O_WRONLY)
## os.write(pipe_1, "server_message_0\n")
