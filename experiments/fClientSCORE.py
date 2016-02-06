import socket
import time

i = 0

sock = socket.socket()

sock.connect(('127.0.0.1', 50007))

# sock.setblocking(0)

while True:
    time.sleep(1)
    sock.send(str([1, 1, 1, i]))
    data = sock.recv(1024)
    if not data:
        break
    print data, i
    i += 1

sock.close()


