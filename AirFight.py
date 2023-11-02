import sys
import pygame
from pygame.locals import *

sys.path.insert(0, "./src/")
from src import *


def gestion_controls():
    global jeu_lance
    global vaisseau
    global utilisation_clavier
    global manette
    global conf_bouttons
    global dep_haut, dep_bas, dep_gauche, dep_droit
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                jeu_lance = False
        
        if event.type == pygame.JOYDEVICEADDED:
            pygame.joystick.init()
            manette = pygame.joystick.Joystick(event.device_index)
            utilisation_clavier = False
            dep_haut, dep_bas, dep_gauche, dep_droit = False, False, False, False
            print("\nPassage en mode manette !\n")
            
        if event.type == pygame.JOYDEVICEREMOVED:
            utilisation_clavier = True
            dep_haut, dep_bas, dep_gauche, dep_droit = False, False, False, False
            print("\nPassage en mode clavier !\n")
        
        if utilisation_clavier:     #si le joueur utilise le clavier
        
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
                    
        else:       #si le joueur utilise la manette

            for nom, num in conf_bouttons.items():
                if manette.get_button(num):
                    print("Bouton", nom, "pressé !")
                    
                    if nom == 'A':
                        print("Aaaaaaaaahh !!")
                    
            #gestion du joystick gauche de la manette
            if manette.get_axis(1) < - 0.2:
                dep_haut = True
            else:
                dep_haut = False
            if manette.get_axis(1) > 0.2:
                dep_bas = True
            else:
                dep_bas = False
            if manette.get_axis(0) < - 0.2:
                dep_gauche = True
            else:
                dep_gauche = False
            if manette.get_axis(0) > 0.2:
                dep_droit = True
            else:
                dep_droit = False
                         
    if dep_haut: vaisseau.haut(vitesse_joueur)
    if dep_bas: vaisseau.bas(vitesse_joueur)
    if dep_gauche: vaisseau.gauche(vitesse_joueur)
    if dep_droit: vaisseau.droite(vitesse_joueur)



#mise en place de la fenêtre de jeu
pygame.init()
screen = pygame.display.set_mode()
SCREEN_HEIGHT = int(screen.get_height() * 0.8)
SCREEN_WIDTH = int(screen.get_width() * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
print("height =", SCREEN_HEIGHT)
print("width =", SCREEN_WIDTH)
pygame.display.set_caption(nom_du_jeu)

clock = pygame.time.Clock()


#création du vaisseau du joueur
apparences_vaisseau = []
for i in range(1, 7):
    apparences_vaisseau.append(pygame.image.load(f"images/joueur/joueur_{i}.png").convert_alpha())
vaisseau = Joueur(apparences_vaisseau, 200, 10, SCREEN_WIDTH, SCREEN_HEIGHT)
print("len", len(apparences_vaisseau))

#contrôles du joueurs
utilisation_clavier = True
manette = None
conf_bouttons = conf_ps

#variable de déplacement du vaisseau
dep_haut, dep_bas, dep_gauche, dep_droit = False, False, False, False

jeu_lance = True
while jeu_lance:
    clock.tick(FPS)
    
    gestion_controls()
    
    
    screen.fill((200, 200, 200))
    
    vaisseau.tick()
    
    screen.blit(vaisseau.visuel(), vaisseau.coordonnees())

    
    pygame.display.flip()
            

print("Merci d'avoir joué !")
pygame.quit()
