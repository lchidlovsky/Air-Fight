import pygame
from math import log
from menus import *
from Vague import *
from constantes import *
from Bouton import Bouton
from Joueur import Joueur
from GameBar import GameBar

class SessionJeu(pygame.Surface):
    """classe représentant une session de jeu
    """
    
    def __init__(self, size):
        pygame.Surface.__init__(self, size)
        self.fill("WHITE")
    
        self.longueur_max = size[0]
        self.hauteur_max = size[1]
        
        
        self.header = GameBar((self.longueur_max, 70), None)
        self.joueur = Joueur((self.longueur_max //2, self.hauteur_max * 0.8),
                             (0, self.header.get_height()), (self.longueur_max, self.hauteur_max), vie_joueur)
        self.header.joueur = self.joueur
        
        self.nb_petits = 5
        self.nb_moyens = 2
        self.nb_gros = 0
        self.visibles = 5
        self.nb_coeurs = 3
        self.nb_munitions = 2
        self.nb_explosifs = 0
        self.nb_feux = 0
        self.nb_vitesses = 0
        self.num_vague = 1
        self.vague = None
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
        self.ecran_noir.set_alpha(255)
    
    def lancement(self):
        self.transition_en_cours = False
        self.page = 0
        self.vague = Vague("VAGUE N°"+str(self.num_vague),
                        coord_min=(0, self.header.get_height()), coord_max=(self.longueur_max, self.hauteur_max),
                        joueur=self.joueur, nb_simultanes=self.visibles,
                        nb_petits=self.nb_petits, nb_moyens=self.nb_moyens, nb_gros=self.nb_gros,
                        nb_coeurs=self.nb_coeurs, nb_munitions=self.nb_munitions, nb_explosifs=self.nb_explosifs,
                        nb_vitesses=self.nb_vitesses, nb_feux=self.nb_feux)
        
        print("vague n°"+str(self.num_vague), self.visibles, "visibles  ", self.nb_petits, "petits  ", self.nb_moyens, "moyens  ", self.nb_gros, "gros  ",
                self.nb_coeurs, 'coeurs   ', self.nb_munitions, 'munitions')
        
    def nouvelle_vague(self):
        self.num_vague += 1
        self.nb_petits += 3
        self.nb_moyens += 1 + (1 if not self.num_vague %2 else 0)
        self.nb_gros += (1 if not self.num_vague %2 else 0)
        self.visibles += 1
        self.nb_coeurs += ((1 if not self.num_vague %2 else 0) if self.num_vague < 11 else 2)
        self.nb_munitions += 1
        self.nb_explosifs = (1 if not self.num_vague %2 else 0)
        self.nb_feux = (1 if not self.num_vague %3 else 0)
        self.nb_vitesses = (1 if not self.num_vague %4 else 0)
        self.vague = Vague("VAGUE N°"+str(self.num_vague),
            coord_min=(0, self.header.get_height()), coord_max=(self.longueur_max, self.hauteur_max),
            joueur=self.joueur, nb_simultanes=self.visibles,
            nb_petits=self.nb_petits, nb_moyens=self.nb_moyens, nb_gros=self.nb_gros,
            nb_coeurs=self.nb_coeurs, nb_munitions=self.nb_munitions, nb_explosifs=self.nb_explosifs,
            nb_vitesses=self.nb_vitesses, nb_feux=self.nb_feux)
        print("vague n°"+str(self.num_vague), self.visibles, "visibles  ", self.nb_petits, "petits  ", self.nb_moyens, "moyens  ", self.nb_gros, "gros  ",
                self.nb_coeurs, 'coeurs   ', self.nb_munitions, 'munitions')
    
    def haut(self):
        if self.page == 0:
            self.joueur.haut()
    
    def bas(self):
        if self.page == 0:
            self.joueur.bas()
        
    def gauche(self):
        if self.page == 0:
            self.joueur.gauche()
    
    def droite(self):
        if self.page == 0:
            self.joueur.droite()
        
    def a_presse(self):
        if self.page == 0:
            self.joueur.tirer()
            
    def b_presse(self):
        if self.page == 0:
            self.joueur.explosion_generale()
    
    
    def update(self):
        #effet d'apparition en fondu
        if self.page == -1:
            if (self.ecran_noir.get_alpha() if self.ecran_noir.get_alpha() else 0) > 0:
                self.ecran_noir.set_alpha((self.ecran_noir.get_alpha() if self.ecran_noir.get_alpha() else 0) - 3)
            else:
                self.lancement()
        else:
            self.joueur.update()
            self.vague.update()
            if self.vague.finie:
                self.nouvelle_vague()
                
    
    def draw(self, surface):
        surface.blit(self, (0, 0))
        if self.page != -1: self.vague.draw(surface)
        self.joueur.projectiles.draw(surface)
        surface.blit(self.joueur.image, self.joueur.rect.topleft)
        if self.page == -1:
            self.header.draw(surface)
        else:
            self.header.draw(surface, self.vague.nom)
        
        surface.blit(self.ecran_noir, (0, 0))
        
        for b in self.boutons:
            self.boutons[b].draw(surface)
