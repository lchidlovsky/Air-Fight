import pygame

def main():
    pygame.init()
    
    screen = pygame.display.set_mode()
    SCREEN_HEIGHT, SCREEN_WIDTH = screen.get_size()
    screen = pygame.display.set_mode((int(SCREEN_HEIGHT*0.8), int(SCREEN_WIDTH*0.8)))
    pygame.display.set_caption("Air Fight")
    
    clock = pygame.time.Clock()
    FPS = 60
    
    
    jeu_lance = True
    while jeu_lance:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jeu_lance = False
                
                
                
                
    
    print("Merci d'avoir joué !")
    pygame.quit()
    
    
    
    
    
    
    
if __name__ == '__main__':
    main()
