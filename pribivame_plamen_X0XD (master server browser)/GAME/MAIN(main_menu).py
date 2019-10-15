#v0

import settings_menu
import settings
import server_browser
import os
import pygame
import random
import copy

pygame.init()

green = (0,255,0)

font = pygame.font.Font(None,30)
def text(scr,x,y,txt):
    txt = font.render(txt,1,green)
    scr.blit(txt,(x,y))

def main():
    #pygame.mixer.Sound('music/Nightcore - Despacito ft. Justin Bieber.wav').play()
    for _,folders,_ in os.walk('music'):
        choosen = random.choice(folders)
        for _,_,files in os.walk('music/%s'%(choosen)):
            files_original = copy.deepcopy(files)
            while True:
                sound_file = random.choice(files)
                if sound_file[-4:] in ['.mp3','.wav']:
                    break
                files.remove(sound_file)
            files = copy.deepcopy(files_original)
            while True:
                image_file = random.choice(files)
                if image_file[-4:] in ['.jpg']:
                    break
                files.remove(image_file)
            background = pygame.image.load('music/%s/%s'%(choosen,image_file))
            pygame.mixer.Sound('music/%s/%s'%(choosen,sound_file)).play()
            break
        break
    
    scrx,scry = settings.get_res_x(),settings.get_res_y()
    if settings.get_fullscreen():
        scr = pygame.display.set_mode((scrx,scry),pygame.FULLSCREEN)
    else:
        scr = pygame.display.set_mode((scrx,scry))

    

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                import sys
                sys.exit(0)
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1:
                    server_browser.main(scr)
                elif e.key == pygame.K_2:
                    settings_menu.main(scr)
                elif e.key == pygame.K_3:
                    pygame.quit()
                    import sys;sys.exit(0)

        cur = pygame.mouse.get_pos()

        scr.fill((0,0,0))

        scr.blit(pygame.transform.scale(background,(scrx,scry)),(0,0))

        text(scr,0,0,'Pribivame Plamen X0XD')
        text(scr,0,60,'1/Play')
        text(scr,0,90,'2/Settings')
        text(scr,0,120,'3/Exit')
        text(scr,0,150,'Samo da si znaesh che hikscheto ne raboti (ako  raboti znachi e bug)')
        
        pygame.display.update()


if __name__ == '__main__':
    main()
