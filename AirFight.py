import sys
import pygame
from pygame.locals import *

sys.path.insert(0, "./src/")
from src import *


def gestion_controles():
    """fonction gérant les actions du joueur
    """
    global utilisation_clavier
    global manette
    global conf_bouttons
    global haut_enclenche, bas_enclenche, gauche_enclenche, droite_enclenche
    global a_presse
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                visible.continu = False
        
        if event.type == pygame.JOYDEVICEADDED:     #si une manette est branchée
            pygame.joystick.init()
            manette = pygame.joystick.Joystick(event.device_index)
            utilisation_clavier = False
            haut_enclenche, bas_enclenche, gauche_enclenche, droite_enclenche = False, False, False, False
            a_presse = False
            print("\nPassage en mode manette !\n")
            
        if event.type == pygame.JOYDEVICEREMOVED:   #si la manette est débranchée
            utilisation_clavier = True
            haut_enclenche, bas_enclenche, gauche_enclenche, droite_enclenche = False, False, False, False
            a_presse = False
            print("\nPassage en mode clavier !\n")
        
        if utilisation_clavier:     #si le joueur utilise le clavier
        
            if event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    haut_enclenche = True
                if event.key == K_DOWN:
                    bas_enclenche = True
                if event.key == K_LEFT:
                    gauche_enclenche = True
                if event.key == K_RIGHT:
                    droite_enclenche = True
                if event.key == K_SPACE:
                    a_presse = True
                if isinstance(visible, SessionJeu):
                    if event.key == K_RETURN:
                        visible.b_presse()
                
                    
            if event.type == pygame.KEYUP:
                if event.key == K_UP:
                    haut_enclenche = False
                if event.key == K_DOWN:
                    bas_enclenche = False
                if event.key == K_LEFT:
                    gauche_enclenche = False
                if event.key == K_RIGHT:
                    droite_enclenche = False
                if event.key == K_SPACE:
                    a_presse = False
                    
        else:       #si le joueur utilise la manette

            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == conf_bouttons['A']:
                    a_presse = True
                if isinstance(visible, SessionJeu):
                    if event.button == conf_bouttons['B']:
                        visible.y_presse()

            if event.type == pygame.JOYBUTTONUP:
                if event.button == conf_bouttons['A']:
                    a_presse = False


            if event.type == pygame.JOYAXISMOTION:      #gestion du joystick gauche de la manette
                if manette.get_axis(1) < - 0.3:
                    haut_enclenche = True
                else:
                    haut_enclenche = False
                if manette.get_axis(1) > 0.3:
                    bas_enclenche = True
                else:
                    bas_enclenche = False
                if manette.get_axis(0) < - 0.3:
                    gauche_enclenche = True
                else:
                    gauche_enclenche = False
                if manette.get_axis(0) > 0.3:
                    droite_enclenche = True
                else:
                    droite_enclenche = False
    
    if a_presse: visible.a_presse()
    if haut_enclenche: visible.haut()
    if bas_enclenche: visible.bas()
    try:
        if gauche_enclenche: visible.gauche()
        if droite_enclenche: visible.droite()
    except:
        pass



#mise en place de la fenêtre de jeu
pygame.init()
screen = pygame.display.set_mode()
SCREEN_HEIGHT = int(screen.get_height() * TAILLE_FENETRE)
SCREEN_WIDTH = int(screen.get_width() * TAILLE_FENETRE)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(nom_du_jeu)

clock = pygame.time.Clock()

#contrôles du joueurs
utilisation_clavier = True
manette = None
conf_bouttons = conf_xbox
manette_xbox = True

#variations des contrôles
haut_enclenche, bas_enclenche, gauche_enclenche, droite_enclenche = False, False, False, False
a_presse = False


visible = MenuAccueil((SCREEN_WIDTH, SCREEN_HEIGHT), manette_xbox)

while visible.continu:
    clock.tick(FPS)
    
    gestion_controles()
    
    visible.update()
    visible.draw(screen)
    
    if isinstance(visible, MenuAccueil) and visible.passage_jeu:
        visible = SessionJeu((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    pygame.display.flip()       #mise à jour de l'affichage


print("Merci d'avoir joué !")
pygame.quit()
