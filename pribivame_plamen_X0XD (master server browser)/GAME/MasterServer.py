import socket
import time


s = socket.socket()
s.bind(('',26999))
s.listen(1)

addrs = []
while True:
    con,addr = s.accept()

    data = con.recv(1)

    if data == b'0':
        for addr in addrs:
            con.sendall(b'%s:%s;'%(addr[0],addr[1]))
            
    elif data == b'1':
        if addr not in addrs:
            addrs.append(addr)
            

    con.close()
