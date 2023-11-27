import pygame
from constantes import *


class Bouton:
    """classe représentant le bouton d'un menu
    """
    
    def __init__(self, message, coord_visible, coord_cache):
        self.longueur = 240
        self.largeur = 110
        self.vitesse_deplacement = 2
        
        self.coord_cache = [
            coord_cache[0] - coord_cache[0] % self.vitesse_deplacement - self.longueur //2,
            coord_cache[1] - coord_cache[1] % self.vitesse_deplacement - self.largeur //2]
        self.coord_visible = [
            coord_visible[0] - coord_visible[0] % self.vitesse_deplacement - self.longueur //2,
            coord_visible[1] - coord_visible[1] % self.vitesse_deplacement - self.largeur //2]
        self.topleft = self.coord_cache
        
        self.message = message
        self.horloge_message = 0
        self.grossir_message = False
        self.taille_message = 25
        
        self.selectionne = False
        self.visible = False
    
    def transition(self):
        self.visible = not self.visible
        if not self.visible : self.selectionne = False
        
    def en_place(self):
        return self.topleft == (self.coord_visible if self.visible else self.coord_cache)
    
    def update(self):
        #gestion de la taille du message
        if self.selectionne:
            self.horloge_message += 1
            if self.grossir_message:    #si le message doit grossir
                self.taille_message += self.horloge_message // self.horloge_message
            else:                       #si le message doit rétrécir
                self.taille_message -= self.horloge_message // self.horloge_message
            if self.horloge_message == 20:
                self.horloge_message = 0
        else:
            self.taille_message = 25

        #gestion du déplacement du bouton
        destination = (self.coord_visible if self.visible else self.coord_cache)
        if self.topleft != destination:
            #cas du déplacement vers haut
            if self.topleft[1] > destination[1]:
                self.topleft[1] -= self.vitesse_deplacement
            #cas du déplacement vers le bas
            if self.topleft[1] < destination[1]:
                self.topleft[1] += self.vitesse_deplacement
            #cas du déplacement vers la gauche
            if self.topleft[0] > destination[0]:
                self.topleft[0] -= self.vitesse_deplacement
            #cas du déplacement vers la droite
            if self.topleft[0] < destination[0]:
                self.topleft[0] += self.vitesse_deplacement
    
    def draw(self, surface):
        #affichage du message
        font = pygame.font.Font(pygame.font.match_font(POLICE), self.taille_message)
        message = font.render(self.message, True, "WHITE")
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
            Bouton((0, 0), "JOUER", (self.longueur_max //2, self.hauteur_max //2), (self.longueur_max //2, self.hauteur_max +50)),
            Bouton((0, 0), "OPTIONS", (self.longueur_max //2, self.hauteur_max //2 +50), (self.longueur_max //2, self.hauteur_max +90)),
            Bouton((0, 0), "QUITTER", (self.longueur_max //2, self.hauteur_max //2 +100), (self.longueur_max //2, self.hauteur_max +130)),
            Bouton((0, 0), "MUSIQUE : OUI", (int(self.longueur_max * 0.75), self.hauteur_max-100), (self.longueur_max +50, self.hauteur_max-100)),
            Bouton((0, 0), "MENU", (int(self.longueur_max * 0.75), self.hauteur_max+100), (self.longueur_max +50, self.hauteur_max+100))
        ]
        self.boutons_entrants = []
        self.boutons_sortants = []
        
        self.page = 0
        self.transition_en_cours = False
        
    def transition_menu(self):
        if not self.transition_en_cours:
            self.page = 0
            self.transition_en_cours = True
            
            #on fait transitionner tous les boutons déjà présents
            for b in self.boutons_entrants:
                self.boutons[b].transition()
                self.boutons_sortants.append(b)
            
            #on insère les trois boutons présents dans le menu principal
            for i in range(3):
                self.boutons[i].transition()
                self.boutons_entrants.append(i)
                
            self.boutons_entrants = self.boutons_entrants[-3:]

    def transition_jouer(self):
        if not self.transition_en_cours:
            self.page = 1
            self.transition_en_cours = True
        
    def transition_options(self):
        if not self.transition_en_cours:
            self.page = 2
            self.transition_en_cours = True
            
            #on fait transitionner tous les boutons déjà présents
            for b in self.boutons_entrants:
                self.boutons[b].transition()
                self.boutons_sortants.append(b)
            
            #on insère les trois boutons présents dans le menu principal
            for i in range(3, 5):
                self.boutons[i].transition()
                self.boutons_entrants.append(i)
                
            self.boutons_entrants = self.boutons_entrants[-2:]
    
    def transition_quitter(self):
        if not self.transition_en_cours:
            self.page = 3
            self.transition_en_cours = True
            
            #on fait transitionner tous les boutons déjà présents
            for b in self.boutons_entrants:
                self.boutons[b].transition()
                self.boutons_sortants.append(b)
            self.boutons_entrants.clear()
        
    def update(self):
        for b in self.boutons_sortants + self.boutons_entrants:
            self.boutons[b].update()
        
        #on fait diparaitre tous les boutons venant de sortir de l'écran
        if self.transition_en_cours:
            disparition = True
            for b in self.boutons_sortants + self.boutons_entrants:
                if not self.boutons[b].en_place():
                    disparition = False
                    break
            if disparition:
                self.boutons_sortants.clear()
                self.transition_en_cours = False
    
    def draw(self, surface):
        surface.blit(self, (0, 0))
        
        for b in self.boutons_sortants + self.boutons_entrants:
            self.boutons[b].draw(surface)