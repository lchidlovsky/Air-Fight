import pygame
from random import randint
from constantes import *
from projectile import Projectile

class Ennemi(pygame.sprite.Sprite):
    """classe représentant un ennemi quelconque
    """
    def __init__(self, apparences, coord, vitesse):
        pygame.sprite.Sprite.__init__(self)
        self.apparences = apparences
        self.num_apparence = 0
        self.horloge_apparence = 0
        
        self.image = apparences[0]
        self.rect = self.image.get_rect()
        self.rect.midbottom = coord
        
        self.vitesse = vitesse
        
        self.vivant = True
        self.existant = True
        
    def tick(self):
        self.bas(self.vitesse)
        
        
        if not self.vivant:             #animation de destruction du vaisseau
            if self.horloge_apparence % 8 == 0:
                if self.num_apparence < len(self.apparences)-1:
                    self.num_apparence += 1
                    self.image = self.apparences[self.num_apparence]
                else:
                    self.existant = False

            self.horloge_apparence += 1
            
    def bas(self, vitesse):
        self.rect.top += vitesse



class Petit(Ennemi):
    """classe représentant un petit ennemi
    """
    def __init__(self, coord):
        
        apparences = []
        for i in range(1,4):
            apparences.append(pygame.image.load(f"images/ennemis/petit_{i}.png").convert_alpha())
        
        super().__init__(apparences, coord, vitesse_petit)
        


class Moyen(Ennemi):
    """classe représentant un ennemi de taille moyenne
    """
    def __init__(self, coord, h_max):
        
        apparences = []
        for i in range(1,6):
            apparences.append(pygame.image.load(f"images/ennemis/moyen_{i}.png").convert_alpha())
        
        super().__init__(apparences, coord, vitesse_moyen)
        self.hauteur_max = h_max
        self.projectiles = pygame.sprite.Group()
        self.vitesse_tirs = 66
        self.cooldown = 1
        
    def tirer(self):
        if self.vivant and self.cooldown == 0 and not randint(0, self.vitesse_tirs):
            self.cooldown += 1
            return Projectile(pygame.image.load(f"images/autres/projectile_2.png").convert_alpha(), (self.rect.left +35, self.rect.top +66))

    def tick(self):
        super().tick()

        if self.cooldown > 0:       #gestion de la cadence de tir
            self.cooldown += 1
            if self.cooldown > self.vitesse_tirs:
                self.cooldown = 0
        

class Gros(Ennemi):
    """classe représentant un gros ennemi
    """
    def __init__(self, coord):
        
        apparences = []
        for i in range(1,8):
            apparences.append(pygame.image.load(f"images/ennemis/gros_{i}.png").convert_alpha())
        
        super().__init__(apparences, coord, vitesse_gros)