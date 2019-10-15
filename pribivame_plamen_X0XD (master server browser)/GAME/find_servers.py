#v0
import pygame
import settings
import socket
import os
import server_browser
from threading import Thread

pygame.init()

green = (0,255,0)
font = pygame.font.Font(None, 30)
def msg(scr, x, y, text):
    text = font.render(text, 1, green)
    scr.blit(text, (x, y))

prind_msg = []
def prind(text):
    prind_msg.append(text)
    if len(prind_msg) > 15:
        del prind_msg[0]
def prind_clear():
    global prind_msg
    prind_msg = []

def connect_thread():
    global servers
    global done
    try:
        f = open('servers.txt','r')
    except FileNotFoundError:
        with open('servers.txt','w') as f:
            f.write('78.90.45.230:27015\n')
            f.close()
        servers = ['78.90.45.230:27015']
    else:
        servers = []
        while True:
            l = f.readline()
            if len(l) == 0:break
            if l[-1] == '\n':
                l = l[:-1]
                if len(l) == 0:break
            servers.append(l)
    master_ip = settings.get_master_server_ip()
    master_port = settings.get_master_server_port()
    s = socket.socket()
    prind('Connecting to master server:')
    prind('    "%s:%s"'%(master_ip,master_port))
    try:
        s.connect((master_ip,master_port))
    except ConnectionRefusedError:
        prind('Connection refused')
    except TimeoutError:
        printd('Connetion Timeout')
    else:
        prind('Connected to server')
        prind('Reciving server data')
        data = b''
        while True:
            try:
                frame = s.recv(1)
            except ConnectionResetError:
                break
            if frame == b';':
                d = data.decode()
                data = b''
                if d not in servers:
                    f = open('servers.txt','a')
                    f.write(d);f.write('\n')
                    f.close()
                    servers.append(d)
            else:
                data += frame
    prind('Servers found: %s'%(len(servers)))
    done = True

done = False
def main(scr):
    prind('Loading...')
    Thread(target=connect_thread).start()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return 0


        scr.fill((0,0,0))

        y = 0
        for text in prind_msg:
            msg(scr,0,y,text)
            y += 30
        
        pygame.display.update()

        if done:
            return servers


if __name__ == '__main__':
    import main_menu
    main_menu.main()
