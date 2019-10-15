import pygame
import time

black = (0,0,0)

pygame.init()

clock = pygame.time.Clock()

def main(scr,s1,s2):
    while True:
        dt = 1/clock.tick()#time between this and last frame in miliseconds (1000ms = 1s)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return 0


        
        scr.fill(black)

        print(dt)

        pygame.display.update()

        

if __name__ == '__main__':
    import main_menu
    main_menu.main()
