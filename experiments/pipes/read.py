import os
import numpy as np

fin = "./fin"

fout = "./fout"

try:

    os.mkfifo(fin)

    os.mkfifo(fout)

except OSError as e:
    print e.errno
    print e.filename
    print e.strerror

while True:

    rp = open(fout, 'r')   # r+ or rb

    response = rp.read()

    print "vector %s" % response, "\n"

    rp.close()

    print "closed"

    wp = open(fin, 'wb+')

    wp.write(str({np.random.randint(0, 2)}))

    wp.close()

    print "write"