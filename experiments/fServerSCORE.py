import socket

i = 0

sock = socket.socket()

sock.bind(('127.0.0.1', 50007))

# sock.setblocking(0)

sock.listen(1)

print "waiting for client"

conn, addr = sock.accept()

print conn, addr

while True:
    try:
        data = conn.recv(1024)
    finally:
        pass
    if not data:
        print "connection closed"
        print "waiting for client"
        conn, addr = sock.accept()
        print conn, addr
        data = conn.recv(1024)
        #break
    print "data from client: ", data, "step", i
    conn.send(str({"info from client": i}))
    i += 1

conn.close()

'''
netstat -ntlp | grep LISTEN
'''

'''
[1, 1, 1, 0]
start core server then start client

socket ('127.0.0.1', 50007)

'''