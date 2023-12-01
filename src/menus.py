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
        
        titre = pygame.image.load("images/autres/air-fight.png").convert_alpha()
        self.titre = pygame.transform.scale(titre, (720, 135))
        self.titre.set_alpha(0)
        
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
        self.ecran_noir.set_alpha(255)
             
    def transition_accueil(self):
        if not self.transition_en_cours:
            self.curseur = 0
            self.page = 0
            self.transition_en_cours = True
            self.titre.set_alpha(5)
            
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
            self.ecran_noir.set_alpha(3)
            self.titre.set_alpha(240)
            
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
                        
    def a_presse(self):
        if not self.transition_en_cours and self.page in [0, 2]:
            match self.curseur:
                case 0:
                    self.transition_jouer()
                case 1:
                    self.transition_options()
                case 2:
                    self.transition_quitter()
                case 3:
                    #activer/désactiver le son
                    pass
                case 4:
                    self.transition_accueil()
               
    def update(self):
        
        #effet d'apparition en fondu
        if self.page == -1:
            if (self.ecran_noir.get_alpha() if self.ecran_noir.get_alpha() else 0) > 1:
                self.ecran_noir.set_alpha((self.ecran_noir.get_alpha() if self.ecran_noir.get_alpha() else 0) - 3)
            else:
                self.transition_en_cours = False
                self.transition_accueil()
        
        if (self.ecran_noir.get_alpha() if self.ecran_noir.get_alpha() else 0) > 254:
            self.passage_jeu = True
        
        if self.cooldown: self.cooldown += 1
        if self.cooldown > 18 : self.cooldown = 0
        for b in self.boutons_sortants + self.boutons_entrants:
            self.boutons[b].update()
        
        if self.transition_en_cours:
            #on fait diparaitre tous les boutons venant de sortir de l'écran
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
                
            #on fait apparaitre/disparaitre le titre du jeu
            if self.page == 0 and (self.titre.get_alpha() if self.titre.get_alpha() else 0) < 255:
                self.titre.set_alpha((self.titre.get_alpha() if self.titre.get_alpha() else 0) + 5)
            if self.page != 0 and (self.titre.get_alpha() if self.titre.get_alpha() else 0) > 0:
                self.titre.set_alpha((self.titre.get_alpha() if self.titre.get_alpha() else 0) - 5)
        else:
            if self.page == 1 and 2 < (self.ecran_noir.get_alpha() if self.ecran_noir.get_alpha() else 0):
                self.ecran_noir.set_alpha((self.ecran_noir.get_alpha() if self.ecran_noir.get_alpha() else 0)+3)
        
    def draw(self, surface):
        surface.blit(self, (0, 0))
        surface.blit(self.titre, (self.longueur_max//2 - self.titre.get_width()//2, self.hauteur_max //2 -250- self.titre.get_height()//2))
        
        for b in self.boutons_sortants + self.boutons_entrants:
            self.boutons[b].draw(surface)
        
        surface.blit(self.ecran_noir, (0, 0))
