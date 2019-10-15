import find_servers
import pygame
import socket
import game_loop

pygame.init()

black = (0,0,0)
green = (0,255,0)

font = pygame.font.Font(None, 30)
def text(x, y, txt):
    text = font.render(txt, 1, green)
    scr.blit(text, (x, y))

def connectAndStart(server):
    s1 = socket.socket()
    s2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    ip,port = server.split(':')
    port = int(port)

    s1.connect((ip,port))
    s1.sendall(b'1')

    game_loop.main(scr,s1,s2)
    s1.close()
    

servers = []
searched_for_servers = False
def main(scr_loc):
    global searched_for_servers
    global servers
    global scr
    scr = scr_loc;del scr_loc
    if not searched_for_servers:
        searched_for_servers = True
        servers = find_servers.main(scr)

    
    

    avail_servs = []
    for serv in servers:
        ip,port = serv.split(':');port = int(port)
        try:
            s1 = socket.socket()
            s1.connect((ip,port))
        except ConnectionRefusedError:
            pass
        else:
            s1.close()
            avail_servs.append(serv)
    del servers;
    servers = avail_servs;del avail_servs


    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return 0

            if e.type == pygame.KEYDOWN:
                if e.key >= 48 and e.key < 55:
                    key = e.key - 48
                    if len(servers)-1 >= key:
                        connectAndStart(servers[key])



        scr.fill(black)

        y = 0
        for ind,ser in enumerate(servers):
            text(0,y,'%s/ %s'%(ind,ser))
            y+=30
        
        pygame.display.update()
            
            
    
        
if __name__ == '__main__':
    import main_menu
    main_menu.main()
