import pygame

pygame.init()

green = (0,255,0)

font = pygame.font.Font(None, 30)
def text(x, y, txt):
    text = font.render(txt, 1, green)
    scr.blit(text, (x, y))

def main(loc_scr):
    global scr
    scr = loc_scr;del loc_scr
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return 0
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_0:
                    return 0

        

        
        scr.fill((0,0,0))
        text(0,0,'Ako iskash da smenish neshto otivash v papka settings')
        text(0,60,'Ako ima problemche si pogovori s developera')
        text(0,90,'Natishi 0 za da se vurnesh')
        pygame.display.update()

if __name__ == '__main__':
    import main_menu
    main_menu.main()
