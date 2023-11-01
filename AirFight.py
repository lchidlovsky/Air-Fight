import sys
import pygame
from pygame.locals import *

sys.path.insert(0, "./src/")
from src import *



def gestion_controls(event):
    global jeu_lance
    global dep_haut, dep_bas, dep_gauche, dep_droit
    
    if event.type == pygame.QUIT:
            jeu_lance = False
        
    if event.type == pygame.KEYDOWN:
        if event.key == K_UP:
            dep_haut = True
        if event.key == K_DOWN:
            dep_bas = True
        if event.key == K_LEFT:
            dep_gauche = True
        if event.key == K_RIGHT:
            dep_droit = True
            
    if event.type == pygame.KEYUP:
        if event.key == K_UP:
            dep_haut = False
        if event.key == K_DOWN:
            dep_bas = False
        if event.key == K_LEFT:
            dep_gauche = False
        if event.key == K_RIGHT:
            dep_droit = False


#mise en place de la fenêtre de jeu
pygame.init()
screen = pygame.display.set_mode()
SCREEN_HEIGHT, SCREEN_WIDTH = screen.get_size()
SCREEN_HEIGHT = int(SCREEN_HEIGHT * 0.8)
SCREEN_WIDTH = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
pygame.display.set_caption(nom_du_jeu)

clock = pygame.time.Clock()


#création du vaisseau du joueur
apparences_vaisseau = []
for i in range(1, 7):
    apparences_vaisseau.append(pygame.image.load(f"images/joueur/joueur_{i}.png").convert_alpha())
vaisseau = Joueur(apparences_vaisseau, 200, 10, SCREEN_HEIGHT, SCREEN_WIDTH)

#variable de déplacement du vaisseau
dep_haut, dep_bas, dep_gauche, dep_droit = False, False, False, False

jeu_lance = True
while jeu_lance:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        gestion_controls(event)
            
    if dep_haut: vaisseau.haut(vitesse_joueur)
    if dep_bas: vaisseau.bas(vitesse_joueur)
    if dep_gauche: vaisseau.gauche(vitesse_joueur)
    if dep_droit: vaisseau.droite(vitesse_joueur)
    
    
    screen.fill((200, 200, 200))
    
    screen.blit(vaisseau.visuel(), vaisseau.coordonnees())

    
    pygame.display.flip()
            

print("Merci d'avoir joué !")
pygame.quit()
