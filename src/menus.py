import pygame
from constantes import *
from bouton import Bouton

class MenuAccueil(pygame.Surface):
    """classe représentant le menu principal du jeu
    """
    def __init__(self, size):
        pygame.Surface.__init__(self, size)
        self.fill("WHITE")
        
        self.longueur_max = size[0]
        self.hauteur_max = size[1]
        
        self.boutons = [
            Bouton("JOUER", (self.longueur_max //2, self.hauteur_max //2), (self.longueur_max //2, self.hauteur_max+40)),
            Bouton("OPTIONS", (self.longueur_max //2, self.hauteur_max //2 +100), (self.longueur_max //2, self.hauteur_max +190)),
            Bouton("QUITTER", (self.longueur_max //2, self.hauteur_max //2 +200), (self.longueur_max //2, self.hauteur_max +340)),
            Bouton("MUSIQUE : OUI", (self.longueur_max //2+280, self.hauteur_max//2-60), (self.longueur_max +150, self.hauteur_max//2-60)),
            Bouton("RETOUR", (self.longueur_max //2+280, self.hauteur_max//2+60), (self.longueur_max +150, self.hauteur_max//2+60))
        ]
        self.boutons_entrants = []
        self.boutons_sortants = []
        
        self.continu = True
        self.passage_jeu = False
        self.curseur = 0
        self.cooldown = 0
        self.page = -1
        self.transition_en_cours = True
        
        self.ecran_noir = pygame.Surface((self.longueur_max, self.hauteur_max))
        self.visibilite = 0
             
    def transition_accueil(self):
        if not self.transition_en_cours:
            self.curseur = 0
            self.page = 0
            self.transition_en_cours = True
            self.visibilite = 255
            
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
            self.curseur = 0
            self.page = 1
            self.transition_en_cours = True
            self.visibilite = 252
            
            #on fait transitionner tous les boutons déjà présents
            for b in self.boutons_entrants:
                self.boutons[b].transition()
                self.boutons_sortants.append(b)
            self.boutons_entrants.clear()
        
    def transition_options(self):
        if not self.transition_en_cours:
            self.curseur = 3
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
            self.curseur = 0
            self.page = 3
            self.transition_en_cours = True
            
            #on fait transitionner tous les boutons déjà présents
            for b in self.boutons_entrants:
                self.boutons[b].transition()
                self.boutons_sortants.append(b)
            self.boutons_entrants.clear()
            
    def haut(self):
        if not self.transition_en_cours and self.cooldown == 0:
            self.cooldown = 1
            limite = 0
            
            match self.page:
                case 0:
                    limite = 0
                
                case 2:
                    limite = 3
                    
            if self.curseur-1 >= limite:
                self.boutons[self.curseur].selectionne = False
                self.curseur -= 1
                self.boutons[self.curseur].selectionne = True
    
    def bas(self):
        if not self.transition_en_cours and self.cooldown == 0:
            self.cooldown = 1
            limite = 0
            
            match self.page:
                case 0:
                    limite = 2
                case 2:
                    limite = 4
            if self.curseur+1 <= limite:
                self.boutons[self.curseur].selectionne = False
                self.curseur += 1
                self.boutons[self.curseur].selectionne = True
                        
    def selection(self):
        if not self.transition_en_cours:
            match self.curseur:
                case 0:
                    self.transition_jouer()
                case 1:
                    self.transition_options()
                case 2:
                    self.transition_quitter()
                case 3:
                    #activer/désactiver le son
                    print("fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
                case 4:
                    self.transition_accueil()
               
    def update(self):
        #effet d'apparition en fondu
        if self.page == -1:
            if self.visibilite < 255:
                self.visibilite += 3
            else:
                self.transition_en_cours = False
                self.transition_accueil()
                
        if self.visibilite == 0:
            self.passage_jeu = True
            
        else:
            if self.cooldown: self.cooldown += 1
            if self.cooldown > 18 : self.cooldown = 0
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
                    if self.boutons_entrants: self.boutons[self.boutons_entrants[0]].selectionne = True
                    if self.page == 3: self.continu = False
            else:
                if self.page == 1 and 2 < self.visibilite < 255:
                    self.visibilite -= 3
        
    def draw(self, surface):
        surface.blit(self, (0, 0))
        
        for b in self.boutons_sortants + self.boutons_entrants:
            self.boutons[b].draw(surface)

        self.ecran_noir.set_alpha(255-self.visibilite)
        surface.blit(self.ecran_noir, (0, 0))
