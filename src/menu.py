import pygame
from constantes import *


class Bouton:
    """classe rassemblant les données d'un bouton
    """
    
    def __init__(self, center, message):
        self.longueur = 240
        self.largeur = 110
        self.vitesse_deplacement = 2
        
        self.topleft = [center[0] - self.longueur //2, center[1] - self.largeur //2]
        self.destination = [0,0]
        
        self.message = message
        self.horloge_message = 0
        self.grossir_message = False
        self.taille_message = 25
        
        self.selectionne = False
    
    def nouvelle_coordonnees(self, x, y):
        """méthode d'assignation de nouvelles coordonnées

        Args:
            x (_type_): _description_
            y (_type_): _description_
        """
        self.topleft = [x - self.longueur //2, y - self.largeur //2]
    
    def nouvelle_destination(self, x, y):
        """méthode d'assignation d'une nouvelle destination atteignable

        Args:
            pos (tuple): couple (x, y) de la nouvelle destination
        """
        self.destination[0] = x - x % self.vitesse_deplacement - self.longueur //2
        self.destination[1] = y - y % self.vitesse_deplacement - self.largeur //2
    
    
    def update(self):
        #gestion de la taille du message
        if self.selected:
            self.horloge_message += 1
            if self.grossir_message:    #si le message doit grossir
                self.taille_message += self.horloge_message // self.horloge_message
            else:                       #si le message doit rétrécir
                self.taille_message -= self.horloge_message // self.horloge_message
            if self.horloge_message == 20:
                self.horloge_message = 0

        #gestion du déplacement du bouton
        if self.topleft != self.destination:
            #cas du déplacement vers haut
            if self.topleft[1] > self.destination[1]:
                self.topleft[1] -= self.vitesse_deplacement
            #cas du déplacement vers le bas
            if self.topleft[1] < self.destination[1]:
                self.topleft[1] += self.vitesse_deplacement
            #cas du déplacement vers la gauche
            if self.topleft[0] > self.destination[0]:
                self.topleft[0] -= self.vitesse_deplacement
            #cas du déplacement vers la droite
            if self.topleft[0] < self.destination[0]:
                self.topleft[0] += self.vitesse_deplacement
                
    def draw(self, surface):
        #affichage du message
        font = pygame.font.Font(pygame.font.match_font(POLICE), self.taille_message)
        message = self.font.render(self.message, True, "WHITE")
        surface.blit(message, (self.topleft[0] + self.longueur - message.get_width() // 2, self.topleft[1] + self.largeur - message.height() // 2))
        
        #affichage du rectangle
        pygame.draw.rect(surface, 'BLACK', pygame.Rect(self.topleft, (self.longueur, self.largeur)), 4, 11)



class MenuAccueil(pygame.Surface):
    """classe représentant le menu principal du jeu
    """
    def __init__(self, size, coord_max):
        pygame.Surface.__init__(self, size)
        self.fill("WHITE")
        
        self.longueur_max = coord_max[0]
        self.hauteur_max = coord_max[1]
        
        self.boutons = [
            Bouton((0, 0), "JOUER"),
            Bouton((0, 0), "OPTIONS"),
            Bouton((0, 0), "QUITTER"),
            Bouton(0, 0), "MENU",
            Bouton((0, 0), "MUSIQUE : OUI")
                        ]
        self.boutons_visibles = set()
        
    def transition_menu(self):
        self.boutons_visibles.add(0)
        self.boutons_visibles.add(1)
        self.boutons_visibles.add(2)
        self.boutons[0].
        self.boutons[0].nouvelle_destination(self.longueur_max //2)
    
    def transition_jouer(self):
        pass
        
    def transition_options(self):
        pass
    
    def transition_quitter(self):
        pass
        
        
    def draw(self, surface):
        surface.blit(self, (0, 0))