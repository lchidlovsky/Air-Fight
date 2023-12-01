import pygame
from constantes import *
from vague import Vague
from menus import Bouton
from joueur import Joueur
from gamebar import gameBar

class SessionJeu(pygame.Surface):
    """classe représentant une session de jeu
    """
    
    def __init__(self, size):
        pygame.Surface.__init__(self, size)
        self.fill("WHITE")
    
        self.longueur_max = size[0]
        self.hauteur_max = size[1]
        
        
        self.header = gameBar((self.longueur_max, 60), None)
        self.joueur = Joueur((self.longueur_max //2, self.hauteur_max * 0.8),
                             (0, self.header.get_height()), (self.longueur_max, self.hauteur_max), vie_joueur)
        self.header.joueur = self.joueur
        
        self.nb_petits = 5
        self.nb_moyens = 2
        self.nb_gros = 0
        self.visibles = 5
        self.num_vague = 1
        self.nb_coeurs = 3
        self.nb_munitions = 2
        self.nb_explosifs = 0
        self.nb_feux = 0
        self.nb_vitesses = 0
        self.vague = Vague("vague n°"+str(self.num_vague),
                        coord_min=(0, self.header.get_height()), coord_max=(self.longueur_max, self.hauteur_max),
                        joueur=self.joueur, nb_simultanes=self.visibles,
                        nb_petits=self.nb_petits, nb_moyens=self.nb_moyens, nb_gros=self.nb_gros,
                        nb_coeurs=self.nb_coeurs, nb_munitions=self.nb_munitions, nb_explosifs=self.nb_explosifs,
                        nb_vitesses=self.nb_vitesses, nb_feux=self.nb_feux)
         
        self.boutons = []
        #    Bouton("REPRENDRE", (self.longueur_max //2, self.hauteur_max //2), (self.longueur_max //2, self.hauteur_max+40)),
        #    Bouton("MUSIQUE : OUI", (self.longueur_max //2, self.hauteur_max //2 +100), (self.longueur_max //2, self.hauteur_max +190)),
        #    Bouton("MENU PRINCIPAL", (self.longueur_max //2, self.hauteur_max //2 +200), (self.longueur_max //2, self.hauteur_max +340))
        #]
        self.continu = True
        self.passage_menu = False
        self.curseur = 0
        self.cooldown = 0
        self.page = -1
        self.transition_en_cours = True
        
        self.ecran_noir = pygame.Surface((self.longueur_max, self.hauteur_max))
        self.visibilite = 0
    
    def lancement(self):
        self.transition_en_cours = False
        self.page = 2
        self.visibilite = 255
    
    def haut(self):
        pass
    
    def bas(self):
        pass
    
    def selection(self):
        pass
    
    
    
    def update(self):
        #effet d'apparition en fondu
        if self.page == -1:
            if self.visibilite < 255:
                self.visibilite += 3
            else:
                self.lancement()
    
    def draw(self, surface):
        surface.blit(self, (0, 0))
        
        self.joueur.update
        self.vague.update()
        self.vague.draw(surface)
        self.joueur.projectiles.draw(surface)
        surface.blit(self.joueur.image, self.joueur.rect.topleft)
        self.header.draw(surface)
        
        self.ecran_noir.set_alpha(255-self.visibilite)
        surface.blit(self.ecran_noir, (0, 0))
        
        for b in self.boutons:
            self.boutons[b].draw(surface)
            
        print(self.visibilite)

        