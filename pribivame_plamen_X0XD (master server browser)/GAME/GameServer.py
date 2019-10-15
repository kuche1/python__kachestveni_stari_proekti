import settings
import socket
import time
from threading import Thread

print('Binding...')
s1 = socket.socket()
s1.bind(('',settings.get_dedicated_server_port()))
s1.listen(1)

s2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s2.bind(('',settings.get_dedicated_server_port()+1))

print('Connecting to master server')
try:
    raise ConnectionRefusedError
    s1.connect((settings.get_master_server_ip(),settings.get_master_server_port()))
except ConnectionRefusedError:
    print('ERROR: Could not connect to the master server')
else:
    print('Sending data to master server')
    s1.sendall(b'1')
    try:
        s1.recv(1)
    except ConnectionResetError:
        pass
    print('Data sent')

def redirects1Info():
    global cons
    global addrs
    while True:
        for con in cons:
            try:
                data = con.recv(1024)
            except BlockingIOError:
                continue
            except ConnectionResetError:
                ind = cons.index(con)
                del cons[ind]
                del addrs[ind]
                print('User disconnected')
            for con2 in cons:
                if con2!=con:
                    con2.sendall(data)

def redirects2Info():
    while True:
        data,addr = s2.recv(1024)
        ip = addr[0]
        for addr in addrs:
            if ip != addr:
                s2.sendto(addr,data)



print('Starting server')
cons = []
addrs = []
Thread(target=redirects1Info).start()
Thread(target=redirects2Info).start()
while True:
    con,addr = s1.accept()
    data = con.recv(1)
    if data==b'':
        print(addr,'checked to see if online')
        continue
    else:
        print(addr,'connected')
        con.setblocking(False)
        cons.append(con)
        addrs.append(addr[0])

    
