import pygame
import sys

sys.path.insert(0, "./src/")
from src import *





jeu_lance = True

def gestion_evenement(event):
    global jeu_lance
    
    if event.type == pygame.QUIT:
        jeu_lance = False


def main():
    global nom_du_jeu
    global FPS
    global jeu_lance
    
    
    pygame.init()
    
    screen = pygame.display.set_mode()
    SCREEN_HEIGHT, SCREEN_WIDTH = screen.get_size()
    SCREEN_HEIGHT = int(SCREEN_HEIGHT * 0.8)
    SCREEN_WIDTH = int(SCREEN_WIDTH * 0.8)
    screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
    pygame.display.set_caption(nom_du_jeu)
    
    clock = pygame.time.Clock()

    while jeu_lance:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            gestion_evenement(event)
        
        
        screen.fill((200, 200, 200))

        
        pygame.display.flip()
                
    
    print("Merci d'avoir joué !")
    pygame.quit()
    
    
    
    
    
    
    
if __name__ == '__main__':
    main()
