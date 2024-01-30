import pygame
from math import log
from MenuAccueil import *
from Vague import *
from constantes import *
from Bouton import Bouton
from Joueur import Joueur
from GameBar import GameBar
from MixerAudio import MixerAudio

class SessionJeu(pygame.Surface):
    """classe représentant une session de jeu
    """
    
    def __init__(self, size, gestion):
        pygame.Surface.__init__(self, size)
        self.fill("WHITE")
    
        self.longueur_max = size[0]
        self.hauteur_max = size[1]
        
        
        self.header = GameBar((self.longueur_max, 70), None)
        self.joueur = Joueur((self.longueur_max //2, self.hauteur_max * 0.8),
                             (0, self.header.get_height()), (self.longueur_max, self.hauteur_max), vie_joueur)
        self.header.joueur = self.joueur
        self.gestion = gestion
        
        self.nb_petits = 5
        self.nb_moyens = 2
        self.nb_gros = 0
        self.visibles = 5
        self.nb_coeurs = 2
        self.nb_munitions = 2
        self.nb_explosifs = 0
        self.nb_feux = 0
        self.nb_vitesses = 0
        self.num_vague = 1
        self.vague = None
        self.boutons = [
            Bouton("REPRENDRE", (self.longueur_max //2, self.hauteur_max//2 -70), (self.longueur_max //2, self.hauteur_max+40), 'WHITE'),
            Bouton(("MUSIQUE : OUI" if self.gestion.son_active else "MUSIQUE : NON"), (self.longueur_max //2, self.hauteur_max//2 +30), (self.longueur_max //2, self.hauteur_max +190), 'WHITE'),
            Bouton("MENU PRINCIPAL", (self.longueur_max //2, self.hauteur_max //2 +130), (self.longueur_max //2, self.hauteur_max +340), 'WHITE'),
            Bouton("RECOMMENCER", (self.longueur_max //2 -200, self.hauteur_max //2 +100), (-100, self.hauteur_max //2 +100), 'WHITE'),
            Bouton("MENU PRINCIPAL", (self.longueur_max //2 +200, self.hauteur_max //2 +100), (self.longueur_max+100, self.hauteur_max //2 +100), 'WHITE')
        ]
        self.boutons_entrants = []
        self.boutons_sortants = []
        
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
        
        #print("vague n°"+str(self.num_vague), self.visibles, "visibles  ", self.nb_petits, "petits  ", self.nb_moyens, "moyens  ", self.nb_gros, "gros  ",
        #        self.nb_coeurs, 'coeurs  ', self.nb_munitions, 'munitions  ', self.nb_explosifs, 'explosifs  ', self.nb_feux, 'feux  ', self.nb_vitesses, 'vitesses')
        
    def nouvelle_vague(self):
        self.num_vague += 1
        self.nb_petits += 3
        self.nb_moyens += 2
        self.nb_gros += ((1 if not self.num_vague %2 else 0) if self.num_vague > 3 else 0)
        self.visibles += 1
        self.nb_coeurs += (1 if not self.num_vague %4 else 0)
        self.nb_munitions += (3 if self.num_vague < 10 else 1)
        self.nb_explosifs = ((1 if not self.num_vague %2 else 0) if self.num_vague < 10 else 1)
        self.nb_feux = (1 if not (self.num_vague+1) %4 else 0)
        self.nb_vitesses = (1 if not self.num_vague %4 else 0)
        self.vague = Vague("VAGUE N°"+str(self.num_vague),
            coord_min=(0, self.header.get_height()), coord_max=(self.longueur_max, self.hauteur_max),
            joueur=self.joueur, nb_simultanes=self.visibles,
            nb_petits=self.nb_petits, nb_moyens=self.nb_moyens, nb_gros=self.nb_gros,
            nb_coeurs=self.nb_coeurs, nb_munitions=self.nb_munitions, nb_explosifs=self.nb_explosifs,
            nb_vitesses=self.nb_vitesses, nb_feux=self.nb_feux)
        #print("vague n°"+str(self.num_vague), self.visibles, "visibles  ", self.nb_petits, "petits  ", self.nb_moyens, "moyens  ", self.nb_gros, "gros  ",
        #    self.nb_coeurs, 'coeurs  ', self.nb_munitions, 'munitions  ', self.nb_explosifs, 'explosifs  ', self.nb_feux, 'feux  ', self.nb_vitesses, 'vitesses')
     
    def haut(self):
        if not self.transition_en_cours:
            if self.page == 0:
                self.joueur.haut()
                
            elif self.page == 1 and self.cooldown == 0:
                self.cooldown = 1
                limite = 0
                
                match self.page:
                    case 1:
                        limite = 0
                    
                    case 2:
                        limite = 3
                        
                if self.curseur-1 >= limite:
                    self.boutons[self.curseur].selectionne = False
                    self.curseur -= 1
                    self.boutons[self.curseur].selectionne = True
                    
                    if self.gestion.son_active: MixerAudio.suivant()
        
    def bas(self):
        if not self.transition_en_cours:
            if self.page == 0:
                self.joueur.bas()
                
            elif self.page == 1 and self.cooldown == 0:
                self.cooldown = 1
                limite = 0
                
                match self.page:
                    case 1:
                        limite = 2
                    
                    case 2:
                        limite = 4
                        
                if self.curseur+1 <= limite:
                    self.boutons[self.curseur].selectionne = False
                    self.curseur += 1
                    self.boutons[self.curseur].selectionne = True
                    
                    if self.gestion.son_active: MixerAudio.suivant()
            
    def gauche(self):
        if not self.transition_en_cours:
            if self.page == 0:
                self.joueur.gauche()
                
            elif self.page == 3 and self.cooldown == 0:
                self.cooldown = 1
                limite = 3
                        
                if self.curseur-1 >= limite:
                    self.boutons[self.curseur].selectionne = False
                    self.curseur -= 1
                    self.boutons[self.curseur].selectionne = True
                    
                    if self.gestion.son_active: MixerAudio.suivant()
        
    def droite(self):
        if not self.transition_en_cours:
            if self.page == 0:
                self.joueur.droite()
            
            elif self.page == 3 and self.cooldown == 0:
                self.cooldown = 1
                limite = 4
                        
                if self.curseur+1 <= limite:
                    self.boutons[self.curseur].selectionne = False
                    self.curseur += 1
                    self.boutons[self.curseur].selectionne = True
                    
                    if self.gestion.son_active: MixerAudio.suivant()
           
    def a_presse(self):
        if not self.transition_en_cours:
            if self.page == 0:
                self.joueur.tirer()
            
            if self.page in [1, 3]:
                match self.curseur:
                    case 0:
                        self.transition_jeu()
                        if self.gestion.son_active: MixerAudio.entree()
                    case 1:
                        if self.cooldown == 0:
                            self.cooldown += 1
                            
                            self.gestion.son_active = not self.gestion.son_active
                            if self.gestion.son_active:
                                self.boutons[1].message = "MUSIQUE : OUI"
                            else:
                                self.boutons[1].message = "MUSIQUE : NON"
                                
                            if self.gestion.son_active: MixerAudio.ok()
                    case 2:
                        self.transition_menu_principal()
                        if self.gestion.son_active: MixerAudio.entree()
                    case 3:
                        self.recommencement()
                        if self.gestion.son_active: MixerAudio.entree()
                    case 4:
                        self.transition_menu_principal()
                        if self.gestion.son_active: MixerAudio.entree()
    
    def b_presse(self):
        if not self.transition_en_cours:
            if self.page == 0 and self.joueur.explosion():
                self.vague.explosion()

    def m_presse(self):
        if not self.transition_en_cours and self.page == 0:
            self.joueur.bouclier()

    def menu_presse(self):
        if not self.transition_en_cours and self.cooldown == 0:
            self.cooldown = 1
            
            #transition du jeu au menu de pause
            if self.page == 0:
                self.transition_menu_pause()
            #retour au jeu
            elif self.page == 1:
                self.transition_jeu()
    
    def transition_menu_pause(self):
        self.curseur = 0
        self.transition_en_cours = True
        self.page = 1
        
        #on insère les trois boutons présents dans le menu de pause
        for i in range(3):
            self.boutons[i].transition()
            self.boutons_entrants.append(i)
    
    def transition_jeu(self):
        self.transition_en_cours = True
        self.page = 0
        
        #on fait transitionner tous les boutons déjà présents
        for b in self.boutons_entrants:
            self.boutons[b].transition()
            self.boutons_sortants.append(b)
        self.boutons_entrants.clear()
        
    def transition_menu_principal(self):
        self.curseur = 0
        self.transition_en_cours = True
        self.page = 2
        
        #on fait transitionner tous les boutons présents
        for b in self.boutons_entrants:
            self.boutons[b].transition()
            self.boutons_sortants.append(b)
        self.boutons_entrants.clear()
        
    def transition_gameover(self):
        self.curseur = 3
        self.transition_en_cours = True
        self.page = 3
        
        #on insère les trois boutons présents dans le menu de pause
        for i in range(3, 5):
            self.boutons[i].transition()
            self.boutons_entrants.append(i)
        
    def recommencement(self):
        self.transition_en_cours = True
        self.page = 4
        
        #on fait transitionner tous les boutons présents
        for b in self.boutons_entrants:
            self.boutons[b].transition()
            self.boutons_sortants.append(b)
        self.boutons_entrants.clear()
    
    def update(self):
        
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
                if self.boutons_entrants: self.boutons[self.boutons_entrants[0]].selectionne = True
            
            match self.page:
                
                #effet d'apparition en fondu
                case -1:
                    if (self.ecran_noir.get_alpha() if self.ecran_noir.get_alpha() else 0) > 0:
                        self.ecran_noir.set_alpha((self.ecran_noir.get_alpha() if self.ecran_noir.get_alpha() else 0) - 3)
                    else:
                        self.lancement()
                    
                case 0:
                    if (self.ecran_noir.get_alpha() if self.ecran_noir.get_alpha() else 0) > 0:
                        self.ecran_noir.set_alpha((self.ecran_noir.get_alpha() if self.ecran_noir.get_alpha() else 0) - 3)
                    elif disparition:
                        self.transition_en_cours = False
                        
                case 1:
                    if (self.ecran_noir.get_alpha() if self.ecran_noir.get_alpha() else 0) < 201:
                        self.ecran_noir.set_alpha((self.ecran_noir.get_alpha() if self.ecran_noir.get_alpha() else 0) + 3)
                    elif disparition:
                        self.transition_en_cours = False
                
                case 2:
                    self.ecran_noir.set_alpha((self.ecran_noir.get_alpha() if self.ecran_noir.get_alpha() else 0) + 1)
                    if disparition and (self.ecran_noir.get_alpha() if self.ecran_noir.get_alpha() else 0) == 255:
                        self.passage_menu = True
                        
                case 3:
                    self.vague.update()
                    if (self.ecran_noir.get_alpha() if self.ecran_noir.get_alpha() else 0) < 202:
                        self.ecran_noir.set_alpha((self.ecran_noir.get_alpha() if self.ecran_noir.get_alpha() else 0) + 2)
                    elif disparition:
                        self.transition_en_cours = False
                        
                case 4:
                    self.ecran_noir.set_alpha((self.ecran_noir.get_alpha() if self.ecran_noir.get_alpha() else 0) + 1)
                    if disparition and (self.ecran_noir.get_alpha() if self.ecran_noir.get_alpha() else 0) == 255:
                        self.__init__((self.longueur_max, self.hauteur_max), self.gestion)
                
        elif self.page in [0, 3]:
            self.joueur.update()
            self.vague.update()
            if self.vague.finie:
                self.nouvelle_vague()
                
        if self.page == 0 and self.joueur.disparu(): self.transition_gameover()
    
    def draw(self, surface):
        surface.blit(self, (0, 0))
        
        if self.page == 0 and not self.joueur.disparu(): self.joueur.draw(surface)
        self.joueur.projectiles.draw(surface)
        
        #on fait apparaître la barre d'informations
        if self.page == -1:
            self.header.draw(surface)
        else:
            self.vague.draw(surface)
            self.header.draw(surface, self.vague.nom)
        
        surface.blit(self.ecran_noir, ((0, 0) if self.page in [-1, 2, 4] else (0, self.header.get_height())))
        
        if self.page == 3:
            font = pygame.font.Font(pygame.font.match_font(POLICE), 120)
            gameover = font.render('GAME OVER', True, 'WHITE')
            surface.blit(gameover, (self.longueur_max //2 - gameover.get_width()//2, self.hauteur_max //2 -100 - gameover.get_height()//2))
        
        for b in self.boutons_sortants + self.boutons_entrants:
            self.boutons[b].draw(surface)
