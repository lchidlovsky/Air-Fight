import pygame
from constantes import *
from Bouton import Bouton
from MixerAudio import MixerAudio

class MenuAccueil(pygame.Surface):
    """classe représentant le menu principal du jeu
    """
    def __init__(self, size, gestion):
        pygame.Surface.__init__(self, size)
        self.fill("WHITE")
        
        self.longueur_max = size[0]
        self.hauteur_max = size[1]
        
        titre = pygame.image.load("images/autres/air-fight.png").convert_alpha()
        self.titre = pygame.transform.scale(titre, (720, 135))
        self.titre.set_alpha(0)
        self.titre_pos = (self.longueur_max//2 - self.titre.get_width()//2, self.hauteur_max //2 -250 - self.titre.get_height()//2)
        
        self.manette = pygame.image.load("images/autres/manette.png").convert_alpha()
        self.manette.set_alpha(0)
        self.manette_pos = (self.longueur_max//2 -310 - self.manette.get_width()//2, self.hauteur_max //2 - self.manette.get_height()//2)
        
        self.gestion = gestion
        
        self.boutons = [
            Bouton("JOUER", (self.longueur_max //2, self.hauteur_max //2), (self.longueur_max //2, self.hauteur_max+40)),
            Bouton("OPTIONS", (self.longueur_max //2, self.hauteur_max //2 +100), (self.longueur_max //2, self.hauteur_max +190)),
            Bouton("QUITTER", (self.longueur_max //2, self.hauteur_max //2 +200), (self.longueur_max //2, self.hauteur_max +340)),
            Bouton(("MUSIQUE : OUI" if self.gestion.son_active else "MUSIQUE : NON"), (self.longueur_max //2+320, self.hauteur_max//2-120), (self.longueur_max +150, self.hauteur_max//2-120)),
            Bouton(("MANETTE : XBOX" if self.gestion.manette_xbox else "MANETTE : PS"), (self.longueur_max //2+320, self.hauteur_max//2-20), (self.longueur_max +150, self.hauteur_max//2-20)),
            Bouton("RETOUR", (self.longueur_max //2+320, self.hauteur_max//2+80), (self.longueur_max +150, self.hauteur_max//2+80))
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
            self.manette.set_alpha(5)
            
            #on fait transitionner tous les boutons déjà présents
            for b in self.boutons_entrants:
                self.boutons[b].transition()
                self.boutons_sortants.append(b)
            
            #on insère les trois boutons présents dans le menu d'options
            for i in range(3, 6):
                self.boutons[i].transition()
                self.boutons_entrants.append(i)
                
            self.boutons_entrants = self.boutons_entrants[-3:]
    
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
                
                if self.gestion.son_active: MixerAudio.suivant()
    
    def bas(self):
        if not self.transition_en_cours and self.cooldown == 0:
            self.cooldown = 1
            limite = 0
            
            match self.page:
                case 0:
                    limite = 2
                case 2:
                    limite = 5
            if self.curseur+1 <= limite:
                self.boutons[self.curseur].selectionne = False
                self.curseur += 1
                self.boutons[self.curseur].selectionne = True
                
                if self.gestion.son_active: MixerAudio.suivant()
                        
    def a_presse(self):
        if not self.transition_en_cours and self.page in [0, 2]:
            match self.curseur:
                case 0:
                    self.transition_jouer()
                    if self.gestion.son_active: MixerAudio.entree()
                case 1:
                    self.transition_options()
                    if self.gestion.son_active: MixerAudio.ok()
                case 2:
                    self.transition_quitter()
                    if self.gestion.son_active: MixerAudio.ok()
                case 3:
                    if self.cooldown == 0:
                        self.cooldown += 1
                        
                        self.gestion.son_active = not self.gestion.son_active
                        if self.gestion.son_active:
                            self.boutons[3].message = "MUSIQUE : OUI"
                        else:
                            self.boutons[3].message = "MUSIQUE : NON"
                            
                        if self.gestion.son_active: MixerAudio.ok()
                case 4:
                    if self.cooldown == 0:
                        self.cooldown += 1
                        
                        self.gestion.manette_xbox = not self.gestion.manette_xbox
                        if self.gestion.manette_xbox:
                            self.boutons[4].message = "MANETTE : XBOX"
                        else:
                            self.boutons[4].message = "MANETTE : PS"
                            
                        if self.gestion.son_active: MixerAudio.ok()
                case 5:
                    self.transition_accueil()
                            
                    if self.gestion.son_active: MixerAudio.ok()
               
    def update(self):
        #effet d'apparition en fondu
        if self.page == -1:
            if (self.ecran_noir.get_alpha() if self.ecran_noir.get_alpha() else 0) > 1:
                self.ecran_noir.set_alpha((self.ecran_noir.get_alpha() if self.ecran_noir.get_alpha() else 0) - 3)
            else:
                self.transition_en_cours = False
                self.transition_accueil()
        
        if self.page == 1 and (self.ecran_noir.get_alpha() if self.ecran_noir.get_alpha() else 0) > 254:
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
                
            #on fait apparaitre/disparaitre la manette
            if self.page == 2 and (self.manette.get_alpha() if self.manette.get_alpha() else 0) < 255:
                self.manette.set_alpha((self.manette.get_alpha() if self.manette.get_alpha() else 0) + 5)
            if self.page != 2 and (self.manette.get_alpha() if self.manette.get_alpha() else 0) > 0:
                self.manette.set_alpha((self.manette.get_alpha() if self.manette.get_alpha() else 0) - 5)
        
        else:   #on assombrit l'écran
            if self.page == 1 and 2 < (self.ecran_noir.get_alpha() if self.ecran_noir.get_alpha() else 0):
                self.ecran_noir.set_alpha((self.ecran_noir.get_alpha() if self.ecran_noir.get_alpha() else 0)+3)
        
    def draw(self, surface):
        surface.blit(self, (0, 0))
        surface.blit(self.titre, self.titre_pos)
        surface.blit(self.manette, self.manette_pos)
        
        for b in self.boutons_sortants + self.boutons_entrants:
            self.boutons[b].draw(surface)
            
        #affichages des indications de controles manettes
        if self.page == 2 and not self.transition_en_cours:
            font = pygame.font.Font(pygame.font.match_font(POLICE), 25)
            
            movement = font.render('Déplacement', True, 'WHITE')
            pygame.draw.rect(surface, 'ORANGE',
                             (self.manette_pos[0] - movement.get_width() - 50, self.manette_pos[1] + self.manette.get_height() * 0.51 -3,
                              movement.get_width()+6, movement.get_height()+6), 0, 10)
            surface.blit(movement, (self.manette_pos[0] - movement.get_width() - 47, self.manette_pos[1] + self.manette.get_height() * 0.51))
            pygame.draw.line(surface, 'ORANGE',
                             (self.manette_pos[0] - 33, self.manette_pos[1] + self.manette.get_height() * 0.51 + movement.get_height()//2),
                             (self.manette_pos[0] + self.manette.get_width() * 0.28, self.manette_pos[1] + self.manette.get_height() * 0.51 + movement.get_height()//2), 4)
            
            a = font.render('Tirer', True, 'WHITE')
            pygame.draw.rect(surface, 'GREEN',
                             (self.manette_pos[0] + self.manette.get_width() + 41, self.manette_pos[1] + self.manette.get_height() * 0.6 -3,
                              a.get_width()+6, a.get_height()+6), 0, 10)
            surface.blit(a, (self.manette_pos[0] + self.manette.get_width() + 44, self.manette_pos[1] + self.manette.get_height() * 0.6))
            pygame.draw.line(surface, 'GREEN',
                             (self.manette_pos[0] + self.manette.get_width() * 0.83, self.manette_pos[1] + self.manette.get_height() * 0.47),
                             (self.manette_pos[0] + self.manette.get_width() + 33, self.manette_pos[1] + a.get_height()//2 + self.manette.get_height() * 0.6), 4)
            
            surface.blit(pygame.image.load("images/logos/logo_bouclier.png").convert_alpha(),
                         (self.manette_pos[0] + self.manette.get_width() + 58, self.manette_pos[1] + self.manette.get_height() * 0.27))
            pygame.draw.line(surface, 'RED',
                             (self.manette_pos[0] + self.manette.get_width() * 0.90, self.manette_pos[1] + self.manette.get_height() * 0.34),
                             (self.manette_pos[0] + self.manette.get_width() + 48, self.manette_pos[1] + self.manette.get_height() * 0.34), 4)
            
        
        surface.blit(self.ecran_noir, (0, 0))
