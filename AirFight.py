import sys
import pygame
from pygame.locals import *

sys.path.insert(0, "./src/")
from src import *


def gestion_controles():
    """fonction gérant les actions du joueur
    """
    global jeu_lance
    global vaisseau
    global balles
    global utilisation_clavier
    global manette
    global conf_bouttons
    global dep_haut, dep_bas, dep_gauche, dep_droit
    global tirer
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                jeu_lance = False
        
        if event.type == pygame.JOYDEVICEADDED:     #si une manette est branchée
            pygame.joystick.init()
            manette = pygame.joystick.Joystick(event.device_index)
            utilisation_clavier = False
            dep_haut, dep_bas, dep_gauche, dep_droit = False, False, False, False
            print("\nPassage en mode manette !\n")
            
        if event.type == pygame.JOYDEVICEREMOVED:   #si la manette est débranchée
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
                if event.key == K_SPACE:
                    tirer = True
                    
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

            for nom, num in conf_bouttons.items():
                if manette.get_button(num):
                    print("Bouton", nom, "pressé !")
                    
                    if nom == 'A':
                        tirer = True
            
            if event.type == pygame.JOYBUTTONUP:
                if event.button == conf_bouttons['A']:
                    tirer = False
                    
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
    if tirer:
        for coord in vaisseau.tirer():
            balles.add(Projectile(pygame.image.load(f"images/autres/projectile_1.png").convert_alpha(), coord))

def gestion_projectiles():
    """fonction animant les projectiles visibles
    """
    global balles
    
    for proj in balles:
        proj.haut(vitesse_projectile)
    
        if proj.rect.bottom < 0:
            balles.remove(proj)

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

#création du vaisseau du joueur
apparences_vaisseau = []
for i in range(1, 7):
    apparences_vaisseau.append(pygame.image.load(f"images/joueur/joueur_{i}.png").convert_alpha())
vaisseau = Joueur(apparences_vaisseau, (SCREEN_WIDTH //2, SCREEN_HEIGHT //2), SCREEN_WIDTH, SCREEN_HEIGHT)

#création du groupe contenant les projectiles
balles = pygame.sprite.Group()

#variable d'action du vaisseau
dep_haut, dep_bas, dep_gauche, dep_droit = False, False, False, False
tirer = False

jeu_lance = True
while jeu_lance:
    clock.tick(FPS)
    
    gestion_controles()
    
    gestion_projectiles()
    
    screen.fill((200, 200, 200))
    
    vaisseau.tick()
    
    balles.draw(screen)
    screen.blit(vaisseau.image, vaisseau.coordonnees())

    
    pygame.display.flip()       #mise à jour de l'affichage
            

print("Merci d'avoir joué !")
pygame.quit()
