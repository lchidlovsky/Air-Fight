import sys
import pygame
from pygame.locals import *

sys.path.insert(0, "./src/")
from src import *


def gestion_controles():
    """fonction gérant les actions du joueur
    """
    global jeu_lance
    global vaisseau_joueur
    global utilisation_clavier
    global manette
    global conf_bouttons
    global dep_haut, dep_bas, dep_gauche, dep_droit
    global tirer
    global w
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                jeu_lance = False
        
        if event.type == pygame.JOYDEVICEADDED:     #si une manette est branchée
            pygame.joystick.init()
            manette = pygame.joystick.Joystick(event.device_index)
            utilisation_clavier = False
            dep_haut, dep_bas, dep_gauche, dep_droit = False, False, False, False
            tirer = False
            print("\nPassage en mode manette !\n")
            
        if event.type == pygame.JOYDEVICEREMOVED:   #si la manette est débranchée
            utilisation_clavier = True
            dep_haut, dep_bas, dep_gauche, dep_droit = False, False, False, False
            tirer = False
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
                if event.key == K_SPACE:
                    tirer = True

                if event.key == K_RETURN:
                    vaisseau_joueur.explosion_generale()
                
                if event.key == K_BACKSPACE: vaisseau_joueur.amelioration_puissance_feu()
                
                    
            if event.type == pygame.KEYUP:
                if event.key == K_UP:
                    dep_haut = False
                if event.key == K_DOWN:
                    dep_bas = False
                if event.key == K_LEFT:
                    dep_gauche = False
                if event.key == K_RIGHT:
                    dep_droit = False
                if event.key == K_SPACE:
                    tirer = False
                    
        else:       #si le joueur utilise la manette

            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == conf_bouttons['A']:
                    tirer = True
                if event.button == conf_bouttons['Y']:
                    vaisseau_joueur.explosion_generale()

            if event.type == pygame.JOYBUTTONUP:
                if event.button == conf_bouttons['A']:
                    tirer = False
                
                if event.button == conf_bouttons['LB']: vaisseau_joueur.amelioration_puissance_feu()
                if event.button == conf_bouttons['RB']: w = not w


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
                         
    if dep_haut: vaisseau_joueur.haut()
    if dep_bas: vaisseau_joueur.bas()
    if dep_gauche: vaisseau_joueur.gauche()
    if dep_droit: vaisseau_joueur.droite()
    if tirer: vaisseau_joueur.tirer()



#mise en place de la fenêtre de jeu
pygame.init()
screen = pygame.display.set_mode()
SCREEN_HEIGHT = int(screen.get_height() * 0.8)
SCREEN_WIDTH = int(screen.get_width() * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(nom_du_jeu)

clock = pygame.time.Clock()

#contrôles du joueurs
utilisation_clavier = True
manette = None
conf_bouttons = conf_xbox


#variable d'action du vaisseau
dep_haut, dep_bas, dep_gauche, dep_droit = False, False, False, False
tirer = False


#création des entités visuelles
header = gameBar((SCREEN_WIDTH, 60), None)

vaisseau_joueur = Joueur((SCREEN_WIDTH //2, SCREEN_HEIGHT * 0.8), (0, header.get_height()), (SCREEN_WIDTH, SCREEN_HEIGHT), vie_joueur)
header.joueur = vaisseau_joueur
v = Vague("vague de test", coord_min=(0, header.get_height()), coord_max=(SCREEN_WIDTH, SCREEN_HEIGHT),
          joueur=vaisseau_joueur, nb_simultanes=4, nb_petits=6, nb_moyens=3, nb_gros=1,
          nb_coeurs=6, nb_munitions=2, nb_explosifs=3, nb_duplications=2)


w = True

jeu_lance = True
while jeu_lance:
    clock.tick(FPS)
    
    gestion_controles()
    
    screen.fill((222, 222, 222))
    
    
    #mise à jour des entités
    vaisseau_joueur.update()
    if w: v.update()
    
    #affichage des entités
    v.draw(screen)
    vaisseau_joueur.projectiles.draw(screen)
    screen.blit(vaisseau_joueur.image, vaisseau_joueur.rect.topleft)
    header.draw(screen)
    
    
    pygame.display.flip()       #mise à jour de l'affichage
            

print("Merci d'avoir joué !")
pygame.quit()
